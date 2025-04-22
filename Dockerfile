# Base image with Python 3.11 and security patches
FROM python:3.11-slim AS base

# Environment variables to avoid bytecode files and ensure stdout flushing
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory in the container
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose port for API
EXPOSE 5000

# Default command to run the Flask API server
CMD ["python", "run.py", "--serve"]