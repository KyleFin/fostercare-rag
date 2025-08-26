# Docker Setup for Foster Care RAG Application

This document explains how to run the Foster Care RAG application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- API keys for OpenAI and Cohere (optional, but required for full functionality)

## Quick Start

### Option 1: Using the startup script (Recommended)

1. **Set up environment variables** (optional but recommended):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Run the startup script**:
   ```bash
   ./start-docker.sh
   ```

### Option 2: Manual Docker commands

1. **Build the image**:
   ```bash
   docker-compose build
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Check the status**:
   ```bash
   docker-compose ps
   ```

## What Gets Built

The Docker setup creates a multi-stage build that:

1. **Builds the React frontend** using Node.js 18
2. **Sets up Python environment** with all required dependencies
3. **Runs both services** in a single container:
   - FastAPI backend on port 8000
   - Frontend static files served on port 3000

## Ports

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/health

## Environment Variables

Create a `.env` file in the root directory with:

```env
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
```

## Useful Commands

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fostercare-rag
```

### Stop services
```bash
docker-compose down
```

### Rebuild and restart
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Access container shell
```bash
docker-compose exec fostercare-rag bash
```

## Troubleshooting

### Port conflicts
If ports 3000 or 8000 are already in use, modify the `docker-compose.yml` file to use different ports:

```yaml
ports:
  - "3001:3000"  # Frontend on host port 3001
  - "8001:8000"  # API on host port 8001
```

### Build issues
If you encounter build issues:

1. Clear Docker cache:
   ```bash
   docker system prune -a
   ```

2. Rebuild without cache:
   ```bash
   docker-compose build --no-cache
   ```

### Memory issues
If the container runs out of memory, you can increase Docker's memory limit in Docker Desktop settings.

## Development vs Production

This Docker setup is designed for development and testing. For production:

1. Use a production-grade web server (nginx) instead of Python's built-in server
2. Implement proper logging and monitoring
3. Use environment-specific configuration files
4. Consider using Docker Swarm or Kubernetes for orchestration

## File Structure in Container

```
/app/
├── api/           # FastAPI application
├── frontend/      # Built React application
├── data/          # PDF documents and data files
└── start_services.py  # Service startup script
```

## Health Checks

The container includes health checks that verify:
- FastAPI is responding on port 8000
- Frontend is accessible on port 3000

Health check status can be viewed with:
```bash
docker-compose ps
```
