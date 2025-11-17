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

# Load embeddings/texts once for explainability
EMB_PATH = "data/processed/embeddings.npy"
TEXT_PATH = "data/processed/texts.npy"
embeddings_db = np.load(EMB_PATH) if os.path.exists(EMB_PATH) else None
texts_db = np.load(TEXT_PATH, allow_pickle=True) if os.path.exists(TEXT_PATH) else None


class TransactionInput(BaseModel):
    text: str


@router.post("/")
def classify_transaction(input: TransactionInput):
    """
    Classify a single transaction and return explainable output.
    """
    result = decide_category(input.text, embeddings_db, texts_db)

    # Clean explanation format: [(token, importance)] → list of dicts
    cleaned_explanation = []
    for token, score in result.get("explanation", []):
        cleaned_explanation.append({
            "token": str(token),
            "importance": float(score)
        })

    # Category scores (optional, but useful and clean)
    result_scores = result.get("scores")
    category_scores = None
    if result_scores:
        category_scores = {cat: float(prob) for cat, prob in result_scores.items()}

    return {
        "category": result["final_category"],
        "confidence": round(float(result["confidence"]), 3),
        "original_text": input.text,
        "explanation": cleaned_explanation,
        "category_scores": category_scores,
        "similar_examples": result.get("similar_examples", []),
        "method": result["method"]
    }