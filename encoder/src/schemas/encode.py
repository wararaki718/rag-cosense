from pydantic import BaseModel

class EncodeRequest(BaseModel):
    text: str

class EncodeResponse(BaseModel):
    sparse_values: dict[str, float]
