from fastapi import status
from fastapi.testclient import TestClient
from tests.consts import TEST_BUCKET_NAME

def test_get_nonexistant_file(client:TestClient):
    response = client.get("/files/nonexistant_file.txt")
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}

def test_head_nonexistent_file(client: TestClient):
    response = client.head("/files/nonexistent_file.txt")
    assert response.status_code == 404


def test_delete_nonexistent_file(client: TestClient):
    response = client.delete("/files/nonexistent_file.txt")
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}
