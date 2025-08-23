# Multi-stage build for Foster Care RAG application
FROM node:18-alpine AS frontend-builder

# Set working directory for frontend
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Clean install - remove lock file if it exists and install fresh
RUN rm -f package-lock.json && npm install --omit=dev

# Copy frontend source code
COPY frontend/src ./src
COPY frontend/public ./public

# Build frontend
RUN npm run build

# Python runtime stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API source code
COPY api/ ./api/

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Copy data files
COPY data/ ./data/

# Copy the proxy handler script
COPY proxy_handler.py /app/start_services.py

RUN chmod +x /app/start_services.py

# Expose ports for frontend and API
EXPOSE 3000 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start both services
CMD ["python", "start_services.py"]
