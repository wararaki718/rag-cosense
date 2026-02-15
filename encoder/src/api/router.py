from fastapi import APIRouter, Depends
from src.schemas.encode import EncodeRequest, EncodeResponse
from src.models.splade import SpladeModel
import functools

router = APIRouter()

@functools.lru_cache()
def get_model():
    return SpladeModel()

@router.post("/encode", response_model=EncodeResponse)
async def encode(request: EncodeRequest, model: SpladeModel = Depends(get_model)):
    sparse_values = model.encode(request.text)
    return EncodeResponse(sparse_values=sparse_values)

@router.get("/health")
async def health():
    return {"status": "healthy"}
