# app/main.py
"""
Step 8a — FastAPI Backend Entry Point
Exposes the Transactly AI engine via API routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import classify,feedback



app = FastAPI(
    title="Transactly AI API",
    description="Privacy-First Explainable AI for Smart Transaction Intelligence",
    version="1.0.0",
)

# Allow frontend (Streamlit or localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(classify.router, prefix="/api/classify", tags=["Classification"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])

@app.get("/")
def root():
    return {"message": "Welcome to Transactly AI API 🚀"}