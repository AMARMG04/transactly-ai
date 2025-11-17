Transactly — Privacy-First Explainable AI for Smart Transaction Intelligence

GHCI 2025 Hackathon — Theme: Automated AI Transaction Categorisation

Transactly is a fully offline, explainable AI system that classifies financial transactions
like:

"AMZN Pmt #4827" → "Shopping"
"IRCTC Train Booking" → "Travel & Transport"

It uses a hybrid rule-based + ML approach, lightweight embeddings, and
transparent explanations — all without any external APIs or cloud-based inference.

⸻

Project Structure

This README matches your current repository layout exactly:

transactly-ai/
│
├── transactly-backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── classify.py
│   │   │   └── feedback.py
│   │   └── core/
│   │       ├── category_taxonomy.py
│   │       ├── preprocessing.py
│   │       ├── embeddings.py
│   │       ├── classifier.py
│   │       ├── rules.py
│   │       └── decision.py
│   ├── archived/
│   ├── data/
│   ├── scripts/
│   ├── Dockerfile
│   └── requirements.txt
│
├── transactly-frontend/    # Next.js frontend
│
├── .gitignore
└── README.md

(📸 Add screenshot of folder structure)

⸻

Core Features

Offline AI Engine

Runs 100% locally using:
	•	MiniLM-L6-v2 embeddings (~90MB)
	•	Logistic Regression classifier
	•	Rule-based overrides for deterministic merchants

Hybrid Categorisation System
	1.	Rule-based detection
	2.	ML-based prediction
	3.	Confidence scoring
	4.	Decision logic → final category

Explainability

Each prediction includes:
	•	method (rule / model)
	•	similarity-based reasoning
	•	top-K similar merchants with cosine scores

Feedback Loop

Users correct misclassified transactions → feedback saved → retraining improves accuracy.

Modern Architecture
	•	Backend: FastAPI
	•	Frontend: Next.js
	•	Storage: Local CSV
	•	Deployment: Docker-ready

⸻

Architecture Overview

(📸 Insert architecture diagram here — “AI Pipeline + Backend + Frontend Flow”)

⸻

Getting Started (Local Development)

1. Clone & Setup

git clone https://github.com/manojmg/transactly-ai.git
cd transactly-ai/transactly-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2. Generate Synthetic Data & Train Model

python -m scripts.prepare_data
python -m app.core.embeddings
python -m app.core.classifier

This produces:

data/processed/
├── embeddings.npy
├── processed.csv
└── classifier.pkl

3. Run FastAPI Backend

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

API docs:

http://127.0.0.1:8000/docs

(📸 Add screenshot of FastAPI Swagger UI)

⸻

Frontend (Next.js)

Inside transactly-frontend/:

npm install
npm run dev

Frontend runs on:

http://localhost:3000

It communicates with FastAPI using environment variables:

.env.local

NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

(📸 Add screenshots of classification UI, feedback UI, explanation UI)

⸻

Feedback & Retraining

Whenever a user corrects a category in the frontend:
	•	feedback is appended to:
transactly-backend/data/feedback.csv

To retrain with feedback:

python transactly-backend/scripts/retrain.py

This regenerates:
	•	embeddings
	•	classifier
	•	updated category mapping

⸻

🧠 Example API Output

{
  "description": "Starbucks Order",
  "final_category": "Food & Dining",
  "method": "model",
  "confidence": 0.87,
  "similar_examples": [
    ["Swiggy", 0.93],
    ["Zomato", 0.91],
    ["McDonalds", 0.89]
  ]
}

(📸 Add screenshot of raw API JSON in Swagger)

⸻

🐳 Docker (Optional)

From root:

cd transactly-backend
docker build -t transactly .
docker run -p 8000:8000 transactly


⸻

🔐 Privacy & Design Principles
	•	No internet calls
	•	No external AI APIs
	•	Local classification only
	•	Fully explainable decisions
	•	Deterministic fallbacks ensure trustworthiness

(📸 Insert “Privacy First” diagram)

⸻

Tech Stack

Backend
	•	Python 3.11
	•	FastAPI
	•	scikit-learn
	•	Sentence Transformers (MiniLM)

Frontend
	•	Next.js 14
	•	Tailwind CSS
	•	Axios

Storage
	•	Local CSV-based storage
	•	No cloud database required

⸻

Contributors

Name	Role
Manoj MG	AI Architecture • ML Pipeline • Backend (FastAPI) • Explainability
Mercy	Next.js Frontend • UI/UX • Documentation • Demo Assets


⸻

Summary

Transactly demonstrates a production-grade offline AI engine with:
	•	state-of-the-art embeddings
	•	interpretable logic
	•	retrainable ML
	•	clean modern web UI
	•	privacy-first design

