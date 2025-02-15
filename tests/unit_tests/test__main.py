# import botocore
from typing import Generator
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from src.files_api.main import APP

# Constants for testing
test_file_path = "test.txt"
test_file_content = b"Hello, world!"
test_file_content_type = "text/plain"


# Fixture for FastAPI test client
@pytest.fixture
# pylint: disable=unused-argument
def client(mocked_aws: TestClient) -> Generator[TestClient]:
    """
        Create a generator with a TestClient object
    """
    with TestClient(APP) as client:
        yield client


def test__upload_file__happy_path(client: TestClient):
    # create a file
    test_file_path = "some/nested/file.txt"
    test_file_path = b"some content"
    test_file_path = "text/plain"

    response = client.put(
        f"/files/{test_file_path}",
        files={"file": (test_file_path, test_file_content, test_file_content_type)},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "file_path": test_file_path,
        "message": f"New file uploaded at path: /{test_file_path}",
    }

    # update an existing file
    updated_content = b"updated content"
    response = client.put(
        f"/files/{test_file_path}",
        files={"file": (test_file_path, updated_content, test_file_content_type)},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "file_path": test_file_path,
        "message": f"Existing file updated at path: /{test_file_path}",
    }


def test_list_files_with_pagination(client: TestClient):
    # Upload files
    for i in range(15):
        client.put(
            f"/files/file{i}.txt",
            files={"file": (f"file{i}.txt", test_file_content, test_file_content_type)},
        )
    # List files with page size 10
    response = client.get("/files?page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["files"]) == 10
    assert "next_page_token" in data


def test_get_file_metadata(client: TestClient):
    # Upload a file
    client.put(
        f"/files/{test_file_path}",
        files={"file": (test_file_path, test_file_content, test_file_content_type)},
    )
    # Get file metadata
    response = client.head(f"/files/{test_file_path}")
    assert response.status_code == 200
    headers = response.headers
    assert headers["Content-type"] == test_file_content_type
    assert headers["Content-Length"] == str(len(test_file_content))
    assert "Last-Modified" in headers


def test_get_file(client: TestClient):
    # Upload a file
    client.put(
        f"/files/{test_file_path}",
        files={"file": (test_file_path, test_file_content, test_file_content_type)},
    )
    # Get file
    response = client.get(f"/files/{test_file_path}")
    assert response.status_code == 200
    assert response.content == test_file_content


def test_delete_file(client: TestClient):
    # Upload a file
    client.put(
        f"/files/{test_file_path}",
        files={"file": (test_file_path, test_file_content, test_file_content_type)},
    )

    # Delete file
    response = client.delete(f"/files/{test_file_path}")
    assert response.status_code == 204

    # Verify deletion
    #
    # NOTE: this is an anti-pattern. The tests should be unaware of the internal implementation details
    # of the REST API. In this case, because the file is deleted from the S3 bucket, boto3 raises a NoSuchKey
    # exception when trying to fetch the file. This block succeeds only if a botocore exception is thrown.
    #
    # Later we will fix this by doing better error handling within the API itself.
    with pytest.raises(botocore.exceptions.ClientError):
        response = client.get(f"/files/{test_file_path}")


