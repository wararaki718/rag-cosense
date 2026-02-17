import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.cosense import CosenseClient
from src.core.config import settings

@pytest.mark.anyio
async def test_should_fetch_all_pages_successfully():
    """Test fetching all pages from Cosense project.
    
    Arrange: Mock httpx.AsyncClient.get to return a list of pages.
    Act: Call get_all_pages.
    Assert: Check that the returned pages match expectations.
    """
    mock_pages = [{"id": "1", "title": "Page 1"}, {"id": "2", "title": "Page 2"}]
    
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"pages": mock_pages}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        client = CosenseClient()
        pages = await client.get_all_pages()
        
        assert len(pages) == 2
        assert pages[0]["title"] == "Page 1"
        assert pages[1]["title"] == "Page 2"

@pytest.mark.anyio
async def test_should_fetch_page_content_successfully():
    """Test fetching full text content of a specific page.
    
    Arrange: Mock httpx.AsyncClient.get to return page text.
    Act: Call get_page_content.
    Assert: Check that the returned text matches expectations.
    """
    expected_text = "This is the content of the page."
    
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = expected_text
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        client = CosenseClient()
        content = await client.get_page_content("Test Page")
        
        assert content == expected_text
