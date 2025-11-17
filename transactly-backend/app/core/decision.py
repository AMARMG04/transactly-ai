"""
Step 7 – Decision Logic Layer
Combines rule-based and model-based reasoning for transaction categorisation.
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.core.rules import apply_rules
from app.core.preprocessing import normalize_transaction
from app.core.classifier import load_model, predict_category
from app.core.embeddings import load_model as load_embedder
from app.core.tokenizer import smart_tokenize
import re


# Soft semantic keyword → category override mapping
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

    # Finance
    "upi": "Financial Services",
    "imps": "Financial Services",
    "neft": "Financial Services",
    "rtgs": "Financial Services",
    "bank": "Financial Services",
}

CONF_THRESHOLD = 0.55


def explain_similarity(embedding, embeddings_db, texts_db, top_k=3):
    sims = cosine_similarity([embedding], embeddings_db)[0]
    idx = np.argsort(sims)[::-1][:top_k]
    return [(texts_db[i], float(sims[i])) for i in idx]


def rule_explanation(rule_pattern, description):
    matches = re.findall(rule_pattern, description, flags=re.IGNORECASE)

    extracted = []
    if matches:
        if isinstance(matches[0], tuple):
            extracted = [m for m in matches[0] if m]
        else:
            extracted = matches

    if not extracted:
        extracted = [rule_pattern.pattern]

    return [(kw, 1.0) for kw in extracted]


def model_explanation(description, emb_model, category_name):
    tokens = smart_tokenize(description)
    token_embs = emb_model.encode(tokens)
    category_emb = emb_model.encode([category_name])[0]

    sims = cosine_similarity(token_embs, [category_emb]).flatten()
    max_sim = sims.max() if sims.max() > 0 else 1.0
    sims = sims / max_sim

    ranked = sorted(zip(tokens, sims), key=lambda x: x[1], reverse=True)
    return [(tok, float(score)) for tok, score in ranked[:3]]


def decide_category(description: str, embeddings_db=None, texts_db=None):
    # 1️⃣ Rules
    rule_cat, rule_pattern = apply_rules(description)
    if rule_cat:
        return {
            "final_category": rule_cat,
            "method": "rule",
            "confidence": 1.0,
            "explanation": rule_explanation(rule_pattern, description)
        }

    # 2️⃣ Embed
    norm_text = normalize_transaction(description)
    emb_model = load_embedder()
    full_emb = emb_model.encode([norm_text])[0]

    # 3️⃣ Model prediction
    clf = load_model()
    pred, conf = predict_category(clf, full_emb)

    # 4️⃣ Soft semantic override
    tokens = smart_tokenize(description.lower())
    override_category = None

    for t in tokens:
        if t in SOFT_KEYWORDS:
            override_category = SOFT_KEYWORDS[t]
            break  # first strong match wins

    if override_category:
        pred = override_category
        conf = min(conf + 0.40, 1.0)

    # 5️⃣ Similarity examples
    top_similar = []
    if embeddings_db is not None and texts_db is not None:
        raw = explain_similarity(full_emb, embeddings_db, texts_db)

        seen = set()
        for text, score in raw:
            if text not in seen:
                top_similar.append((text, score))
                seen.add(text)

        top_similar = top_similar[:3]

    # 6️⃣ High confidence
    if conf >= CONF_THRESHOLD:
        explanation = model_explanation(description, emb_model, pred)
        return {
            "final_category": pred,
            "method": "model",
            "confidence": float(conf),
            "explanation": explanation,
            "similar_examples": top_similar
        }

    # 7️⃣ Low confidence
    return {
        "final_category": "Uncertain",
        "method": "low_confidence",
        "confidence": float(conf),
        "explanation": [],
        "similar_examples": top_similar
    }