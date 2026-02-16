from fastapi import APIRouter, Depends
from typing import Annotated
from src.schemas.encode import EncodeRequest, EncodeResponse
from src.models.splade import SpladeModel
import functools

router = APIRouter()

@functools.lru_cache()
def get_model() -> SpladeModel:
    return SpladeModel()

@router.post("/encode", response_model=EncodeResponse)
async def encode(
    request: EncodeRequest, 
    model: Annotated[SpladeModel, Depends(get_model)]
) -> EncodeResponse:
    sparse_values = model.encode(request.text)
    return EncodeResponse(sparse_values=sparse_values)

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}
