import asyncio
import logging
import sys
from src.services.cosense import CosenseClient
from src.services.indexer import IndexerService
from src.core.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("batch")

async def main():
    """Main entry point for the batch synchronization job."""
    logger.info("Starting Cosense to Elasticsearch synchronization batch...")
    
    if not settings.COSENSE_PROJECT_NAME:
        logger.error("COSENSE_PROJECT_NAME is not set. Exiting.")
        sys.exit(1)

    cosense = CosenseClient()
    indexer = IndexerService()
    
    try:
        logger.info(f"Fetching pages from project: {settings.COSENSE_PROJECT_NAME}")
        pages = await cosense.get_all_pages()
        logger.info(f"Retrieved {len(pages)} pages.")
        
        await indexer.sync_pages(pages, cosense)
        logger.info("Batch synchronization finished successfully.")
        
    except Exception as e:
        logger.error(f"Batch synchronization failed: {e}")
        sys.exit(1)
    finally:
        await indexer.close()

if __name__ == "__main__":
    asyncio.run(main())
