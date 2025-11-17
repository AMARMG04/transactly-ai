# app/core/classifier.py
"""
Step 5 – Classifier Training for Transactly
Trains a Logistic Regression model on sentence-transformer embeddings.
Provides train(), evaluate(), and predict() utilities.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

MODEL_PATH = "app/models/classifier.pkl"

def load_data(embeddings_path: str, csv_path: str):
    """Load embeddings (X) and categories (y)."""
    X = np.load(embeddings_path)
    df = pd.read_csv(csv_path)
    if "category" not in df.columns:
        raise ValueError("Dataset must contain a 'category' column")
    y = df["category"].astype(str).values
    return X, y


def train_classifier(X, y):
    """Train Logistic Regression classifier."""
    print("🔹 Splitting data (80 % train / 20 % test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("🔹 Training Logistic Regression...")
    clf = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        multi_class="multinomial",
        solver="lbfgs"
    )
    clf.fit(X_train, y_train)

    print("🔹 Evaluating...")
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")
    print(f"✅ Accuracy: {acc:.4f}")
    print(f"✅ Macro F1: {f1:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Save trained model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"✅ Model saved → {MODEL_PATH}")

    return clf


def load_model(model_path: str = MODEL_PATH):
    """Load trained Logistic Regression model."""
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model not found. Train it first.")
    return joblib.load(model_path)


def predict_category(model, text_embedding):
    """Predict category + confidence for one embedding vector."""
    probs = model.predict_proba([text_embedding])[0]
    idx = np.argmax(probs)
    return model.classes_[idx], float(probs[idx])


if __name__ == "__main__":
    # Demo: Train model using processed embeddings
    EMB_PATH = "data/processed/embeddings.npy"
    CSV_PATH = "data/processed/transactions.csv"

    if os.path.exists(EMB_PATH) and os.path.exists(CSV_PATH):
        X, y = load_data(EMB_PATH, CSV_PATH)
        model = train_classifier(X, y)
    else:
        print("⚠️ Missing embeddings or dataset. Run embeddings step first.")