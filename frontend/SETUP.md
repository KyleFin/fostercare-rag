# Setup Guide - Foster Care Policy Assistant

This guide will help you set up and run the Foster Care Policy Assistant frontend with the FastAPI backend.

## Prerequisites

- **Node.js** (version 16 or higher)
- **Python** (version 3.8 or higher)
- **npm** or **yarn**
- **Git**

## Quick Start

### 1. Clone and Setup Backend

```bash
# Navigate to the project root
cd fostercare-rag

# Install Python dependencies
cd api
pip install -r requirements.txt

# Start the FastAPI backend
python app.py
```

The backend will start on `http://localhost:8000`

### 2. Setup and Start Frontend

In a new terminal:

```bash
# Navigate to frontend directory
cd fostercare-rag/frontend

# Use the startup script (recommended)
./start.sh

# Or manually:
npm install
npm start
```

The frontend will start on `http://localhost:3000`

## Manual Setup

### Backend Setup

1. **Install Python Dependencies**:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   Create a `.env` file in the `api` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   ```

3. **Start Backend**:
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Install Node.js Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm start
   ```

## Verification

### Check Backend Health

```bash
curl http://localhost:8000/api/health
```

Should return: `{"status": "ok"}`

### Test Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message": "What are foster care policies?"}'
```

### Access Frontend

Open your browser and navigate to: `http://localhost:3000`

## Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Kill process on port 8000 (backend)
   lsof -ti:8000 | xargs kill -9
   
   # Kill process on port 3000 (frontend)
   lsof -ti:3000 | xargs kill -9
   ```

2. **CORS Errors**:
   - Ensure the backend is running on `http://localhost:8000`
   - Check that CORS middleware is properly configured in `api/app.py`

3. **Module Not Found Errors**:
   ```bash
   # Reinstall dependencies
   cd api && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

4. **API Key Issues**:
   - Verify your `.env` file has the correct API keys
   - Ensure the keys have sufficient credits/permissions

### Development Tips

1. **Backend Logs**: Watch the terminal running the backend for detailed logs
2. **Frontend Logs**: Check browser developer tools (F12) for frontend errors
3. **Network Tab**: Use browser dev tools to monitor API requests
4. **Hot Reload**: Both frontend and backend support hot reloading during development

## Production Deployment

### Frontend Build

```bash
cd frontend
npm run build
```

This creates a `build` folder with optimized production files.

### Backend Deployment

The backend can be deployed using:
- **Vercel** (using `vercel.json`)
- **Railway**
- **Heroku**
- **AWS/GCP/Azure**

## File Structure

```
fostercare-rag/
├── api/                    # FastAPI backend
│   ├── app.py             # Main API server
│   ├── agent.py           # LangGraph agent
│   ├── tools.py           # RAG tools
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── src/               # React source code
│   ├── public/            # Static assets
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend documentation
└── data/                  # Policy documents
```

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs in both terminal windows
3. Verify all prerequisites are installed
4. Ensure both backend and frontend are running on the correct ports 