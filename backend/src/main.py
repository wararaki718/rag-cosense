from fastapi import FastAPI
from src.api.v1.api import api_router
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint for basic verification.

    Returns:
        dict: A simple welcome message.
    """
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)
