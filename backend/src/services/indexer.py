from typing import List
import httpx
from langchain_text_splitters import RecursiveCharacterTextSplitter
from elasticsearch import AsyncElasticsearch
from src.core.config import settings

class IndexerService:
    """Service for processing and indexing documents into Elasticsearch."""

    def __init__(self):
        self.es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    async def get_sparse_embeddings(self, text: str) -> dict:
        """Generates a sparse embedding for the given text using the encoder service.
        
        Args:
            text (str): The text to embed.
            
        Returns:
            dict: The generated sparse embedding (token-weight mapping).
        """
        url = f"{settings.ENCODER_SERVICE_URL}/encode"
        payload = {"text": text}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()["sparse_values"]

    async def create_index_if_not_exists(self):
        """Creates the Elasticsearch index with proper mappings if it doesn't exist."""
        index_name = "cosense_pages"
        exists = await self.es.indices.exists(index=index_name)
        if not exists:
            # Note: We use rank_features for SPLADE sparse vectors.
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

    async def sync_pages(self, pages: List[dict], cosense_client):
        """Synchronizes a list of pages into Elasticsearch.
        
        Args:
            pages (List[dict]): Metadata of pages to sync.
            cosense_client: Instance of CosenseClient to fetch content.
        """
        await self.create_index_if_not_exists()
        
        for page in pages:
            title = page["title"]
            try:
                content = await cosense_client.get_page_content(title)
                chunks = self.text_splitter.split_text(content)
                
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
            except Exception as e:
                # Log or handle individual page failures gracefully
                print(f"Failed to sync page {title}: {str(e)}")

    async def close(self):
        """Closes the Elasticsearch connection."""
        await self.es.close()
