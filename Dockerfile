FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg libcairo2 && rm -rf /var/lib/apt/lists/*

# Install Python libs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY main.py .

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
