from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from src.api.v1.api import api_router
from src.core.config import settings
from src.schemas.chat import ChatErrorResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all.
    allow_credentials=False, # Credentials can't be *
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler to ensure all errors are JSON
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handles all unhandled exceptions and returns a standardized JSON error response."""
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ChatErrorResponse(
            status="error",
            message=f"Internal Server Error: {str(exc)}",
            code="INTERNAL_SERVER_ERROR"
        ).model_dump()
    )

# 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    logger.warning(f"404 Not Found: {request.url.path}")
    return JSONResponse(
        status_code=404,
        content=ChatErrorResponse(
            status="error",
            message=f"Path not found: {request.url.path}",
            code="NOT_FOUND"
        ).model_dump()
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
