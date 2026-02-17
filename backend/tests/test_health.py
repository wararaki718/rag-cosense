from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.main import app
from src.core.config import settings

client = TestClient(app)

def test_should_return_connected_for_all_services_when_healthy():
    """Test health check endpoint when all services are connected.
    
    Arrange: Mock connected status for Elasticsearch, Ollama, and Encoder.
    Act: Make a GET request to the health endpoint.
    Assert: Check that all services show 'connected' status.
    """
    with patch("src.api.v1.endpoints.health.AsyncElasticsearch") as mock_es, \
         patch("httpx.AsyncClient.get") as mock_get:
        
        # Mock Elasticsearch
        mock_es_instance = mock_es.return_value
        mock_es_instance.ping = AsyncMock(return_value=True)
        mock_es_instance.close = AsyncMock()
        
        # Mock httpx responses for Ollama and Encoder
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        response = client.get(f"{settings.API_V1_STR}/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["services"]["elasticsearch"] == "connected"
        assert data["services"]["ollama"] == "connected"
        assert data["services"]["encoder"] == "connected"

def test_should_return_error_status_when_services_are_down():
    """Test health check endpoint when services are disconnected.
    
    Arrange: Mock disconnected status for Elasticsearch, Ollama, and Encoder.
    Act: Make a GET request to the health endpoint.
    Assert: Check that all services show appropriate error/disconnected status.
    """
    with patch("src.api.v1.endpoints.health.AsyncElasticsearch") as mock_es, \
         patch("httpx.AsyncClient.get") as mock_get:
        
        # Mock Elasticsearch failure
        mock_es_instance = mock_es.return_value
        mock_es_instance.ping = AsyncMock(return_value=False)
        mock_es_instance.close = AsyncMock()
        
        # Mock httpx failure for Ollama and Encoder
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        response = client.get(f"{settings.API_V1_STR}/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["services"]["elasticsearch"] == "disconnected"
        assert data["services"]["ollama"] == "unexpected status code: 500"
        assert data["services"]["encoder"] == "unexpected status code: 500"

def test_should_return_exception_status_when_services_raise_exception():
    """Test health check endpoint when services raise exceptions.
    
    Arrange: Mock exceptions for Elasticsearch, Ollama, and Encoder.
    Act: Make a GET request to the health endpoint.
    Assert: Check that all services show error messages from exceptions.
    """
    with patch("src.api.v1.endpoints.health.AsyncElasticsearch") as mock_es, \
         patch("httpx.AsyncClient.get") as mock_get:
        
        # Mock Elasticsearch raising exception
        mock_es.side_effect = Exception("ES connection failed")
        
        # Mock httpx raising exception for Ollama and Encoder
        mock_get.side_effect = Exception("HTPX connection failed")
        
        response = client.get(f"{settings.API_V1_STR}/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "error: ES connection failed" in data["services"]["elasticsearch"]
        assert "error: HTPX connection failed" in data["services"]["ollama"]
        assert "error: HTPX connection failed" in data["services"]["encoder"]
