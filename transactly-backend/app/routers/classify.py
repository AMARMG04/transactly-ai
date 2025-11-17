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
    text: str


@router.post("/")
def classify_transaction(input: TransactionInput):
    """
    Classify a single transaction and return explainable output.
    """
    result = decide_category(input.text, embeddings_db, texts_db)

    explanation = result.get("explanation", [])
    scores = result.get("scores", {})
    cleaned_explanation = []
    
    raw_explanation = result.get("explanation", [])
    
    for item in raw_explanation:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            # correct format → (token, score)
            token, score = item
            cleaned_explanation.append({
                "token": str(token),
                "importance": float(score)
            })
        else:
            # fallback → treat single token with neutral importance
            cleaned_explanation.append({
                "token": str(item),
                "importance": 0.1   # default small highlight
            })
    # Fallback scores if missing
    if not scores:
        scores = {
            result["final_category"]: result["confidence"],
            "Other": 1 - result["confidence"]
        }

    return {
        "category": result["final_category"],
        "confidence": round(result["confidence"], 3),
        "original_text": input.text,
        "explanation": cleaned_explanation,
        "category_scores": {
            cat: float(prob) for cat, prob in scores.items()
        },
        "similar_examples": result.get("similar_examples", []),
        "method": result["method"]
    }