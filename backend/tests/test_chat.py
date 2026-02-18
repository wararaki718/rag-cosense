import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.core.config import settings
from src.schemas.chat import Source
from src.api.v1.endpoints.chat import get_chat_service

client = TestClient(app)

def test_chat_endpoint_success():
    """Test the /chat endpoint for a successful response."""
    # Mock ChatService.process_query
    mock_service_instance = MagicMock()
    mock_service_instance.process_query = AsyncMock(return_value=(
        "This is a test answer.",
        [
            Source(title="Test Page", url="https://example.com", score=0.95),
        ]
    ))
    
    # Override the dependency in FastAPI
    app.dependency_overrides[get_chat_service] = lambda: mock_service_instance
    
    payload = {
        "query": "What is the test?",
        "context_history": [
            {"role": "user", "content": "Previous message"}
        ]
    }
    
    try:
        response = client.post(f"{settings.API_V1_STR}/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["answer"] == "This is a test answer."
        assert len(data["data"]["sources"]) == 1
        assert data["data"]["sources"][0]["title"] == "Test Page"
    finally:
        # Cleanup override
        app.dependency_overrides = {}

@pytest.mark.anyio
async def test_chat_service_process_query():
    """Test ChatService's process_query method."""
    from src.services.chat import ChatService
    
    with patch("src.services.chat.AsyncElasticsearch") as mock_es_cls, \
         patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
    
        # Mock ES search
        mock_es_instance = mock_es_cls.return_value
        mock_es_instance.search = AsyncMock(return_value={
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "text": "Context content",
                            "metadata": {"title": "Test Page"}
                        },
                        "_score": 0.8
                    }
                ]
            }
        })
        # Mock httpx POST responses (first for encoder, second for ollama)
        mock_resp_encoder = MagicMock()
        mock_resp_encoder.status_code = 200
        mock_resp_encoder.json.return_value = {"sparse_values": {"token1": 1.0}}
        mock_resp_encoder.raise_for_status = MagicMock()
        
        mock_resp_ollama = MagicMock()
        mock_resp_ollama.status_code = 200
        mock_resp_ollama.json.return_value = {"response": "AI generated answer"}
        mock_resp_ollama.raise_for_status = MagicMock()
        
        # Configure mock_post to return different responses in order
        mock_post.side_effect = [mock_resp_encoder, mock_resp_ollama]
        
        service = ChatService()
        query = "Tell me about tests"
        answer, sources = await service.process_query(query)
        
        assert answer == "AI generated answer"
        assert len(sources) == 1
        assert sources[0].title == "Test Page"
        assert sources[0].score == 0.8
        
        # Verify ES was called correctly
        mock_es_instance.search.assert_called_once()
        # Verify httpx POST was called twice
        assert mock_post.call_count == 2
