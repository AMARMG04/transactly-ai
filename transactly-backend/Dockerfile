# ======================================================
# Transactly Backend - FastAPI + SentenceTransformers
# Fully CPU-safe, pinned Python version
# ======================================================

FROM python:3.10-slim

# 1. Set working directory
WORKDIR /app

# 2. Install system-level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# 3. Copy backend code only
COPY . /app/

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Pre-download model (prevents runtime cold downloads)
RUN python - <<EOF
from sentence_transformers import SentenceTransformer
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
EOF

# 6. Expose FastAPI port
EXPOSE 8000

# 7. Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]