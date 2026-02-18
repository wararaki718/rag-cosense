from pydantic import BaseModel
from typing import List, Optional, Literal

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class Source(BaseModel):
    title: str
    url: str
    score: float

class ChatRequest(BaseModel):
    query: str
    context_history: Optional[List[Message]] = None

class ChatData(BaseModel):
    answer: str
    sources: List[Source]

class ChatSuccessResponse(BaseModel):
    status: Literal["success"] = "success"
    data: ChatData

class ChatErrorResponse(BaseModel):
    status: Literal["error"] = "error"
    message: str
    code: str
