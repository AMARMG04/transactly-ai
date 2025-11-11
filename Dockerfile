# ===============================
# Transactly — All-in-one container
# ===============================
FROM python:3.11-slim

# 1. Set working directory
WORKDIR /app

# 2. Install system deps (for building sentence-transformers, numpy, etc.)
RUN apt-get update && apt-get install -y \
    build-essential git cmake && \
    rm -rf /var/lib/apt/lists/*

# 3. Copy project files
COPY . /app

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Pre-download MiniLM model (so it’s offline)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# 6. Expose backend and frontend ports
EXPOSE 8000
EXPOSE 8501

# 7. Run both FastAPI & Streamlit together
# Use a simple bash script to start both
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0