from fastapi import FastAPI
import logging
from src.api.router import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(title="SPLADE Embedding Service")
    app.include_router(router)
    return app

app = create_app()
