#!/bin/bash

# Start Web Application Script
# This script starts both the backend API and opens the frontend

echo "🚀 Starting Trip Planner Web Application..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run:"
    echo "   python3 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Copy .env.example to .env and add your ANTHROPIC_API_KEY"
    echo ""
fi

# Activate virtual environment
source .venv/bin/activate

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Installing web dependencies..."
    pip install flask flask-cors
fi

# Find available port (5000 or 5001)
PORT=5000
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 5000 is in use, using port 5001 instead"
    PORT=5001
fi

# Start backend
echo "🔧 Starting backend server on port $PORT..."
PORT=$PORT python web_app/backend/app.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:$PORT/api/health > /dev/null; then
    echo "✅ Backend is running!"
else
    echo "❌ Backend failed to start. Check backend.log for errors."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "📝 Update the API URL in web_app/frontend/public/app.js:"
echo "   const API_BASE_URL = 'http://localhost:$PORT/api';"
echo ""

# Open frontend
echo "🌐 Opening frontend..."
cd web_app/frontend/public

# Try to start a simple HTTP server
if command -v python3 &> /dev/null; then
    echo "   Starting frontend on http://localhost:8080"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 Application is ready!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 Frontend:  http://localhost:8080"
    echo "📍 Backend:   http://localhost:$PORT"
    echo "📍 API Docs:  http://localhost:$PORT/api/health"
    echo ""
    echo "To stop:"
    echo "   Press Ctrl+C in this terminal"
    echo "   Or run: kill $BACKEND_PID"
    echo ""
    echo "Logs: backend.log"
    echo ""

    # Start frontend server
    python3 -m http.server 8080
else
    # Just open the HTML file
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open index.html
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open index.html
    else
        echo "Please open web_app/frontend/public/index.html in your browser"
    fi
fi

# Cleanup on exit
trap "echo 'Stopping backend...'; kill $BACKEND_PID 2>/dev/null" EXIT
