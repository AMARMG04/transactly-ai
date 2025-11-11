# app/routers/classify.py
"""
Classification API endpoint — integrates Decision Logic.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from app.core.decision import decide_category
import numpy as np
import os

router = APIRouter()

# Load precomputed embeddings/texts for explainability
EMB_PATH = "data/processed/embeddings.npy"
TEXT_PATH = "data/processed/texts.npy"
embeddings_db = np.load(EMB_PATH) if os.path.exists(EMB_PATH) else None
texts_db = np.load(TEXT_PATH, allow_pickle=True) if os.path.exists(TEXT_PATH) else None

class TransactionInput(BaseModel):
    description: str


@router.post("/")
def classify_transaction(input: TransactionInput):
    """
    Classify a single transaction and return explainable output.
    """
    result = decide_category(input.description, embeddings_db, texts_db)
    return {
        "description": input.description,
        "final_category": result["final_category"],
        "method": result["method"],
        "confidence": round(result["confidence"], 3),
        "explanation": result.get("explanation"),
        "similar_examples": result.get("similar_examples", []),
    }