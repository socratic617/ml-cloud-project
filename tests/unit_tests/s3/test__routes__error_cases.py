from fastapi import status
from fastapi.testclient import TestClient
from files_api.schemas import DEFAULT_GET_FILES_MAX_PAGE_SIZE
from tests.consts import TEST_BUCKET_NAME

def test_get_nonexistant_file(client:TestClient):
    response = client.get("/files/nonexistant_file.txt")
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}

def test_head_nonexistent_file(client: TestClient):
    '''
    Test the HEAD request for a nonexistent file.
    '''
    response = client.head("/files/nonexistent_file.txt")
    assert response.status_code == 404


def test_delete_nonexistent_file(client: TestClient):
    response = client.delete("/files/nonexistent_file.txt")
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}

def test_get_files_invalid_page_size(client: TestClient):
    response = client.get("/files?page_size=-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = client.get(f'/files?page_size={DEFAULT_GET_FILES_MAX_PAGE_SIZE + 1}')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_files_page_token_is_mutually_exclusive_with_page_size_and_directory(client: TestClient):
    response = client.get("/files?page_token=token&page_size=10")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "mutually exclusive" in str(response.json())

    response = client.get("/files?page_token=token&directory=dir")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "mutually exclusive" in str(response.json())


    response = client.get("/files?page_token=token&page_size=10&directory=dir")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "mutually exclusive" in str(response.json())
