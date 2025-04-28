from fastapi.testclient import TestClient

def test_get_nonexistant_file(client:TestClient):
    response = client.get("/files/nonexistant_file.txt")
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}