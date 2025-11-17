# Transactly — Privacy-First Explainable AI for Smart Transaction Intelligence

**GHCI 2025 Hackathon — Theme: Automated AI Transaction Categorisation**

**Transactly** is a fully offline, explainable AI system that classifies financial transactions without any external APIs or cloud-based inference.

> **Example:**
> * "AMZN Pmt #4827" → **"Shopping"**
> * "IRCTC Train Booking" → **"Travel & Transport"**

It uses a hybrid rule-based + ML approach, lightweight embeddings, and transparent explanations.

---

## 📂 Project Structure

This matches the current repository layout exactly:

```text
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
````

*(Replace with actual screenshot path)*

-----

## 🚀 Core Features

### 🧠 Offline AI Engine

Runs **100% locally** using:

  * MiniLM-L6-v2 embeddings (\~90MB)
  * Logistic Regression classifier
  * Rule-based overrides for deterministic merchants

### ⚖️ Hybrid Categorisation System

1.  Rule-based detection
2.  ML-based prediction
3.  Confidence scoring
4.  Decision logic → **Final Category**

### 🔍 Explainability

Each prediction includes:

  * **Method** (rule / model)
  * **Similarity-based reasoning**
  * **Top-K similar merchants** with cosine scores

### 🔄 Feedback Loop

Users correct misclassified transactions → feedback is saved → retraining improves accuracy.

### 🏗️ Modern Architecture

  * **Backend:** FastAPI
  * **Frontend:** Next.js
  * **Storage:** Local CSV
  * **Deployment:** Docker-ready

-----

## 🏗️ Architecture Overview

-----

## ⚡ Getting Started (Local Development)

### 1\. Clone & Setup

```bash
git clone [https://github.com/manojmg/transactly-ai.git](https://github.com/manojmg/transactly-ai.git)
cd transactly-ai/transactly-backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2\. Generate Synthetic Data & Train Model

```bash
python -m scripts.prepare_data
python -m app.core.embeddings
python -m app.core.classifier
```

**This produces:**

  * `data/processed/embeddings.npy`
  * `data/processed/processed.csv`
  * `data/processed/classifier.pkl`

### 3\. Run FastAPI Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**API Docs:** Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see the Swagger UI.

-----

## 💻 Frontend (Next.js)

Navigate to the frontend directory:

```bash
cd transactly-frontend/
npm install
npm run dev
```

**Frontend runs on:** [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000)

It communicates with FastAPI using environment variables defined in `.env.local`:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

-----

## 🔄 Feedback & Retraining

Whenever a user corrects a category in the frontend:

1.  Feedback is appended to `transactly-backend/data/feedback.csv`.

**To retrain with feedback:**

```bash
python transactly-backend/scripts/retrain.py
```

**This regenerates:**

  * Embeddings
  * Classifier model
  * Updated category mapping

-----

## 🧠 Example API Output

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

## 🐳 Docker (Optional)

From the root directory:

```bash
cd transactly-backend
docker build -t transactly .
docker run -p 8000:8000 transactly
```

-----

## 🔐 Privacy & Design Principles

  * **No internet calls:** Data never leaves the machine.
  * **No external AI APIs:** No dependency on OpenAI or Gemini.
  * **Local classification only:** Fast and private.
  * **Fully explainable decisions:** Users know *why* a category was chosen.
  * **Deterministic fallbacks:** Ensures trustworthiness for known merchants.

-----

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python 3.11, FastAPI, scikit-learn, Sentence Transformers (MiniLM) |
| **Frontend** | Next.js 14, Tailwind CSS, Axios |
| **Storage** | Local CSV-based storage (No cloud database required) |

-----

## 👥 Contributors

| Name | Role |
| :--- | :--- |
| **Manoj MG** | AI Architecture • ML Pipeline • Backend (FastAPI) • Explainability |
| **Mercy** | Next.js Frontend • UI/UX • Documentation • Demo Assets |

-----

## 📝 Summary

Transactly demonstrates a production-grade offline AI engine with:

  * ✅ State-of-the-art embeddings
  * ✅ Interpretable logic
  * ✅ Retrainable ML
  * ✅ Clean modern web UI
  * ✅ Privacy-first design

<!-- end list -->

```

### Next Step
Would you like me to create the **requirements.txt** file or the **Dockerfile** content based on the tech stack mentioned in this README?
```Here is the clean, formatted Markdown source code for your `README.md`.

You can copy the code block below directly and paste it into your `README.md` file.

````markdown
# Transactly — Privacy-First Explainable AI for Smart Transaction Intelligence

**GHCI 2025 Hackathon — Theme: Automated AI Transaction Categorisation**

**Transactly** is a fully offline, explainable AI system that classifies financial transactions without any external APIs or cloud-based inference.

> **Example:**
> * "AMZN Pmt #4827" → **"Shopping"**
> * "IRCTC Train Booking" → **"Travel & Transport"**

It uses a hybrid rule-based + ML approach, lightweight embeddings, and transparent explanations.

---

## 📂 Project Structure

This matches the current repository layout exactly:

```text
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
````

*(Replace with actual screenshot path)*

-----

## 🚀 Core Features

### 🧠 Offline AI Engine

Runs **100% locally** using:

  * MiniLM-L6-v2 embeddings (\~90MB)
  * Logistic Regression classifier
  * Rule-based overrides for deterministic merchants

### ⚖️ Hybrid Categorisation System

1.  Rule-based detection
2.  ML-based prediction
3.  Confidence scoring
4.  Decision logic → **Final Category**

### 🔍 Explainability

Each prediction includes:

  * **Method** (rule / model)
  * **Similarity-based reasoning**
  * **Top-K similar merchants** with cosine scores

### 🔄 Feedback Loop

Users correct misclassified transactions → feedback is saved → retraining improves accuracy.

### 🏗️ Modern Architecture

  * **Backend:** FastAPI
  * **Frontend:** Next.js
  * **Storage:** Local CSV
  * **Deployment:** Docker-ready

-----

## 🏗️ Architecture Overview

-----

## ⚡ Getting Started (Local Development)

### 1\. Clone & Setup

```bash
git clone [https://github.com/manojmg/transactly-ai.git](https://github.com/manojmg/transactly-ai.git)
cd transactly-ai/transactly-backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2\. Generate Synthetic Data & Train Model

```bash
python -m scripts.prepare_data
python -m app.core.embeddings
python -m app.core.classifier
```

**This produces:**

  * `data/processed/embeddings.npy`
  * `data/processed/processed.csv`
  * `data/processed/classifier.pkl`

### 3\. Run FastAPI Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**API Docs:** Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see the Swagger UI.

-----

## 💻 Frontend (Next.js)

Navigate to the frontend directory:

```bash
cd transactly-frontend/
npm install
npm run dev
```

**Frontend runs on:** [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000)

It communicates with FastAPI using environment variables defined in `.env.local`:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

-----

## 🔄 Feedback & Retraining

Whenever a user corrects a category in the frontend:

1.  Feedback is appended to `transactly-backend/data/feedback.csv`.

**To retrain with feedback:**

```bash
python transactly-backend/scripts/retrain.py
```

**This regenerates:**

  * Embeddings
  * Classifier model
  * Updated category mapping

-----

## 🧠 Example API Output

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

## 🐳 Docker (Optional)

From the root directory:

```bash
cd transactly-backend
docker build -t transactly .
docker run -p 8000:8000 transactly
```

-----

## 🔐 Privacy & Design Principles

  * **No internet calls:** Data never leaves the machine.
  * **No external AI APIs:** No dependency on OpenAI or Gemini.
  * **Local classification only:** Fast and private.
  * **Fully explainable decisions:** Users know *why* a category was chosen.
  * **Deterministic fallbacks:** Ensures trustworthiness for known merchants.

-----

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python 3.11, FastAPI, scikit-learn, Sentence Transformers (MiniLM) |
| **Frontend** | Next.js 14, Tailwind CSS, Axios |
| **Storage** | Local CSV-based storage (No cloud database required) |

-----

## 👥 Contributors

| Name | Role |
| :--- | :--- |
| **Manoj MG** | AI Architecture • ML Pipeline • Backend (FastAPI) • Explainability |
| **Mercy** | Next.js Frontend • UI/UX • Documentation • Demo Assets |

-----

## 📝 Summary

Transactly demonstrates a production-grade offline AI engine with:

  * ✅ State-of-the-art embeddings
  * ✅ Interpretable logic
  * ✅ Retrainable ML
  * ✅ Clean modern web UI
  * ✅ Privacy-first design

### Next Step
Would you like me to create the **requirements.txt** file or the **Dockerfile** content based on the tech stack mentioned in this README?
```
