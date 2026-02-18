from typing import List, Any
import httpx
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from elasticsearch import AsyncElasticsearch
from src.services.cosense import CosenseClient
from src.core.config import settings

class IndexerService:
    """Service for processing and indexing documents into Elasticsearch."""

    def __init__(self) -> None:
        self.es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    def _clean_text(self, text: str) -> str:
        """Removes HTML tags and other noise from the text."""
        # Remove HTML tags
        text = re.sub(r'<[^>]*>', '', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    async def get_sparse_embeddings(self, text: str) -> dict[str, Any]:
        """Generates a sparse embedding for the given text using the encoder service."""
        url = f"{settings.ENCODER_SERVICE_URL}/encode"
        payload = {"text": text}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=60.0)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            return data["sparse_values"]

    async def create_index_if_not_exists(self) -> None:
        """Creates the Elasticsearch index with proper mappings if it doesn't exist."""
        index_name = "cosense_pages"
        exists = await self.es.indices.exists(index=index_name)
        if not exists:
            await self.es.indices.create(
                index=index_name,
                body={
                    "mappings": {
                        "properties": {
                            "text": {"type": "text"},
                            "sparse_vector": {"type": "rank_features"},
                            "metadata": {
                                "properties": {
                                    "title": {"type": "keyword"},
                                    "chunk_id": {"type": "integer"},
                                    "project": {"type": "keyword"}
                                }
                            }
                        }
                    }
                }
            )

    async def sync_pages(self, pages: List[dict[str, Any]], cosense_client: CosenseClient) -> None:
        """Synchronizes a list of pages into Elasticsearch."""
        await self.create_index_if_not_exists()
        
        for page in pages:
            title = page["title"]
            try:
                content = await cosense_client.get_page_content(title)
                cleaned_content = self._clean_text(content)
                chunks = self.text_splitter.split_text(cleaned_content)
                
                for i, chunk in enumerate(chunks):
                    sparse_vector = await self.get_sparse_embeddings(chunk)
                    doc = {
                        "text": chunk,
                        "sparse_vector": sparse_vector,
                        "metadata": {
                            "title": title,
                            "chunk_id": i,
                            "project": settings.COSENSE_PROJECT_NAME
                        }
                    }
                    await self.es.index(index="cosense_pages", document=doc)
                print(f"Synced page: {title}")
            except Exception as e:
                print(f"Failed to sync page {title}: {str(e)}")

    async def close(self) -> None:
        """Closes the Elasticsearch connection."""
        await self.es.close()
