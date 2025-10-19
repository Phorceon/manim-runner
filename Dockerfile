FROM python:3.11-slim

# Install system dependencies required by Manim
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libcairo2 \
    libpango1.0-0 \
    libglib2.0-0 \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    tipa \
    fonts-freefont-otf \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose port and start FastAPI
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
