#!/bin/bash

# Foster Care RAG Docker Startup Script

echo "🚀 Starting Foster Care RAG Application..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Please create one with your API keys:"
    echo "   OPENAI_API_KEY=your_openai_key_here"
    echo "   COHERE_API_KEY=your_cohere_key_here"
    echo ""
fi

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ FastAPI is running on http://localhost:8000"
else
    echo "❌ FastAPI failed to start"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is running on http://localhost:3000"
else
    echo "❌ Frontend failed to start"
fi

echo ""
echo "🎉 Application should be running at:"
echo "   Frontend: http://localhost:3000"
echo "   API: http://localhost:8000"
echo ""
echo "📖 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
