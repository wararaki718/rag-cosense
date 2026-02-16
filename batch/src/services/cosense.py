import httpx
from typing import List, Dict, Any
from src.core.config import settings

class CosenseClient:
    """Client for interacting with the Cosense (Scrapbox) API."""

    def __init__(self):
        self.base_url = "https://scrapbox.io/api"
        self.headers = {"Cookie": f"connect.sid={settings.COSENSE_SID}"} if settings.COSENSE_SID else {}

    async def get_all_pages(self) -> List[Dict[str, Any]]:
        """Fetches all pages in the project."""
        url = f"{self.base_url}/pages/{settings.COSENSE_PROJECT_NAME}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("pages", [])

    async def get_page_content(self, page_title: str) -> str:
        """Fetches the full text content of a specific page."""
        url = f"{self.base_url}/pages/{settings.COSENSE_PROJECT_NAME}/{page_title}/text"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
