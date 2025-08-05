#!/bin/bash

# Foster Care Policy Assistant Frontend Startup Script

echo "🚀 Starting Foster Care Policy Assistant Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:8000/api/health > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "⚠️  Warning: Backend not detected on http://localhost:8000"
    echo "   Make sure to start the FastAPI backend first:"
    echo "   cd ../api && python app.py"
    echo ""
fi

echo "🌐 Starting React development server..."
echo "   Frontend will be available at: http://localhost:3000"
echo ""

npm start 