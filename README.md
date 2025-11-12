# 💳 Transactly — Privacy-First Explainable AI for Smart Transaction Intelligence

> **Built for GHCI 2025 Hackathon — Theme: Automated AI Transaction Categorisation**

Transactly is a **fully offline, explainable AI engine** that automatically categorises financial transactions like
`"AMZN Pmt #4827" → "Shopping"`
using a hybrid of **rule-based precision** and **lightweight machine learning**.

It is designed to be **privacy-first**, **interpretable**, and **deployable offline**, combining text-normalisation, embeddings, logistic regression, and explainability.

-----

## 🌟 Key Features

  * 🧠 **Offline AI Engine** — No external APIs, runs fully local.
  * 🪶 **Lightweight Embeddings** — Uses `all-MiniLM-L6-v2` (\~90 MB).
  * ⚙️ **Hybrid Categorisation** — Rules + ML + Confidence logic.
  * 🔍 **Explainability Layer** — Shows top-3 similar merchants.
  * 🔁 **Feedback-Driven Learning** — User corrections retrain model.
  * 🧩 **Modular Architecture** — Python + FastAPI + Streamlit.
  * 🐳 **Docker-ready** — Single-command portable demo.

-----

## 🏗️ Project Architecture

```text
transactly-ai/
│
├── app/                # FastAPI backend
│   ├── main.py           # API entrypoint
│   ├── routers/
│   │   ├── classify.py   # /api/classify endpoint
│   │   └── feedback.py   # /api/feedback endpoint
│   └── core/
│       ├── category_taxonomy.py
│       ├── preprocessing.py
│       ├── embeddings.py
│       ├── classifier.py
│       ├── rules.py
│       └── decision.py
│
├── scripts/
│   ├── prepare_data.py   # Synthetic data generator
│   └── retrain.py        # Active learning retrain loop
│
├── data/
│   ├── processed/        # CSVs, embeddings, etc.
│   └── feedback.csv      # User corrections
│
├── ui/
│   └── streamlit_app.py  # Streamlit demo dashboard
│
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

-----

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **ML** | scikit-learn (LogisticRegression), Sentence-Transformers |
| **API** | FastAPI |
| **Frontend** | Streamlit |
| **Storage** | CSV (local) |
| **Explainability** | Cosine similarity of embeddings |
| **Deployment** | Render (backend) + Streamlit Cloud (frontend) |

-----

## 🚀 Getting Started (Local Development)

### 1️⃣ Clone & setup environment

```bash
git clone https://github.com/manojmg/transactly-ai.git
cd transactly-ai
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 2️⃣ Prepare data & train model

```bash
python -m scripts.prepare_data
python -m app.core.embeddings
python -m app.core.classifier
```

### 3️⃣ Run FastAPI backend

```bash
uvicorn app.main:app --reload
```

→ Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4️⃣ Run Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

→ Open http://localhost:8501

### 🔁 Feedback & Retraining

Users can submit corrections through the Streamlit interface.
Feedback is logged into `data/feedback.csv`.

To merge feedback and retrain:

```bash
python scripts/retrain.py
```

This regenerates embeddings and updates `app/models/classifier.pkl`.

## 🌐 Deployment

### 🧩 Backend (FastAPI on Render)

1.  Push repo to GitHub.
2.  Create a new **Render Web Service**.
      * **Build command**: `pip install -r requirements.txt`
      * **Start command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3.  Wait for deploy → you’ll get a public URL like
    `https://transactly-backend.onrender.com`

### 💻 Frontend (Streamlit Cloud)

1.  Go to [https://share.streamlit.io](https://share.streamlit.io)
2.  Choose this repo.
3.  Set **Main file path**: `ui/streamlit_app.py`
4.  Add an environment variable (TOML syntax):
    `BACKEND_URL = "https://transactly-backend.onrender.com"`
5.  Click **Deploy** → you’ll get
    `https://transactly-ui.streamlit.app`

✅ Your app now runs end-to-end online and locally.

### 🌐 Environment-Aware Configuration

`ui/streamlit_app.py` automatically switches environments:

```python
import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
API_URL = f"{BACKEND_URL}/api/classify/"
FEEDBACK_URL = f"{BACKEND_URL}/api/feedback/"
```

So it “just works”:

  * **Locally** → connects to `localhost:8000`
  * **On Cloud** → connects to Render backend via env var

### 🐳 Docker (optional offline bundle)

Build & run both backend + frontend together:

```bash
docker build -t transactly .
docker run -p 8000:8000 -p 8501:8501 transactly
```

Then open:

  * **FastAPI** → http://localhost:8000/docs
  * **Streamlit** → http://localhost:8501

-----

## 🧠 Example Inference

```text
Input:   "IRCTC Train Booking #7845"
Output:  Travel & Transport  (rule-based, 100%)

Input:   "AMZN Pmt #8392"
Output:  Shopping  (model-based, 91%)

Input:   "Netflix Subscription"
Output:  Entertainment  (rule-based, 100%)
```

-----

## 🧩 Explainability Layer

Each prediction includes:

  * **Method**: `rule` or `model`
  * **Confidence**: probability from classifier
  * **Explanation**: matched rule or similar transactions

Example JSON response:

```json
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
```

-----

## 🧾 Notes

  * Render Free Tier may “sleep” after 15 min inactivity (cold start delay ≈ 10 s).
  * All AI runs locally – no external API calls or internet inference.
  * Feedback is stored locally (`feedback.csv`), retrainable anytime.

-----

## 🧩 Contributors

| Name | Role |
|---|---|
| Manoj MG | Core AI Architecture • Backend (FastAPI) • Model & Explainability |
| Mercy | UI & Streamlit Design • Documentation • Pitch Slides & Demo Video |
