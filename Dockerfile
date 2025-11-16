# ===============================
# Transactly — FastAPI Backend
# ===============================

FROM python:3.11-slim

# 1. Working directory
WORKDIR /app

# 2. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential git cmake && \
    rm -rf /var/lib/apt/lists/*

# 3. Copy repo contents
COPY . /app

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Pre-download MiniLM model (offline loading)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# 6. Expose FastAPI port
EXPOSE 8000

# 7. Start FastAPI backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]