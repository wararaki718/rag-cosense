from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_should_read_root_endpoint():
    """Test the root endpoint and verify the welcome message.
    
    Arrange: Set up the TestClient with the app.
    Act: Make a GET request to the root endpoint.
    Assert: Check that the status code is 200 and the message is correct.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to rag-cosense API"}
