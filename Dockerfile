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

# Create a simple HTTP server script to serve the frontend
RUN echo '#!/usr/bin/env python3\n\
import http.server\n\
import socketserver\n\
import os\n\
import threading\n\
import subprocess\n\
import sys\n\
\n\
def serve_frontend():\n\
    os.chdir("/app/frontend/build")\n\
    with socketserver.TCPServer(("", 3000), http.server.SimpleHTTPRequestHandler) as httpd:\n\
        print("Frontend server running on port 3000")\n\
        httpd.serve_forever()\n\
\n\
def serve_api():\n\
    os.chdir("/app")\n\
    subprocess.run([sys.executable, "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"])\n\
\n\
if __name__ == "__main__":\n\
    # Start frontend server in a separate thread\n\
    frontend_thread = threading.Thread(target=serve_frontend, daemon=True)\n\
    frontend_thread.start()\n\
    \n\
    # Start API server in main thread\n\
    serve_api()\n\
' > /app/start_services.py

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
