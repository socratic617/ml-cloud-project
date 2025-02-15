#!/bin/bash

set -e

#####################
# --- Constants --- #
#####################

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
MINIMUM_TEST_COVERAGE_PERCENT=0


##########################
# --- Task Functions --- #
##########################

# install core and development Python dependencies into the currently activated venv
function install {
    python -m pip install --upgrade pip
    python -m pip install --editable "$THIS_DIR/[dev]"
}

# allows uvicorn to respond with requests with the latest changes to our code
function run {
   AWS_PROFILE=cloud-course uvicorn files_api.main:APP --reload
}


function is_moto_server_running {
    # Try to curl the local moto server
    if curl --silent --max-time 2 http://localhost:5001 > /dev/null; then
        echo "Moto server is running on localhost:5001"
        return 0
    else
        echo "Moto server is NOT running on localhost:5001"
        return 1
    fi
}

# this will run the fast api app but it mocks(using moto) the calls to aws
# start the FastAPI app, pointed at a mocked aws endpoint
function run-mock {
    set +e

    # Start moto.server in the background on localhost:5001
    # python -m moto.server -p 5001 &
    # MOTO_PID=$!

    echo "Checking if Moto server is already running else we will start a new moto server"
    ps aux | grep moto

    # Check if the moto server is running
    if is_moto_server_running; then
        echo "Proceeding with mock server setup."
    else
        echo "Starting moto.server..."
        python -m moto.server -p 5001 &
        MOTO_PID=$!
        sleep 5
    fi

    # point the AWS CLI and boto3 to the mocked AWS server using mocked credentials
    export AWS_ENDPOINT_URL="http://localhost:5001"
    # export AWS_SECRET_ACCESS_KEY="mock"
    # export AWS_ACCESS_KEY_ID="mock"
    # export AWS_PROFILE="mock"
    export AWS_DEFAULT_REGION="us-east-1"

    if aws s3 ls | grep -q "some-bucket"; then
        echo "Bucket 'some-bucket' already exists!"
    else
        aws s3 mb s3://some-bucket || echo "Error creating bucket"
        aws s3 mb s3://some-bucket-test || echo "Error creating bucket"
        aws s3 mb s3://some-bucket-test123 || echo "Error creating bucket"
    fi

    # Check if the bucket was created by listing the S3 buckets
    if aws s3 ls | grep -q "some-bucket"; then
        echo "Bucket 'some-bucket' was successfully created!"
    else
        echo "Failed to create 'some-bucket'."
    fi

    # echo aws s3 ls 
    echo "Display all existing buckets in the moto.server"
    aws s3 ls
    # Trap EXIT signal to kill the moto.server process when uvicorn stops
    trap 'kill $MOTO_PID' EXIT

    # Set AWS endpoint URL and start FastAPI app with uvicorn in the foreground
    uvicorn src.files_api.main:APP --reload

    # Wait for the moto.server process to finish (this is optional if you want to keep it running)
    wait $MOTO_PID
}

# run linting, formatting, and other static code quality tools
function lint {
    pre-commit run --all-files
}

# same as `lint` but with any special considerations for CI
function lint:ci {
    # We skip no-commit-to-branch since that blocks commits to `main`.
    # All merged PRs are commits to `main` so this must be disabled.
    SKIP=no-commit-to-branch pre-commit run --all-files
}

# execute tests that are not marked as `slow`
function test:quick {
    run-tests -m "not slow" ${@:-"$THIS_DIR/tests/"}
}

# execute tests against the installed package; assumes the wheel is already installed
function test:ci {
    INSTALLED_PKG_DIR="$(python -c 'import files_api; print(files_api.__path__[0])')"
    # in CI, we must calculate the coverage for the installed package, not the src/ folder
    COVERAGE_DIR="$INSTALLED_PKG_DIR" run-tests
}

# (example) ./run.sh test tests/test_states_info.py::test__slow_add
function run-tests {
    PYTEST_EXIT_STATUS=0

    # clean the test-reports dir
    rm -rf "$THIS_DIR/test-reports" || mkdir "$THIS_DIR/test-reports"

    # execute the tests, calculate coverage, and generate coverage reports in the test-reports dir
    python -m pytest ${@:-"$THIS_DIR/tests/"} \
        --cov "${COVERAGE_DIR:-$THIS_DIR/src}" \
        --cov-report html \
        --cov-report term \
        --cov-report xml \
        --junit-xml "$THIS_DIR/test-reports/report.xml" \
        --cov-fail-under "$MINIMUM_TEST_COVERAGE_PERCENT" || ((PYTEST_EXIT_STATUS+=$?))
    mv coverage.xml "$THIS_DIR/test-reports/" || true
    mv htmlcov "$THIS_DIR/test-reports/" || true
    mv .coverage "$THIS_DIR/test-reports/" || true
    return $PYTEST_EXIT_STATUS
}

function test:wheel-locally {
    deactivate || true
    rm -rf test-env || true
    python -m venv test-env
    source test-env/bin/activate
    clean || true
    pip install build
    build
    pip install ./dist/*.whl pytest pytest-cov
    test:ci
    deactivate || true
}

# serve the html test coverage report on localhost:8000
function serve-coverage-report {
    python -m http.server --directory "$THIS_DIR/test-reports/htmlcov/" 8000
}

# build a wheel and sdist from the Python source code
function build {
    python -m build --sdist --wheel "$THIS_DIR/"
}

function release:test {
    lint
    clean
    build
    publish:test
}

function release:prod {
    release:test
    publish:prod
}

function publish:test {
    try-load-dotenv || true
    twine upload dist/* \
        --repository testpypi \
        --username=__token__ \
        --password="$TEST_PYPI_TOKEN"
}

function publish:prod {
    try-load-dotenv || true
    twine upload dist/* \
        --repository pypi \
        --username=__token__ \
        --password="$PROD_PYPI_TOKEN"
}

# remove all files generated by tests, builds, or operating this codebase
function clean {
    rm -rf dist build coverage.xml test-reports
    find . \
      -type d \
      \( \
        -name "*cache*" \
        -o -name "*.dist-info" \
        -o -name "*.egg-info" \
        -o -name "*htmlcov" \
      \) \
      -not -path "*env/*" \
      -exec rm -r {} + || true

    find . \
      -type f \
      -name "*.pyc" \
      -not -path "*env/*" \
      -exec rm {} +
}

# export the contents of .env as environment variables
function try-load-dotenv {
    if [ ! -f "$THIS_DIR/.env" ]; then
        echo "no .env file found"
        return 1
    fi

    while read -r line; do
        export "$line"
    done < <(grep -v '^#' "$THIS_DIR/.env" | grep -v '^$')
}

# print all functions in this file
function help {
    echo "$0 <task> <args>"
    echo "Tasks:"
    compgen -A function | cat -n
}

TIMEFORMAT="Task completed in %3lR"
time ${@:-help}
