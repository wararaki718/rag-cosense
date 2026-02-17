import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.indexer import IndexerService
from src.services.cosense import CosenseClient

@pytest.fixture
def mock_cosense_client():
    client = MagicMock(spec=CosenseClient)
    client.get_page_content = AsyncMock()
    return client

@pytest.mark.anyio
async def test_should_create_index_if_not_exists_successfully():
    """Test index creation logic in Elasticsearch.
    
    Arrange: Mock AsyncElasticsearch to return index not exists.
    Act: Call create_index_if_not_exists.
    Assert: Check indices.create is called with the expected body.
    """
    with patch("src.services.indexer.AsyncElasticsearch") as mock_es_class:
        mock_es = mock_es_class.return_value
        mock_es.indices.exists = AsyncMock(return_value=False)
        mock_es.indices.create = AsyncMock()
        
        service = IndexerService()
        await service.create_index_if_not_exists()
        
        mock_es.indices.exists.assert_called_once_with(index="cosense_pages")
        mock_es.indices.create.assert_called_once()
        args, kwargs = mock_es.indices.create.call_args
        assert kwargs["index"] == "cosense_pages"
        assert "mappings" in kwargs["body"]

@pytest.mark.anyio
async def test_should_get_sparse_embeddings_via_encoder_service_successfully():
    """Test retrieving sparse embeddings from the encoder service.
    
    Arrange: Mock httpx.AsyncClient.post to return mock sparse values.
    Act: Call get_sparse_embeddings.
    Assert: Check that returned dictionary matches expectations.
    """
    mock_sparse_values = {"1": 0.5, "2": 0.8}
    
    with patch("src.services.indexer.AsyncElasticsearch"), \
         patch("httpx.AsyncClient.post") as mock_post:
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"sparse_values": mock_sparse_values}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        service = IndexerService()
        result = await service.get_sparse_embeddings("test text")
        
        assert result == mock_sparse_values

@pytest.mark.anyio
async def test_should_sync_pages_into_elasticsearch_successfully(mock_cosense_client):
    """Test synchronizing Cosense pages with Elasticsearch indexing.
    
    Arrange: Mock all external interactions (index check, content fetch, encoder service, ES index).
    Act: Call sync_pages.
    Assert: Verify that indexing occurs for each page and its chunks.
    """
    mock_pages = [{"title": "Page 1"}]
    mock_cosense_client.get_page_content.return_value = "Sample content for testing the synchronization."
    
    with patch("src.services.indexer.AsyncElasticsearch") as mock_es_class, \
         patch("src.services.indexer.IndexerService.get_sparse_embeddings") as mock_get_sparse:
        
        mock_es = mock_es_class.return_value
        mock_es.indices.exists = AsyncMock(return_value=True)
        mock_get_sparse.return_value = {"123": 0.5}
        mock_es.index = AsyncMock()
        
        service = IndexerService()
        await service.sync_pages(mock_pages, mock_cosense_client)
        
        mock_cosense_client.get_page_content.assert_called_once_with("Page 1")
        mock_get_sparse.assert_called()
        mock_es.index.assert_called()
        args, kwargs = mock_es.index.call_args
        assert kwargs["index"] == "cosense_pages"
        assert kwargs["document"]["metadata"]["title"] == "Page 1"

@pytest.mark.anyio
async def test_should_handle_sync_failure_gracefully(mock_cosense_client):
    """Test error handling during page synchronization.
    
    Arrange: Mock get_page_content to raise an exception.
    Act: Call sync_pages.
    Assert: Verify that the process continues and handles the error gracefully.
    """
    mock_pages = [{"title": "Failed Page"}]
    mock_cosense_client.get_page_content.side_effect = Exception("API Error")
    
    with patch("src.services.indexer.AsyncElasticsearch") as mock_es_class:
        mock_es = mock_es_class.return_value
        mock_es.indices.exists = AsyncMock(return_value=True)
        
        service = IndexerService()
        # Should not raise exception
        await service.sync_pages(mock_pages, mock_cosense_client)
        
        mock_cosense_client.get_page_content.assert_called_once_with("Failed Page")

@pytest.mark.anyio
async def test_should_close_elasticsearch_connection_successfully():
    """Test closing the service connection.
    
    Arrange: Mock AsyncElasticsearch.
    Act: Call close.
    Assert: Check that es.close is called once.
    """
    with patch("src.services.indexer.AsyncElasticsearch") as mock_es_class:
        mock_es = mock_es_class.return_value
        mock_es.close = AsyncMock()
        
        service = IndexerService()
        await service.close()
        
        mock_es.close.assert_called_once()
