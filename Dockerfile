FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements-simple.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.1.1+cpu torchvision==0.16.1+cpu torchaudio==2.1.1+cpu

# Copy application code
COPY backend/ .

# Create necessary directories
RUN mkdir -p /tmp/uploads/images /tmp/uploads/videos /tmp/uploads/audio /tmp/uploads/temp ml_models && \
    chmod -R 755 /tmp/uploads

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app && \
    chown -R appuser:appuser /tmp/uploads
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 