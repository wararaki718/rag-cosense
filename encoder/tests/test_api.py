from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_encode_endpoint(client: TestClient, mock_model):
    test_text = "test message"
    response = client.post("/encode", json={"text": test_text})
    
    assert response.status_code == 200
    data = response.json()
    assert "sparse_values" in data
    assert data["sparse_values"] == {"hello": 1.0, "world": 0.5}
    
    mock_model.encode.assert_called_once_with(test_text)

def test_encode_endpoint_invalid_request(client: TestClient):
    # Missing 'text' field
    response = client.post("/encode", json={})
    assert response.status_code == 422
