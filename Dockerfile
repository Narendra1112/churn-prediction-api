# ---- Streamlit Dockerfile ----
FROM python:3.10-slim

WORKDIR /app

# Copy all files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "Streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
