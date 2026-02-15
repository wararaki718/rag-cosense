from fastapi import APIRouter, BackgroundTasks
from src.services.cosense import CosenseClient
from src.services.indexer import IndexerService
from src.core.config import settings

router = APIRouter()

async def run_sync():
    """Background task to sync all Cosense pages."""
    cosense = CosenseClient()
    indexer = IndexerService()
    try:
        pages = await cosense.get_all_pages()
        await indexer.sync_pages(pages, cosense)
    finally:
        await indexer.close()

@router.post("/sync")
async def sync_cosense_data(background_tasks: BackgroundTasks):
    """Initiates an asynchronous synchronization of Cosense data to Elasticsearch.
    
    Returns:
        dict: Confirmation message that the task has started.
    """
    background_tasks.add_task(run_sync)
    return {"message": "Sync task started in background."}
