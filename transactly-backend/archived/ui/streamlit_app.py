# ui/streamlit_app.py
"""
Step 8b — Streamlit Frontend for Transactly
Provides an interactive demo for AI-based transaction categorization.
"""

import os
import streamlit as st
import requests
import pandas as pd

# API_URL = "http://127.0.0.1:8000/api/classify/"
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

API_URL = f"{BACKEND_URL.rstrip('/')}/api/classify/"
FEEDBACK_URL = f"{BACKEND_URL.rstrip('/')}/api/feedback/"

st.set_page_config(
    page_title="Transactly — Explainable Transaction Intelligence",
    page_icon="💳",
    layout="centered"
)

st.title("💳 Transactly — Privacy-First Explainable AI")
st.caption("Smart, Offline, and Transparent Transaction Categorisation")

# --- Input section ---
description = st.text_input(
    "Enter a transaction description",
    placeholder="e.g., IRCTC Train Booking #7382 or Swiggy Order 8392",
)

if st.button("🔍 Classify Transaction"):
    if not description.strip():
        st.warning("Please enter a transaction description.")
    else:
        with st.spinner("Analysing..."):
            try:
                response = requests.post(API_URL, json={"description": description})
                if response.status_code == 200:
                    result = response.json()
                    st.success("Classification complete ✅")

                    # --- Display main prediction ---
                    st.markdown("### 🧠 Prediction")
                    st.write(f"**Category:** {result['final_category']}")
                    st.write(f"**Method:** {result['method'].capitalize()}")
                    st.write(f"**Confidence:** {result['confidence']*100:.2f}%")
                    st.info(result.get("explanation", ""))
                    
                    # --- Feedback section ---
                    st.markdown("### 📝 Provide Feedback")
                    corrected_category = st.selectbox(
                        "If the prediction is wrong, select the correct category:",
                        [
                            "",
                            "Food & Dining",
                            "Shopping",
                            "Fuel",
                            "Travel & Transport",
                            "Utilities",
                            "Health & Fitness",
                            "Entertainment",
                            "Bills & Subscriptions",
                            "Groceries",
                            "Others"
                        ]
                    )
                    
                    if st.button("Submit Feedback"):
                        if corrected_category and corrected_category != result['final_category']:
                            feedback_payload = {
                                "description": result["description"],
                                "predicted_category": result["final_category"],
                                "corrected_category": corrected_category,
                                "method": result["method"],
                                "confidence": result["confidence"]
                            }
                    
                            try:
                                feedback_response = requests.post("http://127.0.0.1:8000/api/feedback/", json=feedback_payload)
                                if feedback_response.status_code == 200:
                                    st.success("✅ Feedback submitted! This will help Transactly improve over time.")
                                else:
                                    st.error(f"⚠️ Failed to submit feedback (Status: {feedback_response.status_code}).")
                            except Exception as e:
                                st.error(f"⚠️ Could not send feedback: {e}")
                        else:
                            st.info("Select a correct category that differs from the prediction before submitting.")

                    # --- Show similar examples if available ---
                    similar = result.get("similar_examples", [])
                    if similar:
                        st.markdown("### 🔍 Most Similar Transactions")
                        df = pd.DataFrame(similar, columns=["Example", "Similarity"])
                        df["Similarity"] = (df["Similarity"] * 100).round(2).astype(str) + "%"
                        st.dataframe(df, use_container_width=True)
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ Connection failed: {e}")

st.markdown("---")
st.caption("Built with ❤️ by Manoj & Mercy for GHCI 25 Hackathon")