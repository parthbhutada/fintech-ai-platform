# Multi-stage lightweight Dockerfile for NexusFin AI Platform
FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5050

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt .

# Optional package install (software contains pure-Python fallbacks as well)
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy project files
COPY . .

# Run test suite to verify container integrity
RUN python3 -m unittest discover -s tests -p "test_*.py"

# Expose microservice port
EXPOSE 5050

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5050/health || exit 1

# Default command launches straight-through CLI demo or web API
CMD ["python3", "src/cli.py", "pipeline", "--dataset", "dataset/lending_club_sample.csv"]
