#!/bin/bash
set -e

# Colors for output
green='\033[0;32m'
red='\033[0;31m'
yellow='\033[1;33m'
reset='\033[0m'

# Helper function
echo_success() { echo -e "${green}$1${reset}"; }
echo_error() { echo -e "${red}$1${reset}"; }
echo_warning() { echo -e "${yellow}$1${reset}"; }

# 1. Backend Python venv and dependencies
cd backend
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo_success "Created Python virtual environment."
else
  echo_success "Python virtual environment already exists."
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install uvicorn

echo_success "Backend dependencies installed."
deactivate
cd ..

# 2. Frontend Node.js and npm dependencies
if ! command -v node &> /dev/null; then
  echo_success "Node.js not found. Installing via Homebrew..."
  brew install node
else
  echo_success "Node.js is already installed."
fi

if [ -d "frontend" ]; then
  cd frontend
  npm install
  echo_success "Frontend dependencies installed."
  cd ..
else
  echo_error "Frontend directory not found!"
fi

# 3. MongoDB install and start
if ! command -v mongod &> /dev/null; then
  echo_success "MongoDB not found. Installing via Homebrew..."
  brew tap mongodb/brew
  brew install mongodb-community@6.0
else
  echo_success "MongoDB is already installed."
fi

# Try to start MongoDB service, but don't fail if there are permission issues
echo_success "Attempting to start MongoDB service..."
if brew services start mongodb-community@6.0 2>/dev/null; then
  echo_success "MongoDB service started successfully."
else
  echo_warning "Could not start MongoDB service automatically."
  echo_warning "You may need to start it manually with:"
  echo_warning "  brew services start mongodb-community@6.0"
  echo_warning "Or run MongoDB manually with:"
  echo_warning "  mongod --config /opt/homebrew/etc/mongod.conf"
fi

echo_success "\nAll setup steps completed!"
echo_success "To start the backend:"
echo_success "  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo_success "To start the frontend:"
echo_success "  cd frontend && npm start"
echo_warning "\nNote: If MongoDB didn't start automatically, you may need to:"
echo_warning "1. Start it manually: brew services start mongodb-community@6.0"
echo_warning "2. Or use a cloud MongoDB instance and update the MONGODB_URI in backend/.env" 