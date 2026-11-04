
# Use Python runtime
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency definitions first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/
COPY ingestion/ ./ingestion/
COPY retrieval/ ./retrieval/
COPY graph/ ./graph/

# Expose Streamlit port
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
