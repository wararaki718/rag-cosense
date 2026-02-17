import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer
import logging
from typing import Any

logger = logging.getLogger(__name__)

class SpladeModel:
    tokenizer: Any
    model: Any
    device: torch.device

    def __init__(self, model_id: str = "aken12/splade-japanese-v3") -> None:
        self.model_id = model_id
        logger.info(f"Loading model {model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForMaskedLM.from_pretrained(model_id)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        logger.info(f"Model loaded on {self.device}")

    def encode(self, text: str) -> dict[str, float]:
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            logits = self.model(**inputs).logits
            
        # SPLADE representation: max(log1p(relu(logits))) over sequence dimension
        sparse_vector = torch.max(torch.log1p(torch.relu(logits)), dim=1).values[0]
        
        # Extract non-zero elements
        indices = torch.nonzero(sparse_vector).flatten()
        values = sparse_vector[indices]
        
        result = {}
        for idx, val in zip(indices.tolist(), values.tolist()):
            token = self.tokenizer.decode([idx]).strip()
            if token and val > 0.01:
                result[token] = float(val)
                
        return result
