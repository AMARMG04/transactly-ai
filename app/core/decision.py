# app/core/decision.py
"""
Step 7 – Decision Logic Layer
Combines rule-based and model-based reasoning for final transaction categorisation.
Implements confidence thresholds and explainability.
"""

import numpy as np
from app.core.rules import apply_rules
from app.core.preprocessing import normalize_transaction
from app.core.classifier import load_model, predict_category
from app.core.embeddings import load_model as load_embedder
from sklearn.metrics.pairwise import cosine_similarity

# Confidence threshold for model acceptance
CONF_THRESHOLD = 0.75


def explain_similarity(embedding, embeddings_db, texts_db, top_k=3):
    """
    Find top-k most similar transactions in the existing dataset.
    Returns list of (text, similarity_score).
    """
    sims = cosine_similarity([embedding], embeddings_db)[0]
    top_idx = np.argsort(sims)[::-1][:top_k]
    return [(texts_db[i], float(sims[i])) for i in top_idx]


def decide_category(description: str, embeddings_db=None, texts_db=None):
    """
    End-to-end decision logic for a single transaction description.
    Returns a structured dict containing the final category, method, confidence, and explanation.
    """

    # 1️⃣ Apply preprocessing + rules
    rule_cat, rule_pattern = apply_rules(description)
    if rule_cat:
        return {
            "final_category": rule_cat,
            "method": "rule",
            "confidence": 1.0,
            "explanation": f"Matched rule pattern: {rule_pattern}"
        }

    # 2️⃣ Normalize & embed
    norm_text = normalize_transaction(description)
    emb_model = load_embedder()
    emb = emb_model.encode([norm_text])[0]

    # 3️⃣ Model inference
    clf = load_model()
    pred, conf = predict_category(clf, emb)

    # 4️⃣ Explainability (optional)
    top_similar = []
    if embeddings_db is not None and texts_db is not None:
        top_similar = explain_similarity(emb, embeddings_db, texts_db)

    # 5️⃣ Decision logic
    if conf >= CONF_THRESHOLD:
        return {
            "final_category": pred,
            "method": "model",
            "confidence": conf,
            "explanation": f"Predicted by model with confidence {conf:.2f}",
            "similar_examples": top_similar
        }
    else:
        return {
            "final_category": "Uncertain",
            "method": "low_confidence",
            "confidence": conf,
            "explanation": "Below confidence threshold; needs user feedback",
            "similar_examples": top_similar
        }


# 🧪 Demo
if __name__ == "__main__":
    import numpy as np
    import os

    # Load embeddings for explainability (optional)
    emb_path = "data/processed/embeddings.npy"
    text_path = "data/processed/texts.npy"

    embeddings_db = np.load(emb_path) if os.path.exists(emb_path) else None
    texts_db = np.load(text_path, allow_pickle=True) if os.path.exists(text_path) else None

    samples = [
        "IRCTC Train Booking #7845",
        "Swiggy Food Order #2398",
        "Netflix Monthly Subscription",
        "Payment to Reliance Fresh Supermarket",
        "Unknown merchant 1234",
        "Fuel charge IndianOil station"
    ]

    for s in samples:
        result = decide_category(s, embeddings_db, texts_db)
        print("\nTransaction:", s)
        for k, v in result.items():
            print(f"  {k}: {v}")