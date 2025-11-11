# app/core/embeddings.py
"""
Step 4 - Feature Extraction
Generates text embeddings for transaction descriptions using all-MiniLM-L6-v2.
"""

import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from app.core.preprocessing import normalize_transaction


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_DIM = 384
EMBED_SAVE_PATH = "data/processed/embeddings.npy"
TEXT_SAVE_PATH = "data/processed/texts.npy"


def load_model():
    """Load MiniLM model once."""
    print(f"🔹 Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    return model


def generate_embeddings(csv_path: str, model=None):
    """
    Generate embeddings for transaction descriptions.
    Returns: np.ndarray of shape (n_samples, EMBED_DIM)
    """
    if model is None:
        model = load_model()

    df = pd.read_csv(csv_path)
    if "description" not in df.columns:
        raise ValueError("Input CSV must contain a 'description' column")

    # Normalize merchant text before embedding
    print("🔹 Normalizing descriptions...")
    df["normalized_text"] = df["description"].apply(normalize_transaction)

    print("🔹 Generating embeddings...")
    embeddings = model.encode(df["normalized_text"].tolist(), batch_size=32, show_progress_bar=True)

    os.makedirs(os.path.dirname(EMBED_SAVE_PATH), exist_ok=True)
    np.save(EMBED_SAVE_PATH, embeddings)
    np.save(TEXT_SAVE_PATH, df["normalized_text"].to_numpy())

    print(f"✅ Saved embeddings → {EMBED_SAVE_PATH}")
    print(f"✅ Shape: {embeddings.shape}")
    return embeddings, df


if __name__ == "__main__":
    # quick demo: run directly to generate embeddings for processed dataset
    csv_path = "data/processed/transactions.csv"
    if os.path.exists(csv_path):
        model = load_model()
        generate_embeddings(csv_path, model)
    else:
        print("⚠️ Dataset not found at data/processed/transactions.csv. Run prepare_data.py first.")