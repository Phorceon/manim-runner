FROM python:3.11-bullseye

# System deps needed for Manim, pycairo, pangocairo, GI, fonts, and TeX
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    pkg-config \
    git \
    python3-dev \
    python3-gi \
    libcairo2 \
    libcairo2-dev \
    libpango1.0-0 \
    libpango1.0-dev \
    libpangocairo-1.0-0 \
    libpangocairo-1.0-dev \
    libglib2.0-0 \
    libglib2.0-dev \
    libgirepository1.0-dev \
    gir1.2-pango-1.0 \
    libffi-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libpng-dev \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-plain-generic \
    fonts-freefont-otf \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip tooling to avoid wheel/build issues
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY main.py .

# Expose port
EXPOSE 8080

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
