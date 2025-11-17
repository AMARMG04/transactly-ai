"""
Step 7 – Decision Logic Layer
Combines rule-based and model-based reasoning for final transaction categorisation.
Implements confidence thresholds and explainability.
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.core.rules import apply_rules
from app.core.preprocessing import normalize_transaction
from app.core.classifier import load_model, predict_category
from app.core.embeddings import load_model as load_embedder
from app.core.tokenizer import smart_tokenize

# Soft semantic keyword → category boost mapping
SOFT_KEYWORDS = {
    # Food & Dining
    "restaurant": "Food & Dining",
    "dinner": "Food & Dining",
    "meal": "Food & Dining",
    "biryani": "Food & Dining",
    "cafe": "Food & Dining",
    "hotel": "Food & Dining",
    "breakfast": "Food & Dining",
    "lunch": "Food & Dining",

    # Groceries
    "grocery": "Groceries",
    "groceries": "Groceries",
    "supermarket": "Groceries",
    "mart": "Groceries",
    "kirana": "Groceries",

    # Shopping
    "shopping": "Shopping",
    "apparel": "Shopping",
    "fashion": "Shopping",
    "clothing": "Shopping",

    # Travel
    "ride": "Travel & Transport",
    "auto": "Travel & Transport",
    "bus": "Travel & Transport",
    "flight": "Travel & Transport",
    "train": "Travel & Transport",
    "cab": "Travel & Transport",

    # Entertainment
    "movie": "Entertainment",
    "cinema": "Entertainment",
    "theatre": "Entertainment",
    "ticket": "Entertainment",

    # Utilities
    "bill": "Utilities",
    "recharge": "Utilities",
    "electricity": "Utilities",
    "water": "Utilities",

    # Health
    "pharmacy": "Health & Fitness",
    "clinic": "Health & Fitness",
    "hospital": "Health & Fitness",

    # Finance (backup)
    "upi": "Financial Services",
    "imps": "Financial Services",
    "neft": "Financial Services",
    "rtgs": "Financial Services",
    "bank": "Financial Services",
}

# Confidence threshold for model acceptance
CONF_THRESHOLD = 0.55


def explain_similarity(embedding, embeddings_db, texts_db, top_k=3):
    """
    Find top-k most similar transactions in the dataset.
    Returns list of (text, similarity_score).
    """
    sims = cosine_similarity([embedding], embeddings_db)[0]
    top_idx = np.argsort(sims)[::-1][:top_k]
    return [(texts_db[i], float(sims[i])) for i in top_idx]


def rule_explanation(description, rule_pattern):
    """
    Token-level explanation for rule-based classification.
    Highlights only the tokens matched from the rule pattern.
    """
    pattern_str = str(rule_pattern) if rule_pattern is not None else ""
    tokens = smart_tokenize(description)
    key_tokens = [t.lower() for t in smart_tokenize(pattern_str)]

    explanation = []
    for token in tokens:
        if token.lower() in key_tokens:
            explanation.append((token, 1.0))   # strong highlight
        else:
            explanation.append((token, 0.1))   # muted

    return explanation


def model_explanation(description, emb_model, category_embedding):
    """
    Token-level explanation using cosine similarity between each token's embedding
    and the full description/category embedding.
    """
    tokens = smart_tokenize(description)

    # Encode each token individually
    token_embs = emb_model.encode(tokens)

    # Similarity of each token to the main embedding
    sims = cosine_similarity(token_embs, [category_embedding]).flatten()

    max_sim = sims.max() if sims.max() > 0 else 1.0
    sims = sims / max_sim  # normalize to 0–1

    explanation = [(tok, float(imp)) for tok, imp in zip(tokens, sims)]
    return explanation


def low_confidence_explanation(description):
    """
    Token-level fallback when confidence is low.
    Everything is muted (no strong signal).
    """
    return [(t, 0.1) for t in smart_tokenize(description)]


def decide_category(description: str, embeddings_db=None, texts_db=None):
    """
    Main decision logic entrypoint.
    Returns a structured dict containing the final category,
    method, confidence, and token-level explanation.
    """

    # ---------------------------
    # 1️⃣ APPLY RULES
    # ---------------------------
    rule_cat, rule_pattern = apply_rules(description)

    if rule_cat:
        return {
            "final_category": rule_cat,
            "method": "rule",
            "confidence": 1.0,
            "explanation": rule_explanation(description, rule_pattern)
        }

    # ---------------------------
    # 2️⃣ NORMALIZE + EMBED
    # ---------------------------
    norm_text = normalize_transaction(description)

    emb_model = load_embedder()
    full_emb = emb_model.encode([norm_text])[0]

    # ---------------------------
    # 3️⃣ MODEL INFERENCE
    # ---------------------------
    clf = load_model()
    pred, conf = predict_category(clf, full_emb)
    # --------------------------------------
    # Soft Semantic Boost
    # --------------------------------------
    tokens = smart_tokenize(description.lower())
    boost = 0.0
    
    for token in tokens:
        if token in SOFT_KEYWORDS and SOFT_KEYWORDS[token] == pred:
            boost += 0.10      # soft boost per matched keyword
    
    # limit max boost
    boost = min(boost, 0.25)   # prevent overconfidence

    # ---------------------------
    # 4️⃣ SIMILARITY EXAMPLES
    # ---------------------------
    top_similar = []
    if embeddings_db is not None and texts_db is not None:
        top_similar = explain_similarity(full_emb, embeddings_db, texts_db)

    # ---------------------------
    # 5️⃣ MODEL ACCEPTED (High confidence)
    # ---------------------------
    conf = float(conf + boost)
    if conf > 1.0:
        conf = 1.0
    if conf >= CONF_THRESHOLD:
        explanation = model_explanation(description, emb_model, full_emb)

        return {
            "final_category": pred,
            "method": "model",
            "confidence": float(conf),
            "explanation": explanation,
            "similar_examples": top_similar
        }

    # ---------------------------
    # 6️⃣ LOW CONFIDENCE
    # ---------------------------
    return {
        "final_category": "Uncertain",
        "method": "low_confidence",
        "confidence": float(conf),
        "explanation": low_confidence_explanation(description),
        "similar_examples": top_similar
    }


# ---------------------------
# 🧪 DEMO
# ---------------------------
if __name__ == "__main__":
    import os

    emb_path = "data/processed/embeddings.npy"
    text_path = "data/processed/texts.npy"

    embeddings_db = np.load(emb_path) if os.path.exists(emb_path) else None
    texts_db = np.load(text_path, allow_pickle=True) if os.path.exists(text_path) else None

    samples = [
        "IRCTC Train Booking #7845",
        "Swiggy Order 2398",
        "Netflix Monthly Subscription",
        "Payment to Reliance Fresh Supermarket",
        "Fuel charge IndianOil station",
        "Unknown merchant 1234"
    ]

    for s in samples:
        res = decide_category(s, embeddings_db, texts_db)
        print("\nTransaction:", s)
        for k, v in res.items():
            print(f"  {k}: {v}")