# app/routers/feedback.py
"""
Feedback API — stores user corrections for model improvement.
"""

from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import os

router = APIRouter()

FEEDBACK_PATH = "data/feedback.csv"

class FeedbackItem(BaseModel):
    description: str
    predicted_category: str
    corrected_category: str
    method: str
    confidence: float


@router.post("/")
def submit_feedback(item: FeedbackItem):
    """
    Receive feedback and store in feedback.csv
    """
    os.makedirs("data", exist_ok=True)
    new_entry = {
        "description": item.description,
        "predicted_category": item.predicted_category,
        "corrected_category": item.corrected_category,
        "method": item.method,
        "confidence": item.confidence
    }

    # Append to CSV
    if os.path.exists(FEEDBACK_PATH):
        df = pd.read_csv(FEEDBACK_PATH)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])
    df.to_csv(FEEDBACK_PATH, index=False)

    return {"message": "✅ Feedback recorded successfully", "data": new_entry}