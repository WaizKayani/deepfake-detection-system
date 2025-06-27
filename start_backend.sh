#!/bin/bash

echo "🚀 Starting Deepfake Detection Backend..."

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment not found. Please run ./install_dependencies.sh first."
    exit 1
fi

# Activate virtual environment
cd backend
source venv/bin/activate

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running. Please start MongoDB first:"
    echo "   brew services start mongodb-community"
    echo ""
    echo "Starting backend anyway (may fail if MongoDB is not available)..."
fi

# Start the backend server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📊 API documentation available at http://localhost:8000/docs"
echo ""

# Use uvicorn from the virtual environment
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
