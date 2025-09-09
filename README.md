# Foster Care RAG Application

This project uses Retrieval-Augmented Generation (RAG) to reliably answer questions about foster care policies across US states.

👉 See demo videos in [cert.md](/cert.md) 👈

## Running with Docker

### Using Docker Compose (Recommended)

```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file with your API keys
vi .env

# Run the application
docker-compose up
```

### Using Docker Run

When using `docker run` directly, you must explicitly pass environment variables:

```bash
docker run -it -p 8000:8000 -p 3000:3000 \
  -e OPENAI_API_KEY=your_openai_key \
  -e COHERE_API_KEY=your_cohere_key \
  -e TAVILY_API_KEY=your_tavily_key \
  -e LANGCHAIN_API_KEY=your_langchain_key \
  kfin-containers
```

Or reference environment variables from your host:

```bash
docker run -it -p 8000:8000 -p 3000:3000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e COHERE_API_KEY=$COHERE_API_KEY \
  -e TAVILY_API_KEY=$TAVILY_API_KEY \
  -e LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY \
  kfin-containers
```
