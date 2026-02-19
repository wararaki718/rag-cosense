from fastapi import APIRouter, Depends
from src.schemas.chat import ChatRequest, ChatSuccessResponse, ChatData
from src.services.chat import ChatService
import functools

router = APIRouter()

@functools.lru_cache()
def get_chat_service() -> ChatService:
    return ChatService()

@router.post("", response_model=ChatSuccessResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
) -> ChatSuccessResponse:
    """Chat endpoint to process user queries via RAG."""
    answer, sources = await chat_service.process_query(
        query=request.query,
        context_history=request.context_history
    )
    return ChatSuccessResponse(
        data=ChatData(
            answer=answer,
            sources=sources
        )
    )
