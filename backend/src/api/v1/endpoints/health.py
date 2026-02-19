from typing import Any
import httpx
from fastapi import APIRouter
from elasticsearch import AsyncElasticsearch
from src.core.config import settings

router = APIRouter()

@router.get("")
async def health_check() -> dict[str, Any]:
    """Check the health of the application and its downstream services.

    Performs connectivity tests for Elasticsearch and Ollama.

    Returns:
        dict: A dictionary containing the status of each service.
    """
    health_status: dict[str, Any] = {
        "status": "ok",
        "services": {
            "elasticsearch": "unknown",
            "ollama": "unknown",
            "encoder": "unknown"
        }
    }

    # Check Elasticsearch
    try:
        es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
        if await es.ping():
            health_status["services"]["elasticsearch"] = "connected"
        else:
            health_status["services"]["elasticsearch"] = "disconnected"
        await es.close()
    except Exception as e:
        health_status["services"]["elasticsearch"] = f"error: {str(e)}"

    # Check Ollama
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                health_status["services"]["ollama"] = "connected"
            else:
                health_status["services"]["ollama"] = f"unexpected status code: {response.status_code}"
    except Exception as e:
        health_status["services"]["ollama"] = f"error: {str(e)}"

    # Check Encoder
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.ENCODER_SERVICE_URL}/health")
            if response.status_code == 200:
                health_status["services"]["encoder"] = "connected"
            else:
                health_status["services"]["encoder"] = f"unexpected status code: {response.status_code}"
    except Exception as e:
        health_status["services"]["encoder"] = f"error: {str(e)}"

    return health_status
