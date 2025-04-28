import pytest
from fastapi.testclient import TestClient
from files_api.main import create_app
from files_api.settings import Settings
from typing import Generator

from tests.consts import TEST_BUCKET_NAME

# Fixture for FastAPI test client
@pytest.fixture
# pylint: disable=unused-argument
def client(mocked_aws: TestClient) -> Generator[TestClient]:
    """
        Create a generator with a TestClient object
    """
    settings = Settings(s3_bucket_name=TEST_BUCKET_NAME)

    app = create_app(settings=settings)
    with TestClient(app) as client:
        yield client
