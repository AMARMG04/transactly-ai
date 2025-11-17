# scripts/retrain.py
"""
Step 10 — Active Retraining Script for Transactly
Merges user feedback, regenerates embeddings, and retrains the classifier.
"""

import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from app.core.preprocessing import normalize_transaction
from app.core.classifier import train_classifier

# Paths
DATA_PATH = "data/processed/transactions.csv"
FEEDBACK_PATH = "data/feedback.csv"
NEW_DATA_PATH = "data/processed/transactions_retrained.csv"
EMB_PATH = "data/processed/embeddings.npy"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def merge_feedback():
    """Merge feedback corrections into the main dataset."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Main dataset not found. Run prepare_data.py first.")
    
    df_main = pd.read_csv(DATA_PATH)

    if os.path.exists(FEEDBACK_PATH):
        df_fb = pd.read_csv(FEEDBACK_PATH)
        if len(df_fb) > 0:
            print(f"🔹 Found {len(df_fb)} feedback samples. Merging...")

            # Normalize feedback texts
            df_fb["description"] = df_fb["description"].apply(normalize_transaction)
            df_fb.rename(columns={"corrected_category": "category"}, inplace=True)

            # Append to main dataset
            df_new = pd.concat(
                [df_main, df_fb[["description", "category"]]],
                ignore_index=True
            )

            # Drop duplicates
            df_new.drop_duplicates(subset=["description"], inplace=True)
            df_new.to_csv(NEW_DATA_PATH, index=False)
            print(f"✅ Merged dataset saved: {NEW_DATA_PATH} ({len(df_new)} rows)")
            return df_new
    else:
        print("⚠️ No feedback.csv found. Using original dataset.")
        return df_main


def regenerate_embeddings(df):
    """Generate fresh embeddings for the merged dataset."""
    print("🔹 Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("🔹 Normalizing and encoding texts...")
    df["normalized_text"] = df["description"].apply(normalize_transaction)
    embeddings = model.encode(df["normalized_text"].tolist(), batch_size=32, show_progress_bar=True)

    np.save(EMB_PATH, embeddings)
    print(f"✅ Saved new embeddings → {EMB_PATH}")
    return embeddings


def retrain_model():
    """Full retraining pipeline."""
    df = merge_feedback()
    embeddings = regenerate_embeddings(df)

    # Align shapes
    X = embeddings
    y = df["category"].astype(str).values

    # Retrain classifier
    print("🔹 Retraining Logistic Regression model...")
    from app.core.classifier import train_classifier
    model = train_classifier(X, y)

    print("🎯 Retraining complete. New model saved to app/models/classifier.pkl")


if __name__ == "__main__":
    retrain_model()