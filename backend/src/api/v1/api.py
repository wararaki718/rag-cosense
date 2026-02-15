from fastapi import APIRouter
from src.api.v1.endpoints import health, index

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(index.router, prefix="/index", tags=["index"])
