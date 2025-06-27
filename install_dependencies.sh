#!/bin/bash

echo "🚀 Installing dependencies for Deepfake Detection System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment and install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install system dependencies for face recognition
echo "📦 Installing system dependencies for face recognition..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    brew install cmake
    brew install dlib
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    sudo apt-get update
    sudo apt-get install -y cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev
fi

# Install Python packages
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Install additional dependencies for real models
echo "📦 Installing additional ML dependencies..."
pip install face-recognition==1.3.0
pip install face-recognition-models==0.3.0
pip install transformers==4.35.2
pip install librosa==0.10.1
pip install soundfile==0.12.1
pip install scipy==1.11.4

cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create upload directories
echo "📁 Creating upload directories..."
mkdir -p backend/uploads/image
mkdir -p backend/uploads/video
mkdir -p backend/uploads/audio

# Create temp directories
mkdir -p /tmp/video_frames

# Set permissions
chmod 755 backend/uploads
chmod 755 /tmp/video_frames

echo "✅ Dependencies installed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Start MongoDB: brew services start mongodb-community"
echo "2. Start the backend: ./start_backend.sh"
echo "3. Start the frontend: ./start_frontend.sh"
echo "4. Open http://localhost:3000 in your browser" 