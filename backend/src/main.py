from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.api.v1.api import api_router
from src.core.config import settings
from src.schemas.chat import ChatErrorResponse

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

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
    return JSONResponse(
        status_code=500,
        content=ChatErrorResponse(
            status="error",
            message=f"Internal Server Error: {str(exc)}",
            code="INTERNAL_SERVER_ERROR"
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
