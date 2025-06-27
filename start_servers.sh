#!/bin/bash

# Colors for output
green='\033[0;32m'
blue='\033[0;34m'
reset='\033[0m'

echo_success() { echo -e "${green}$1${reset}"; }
echo_info() { echo -e "${blue}$1${reset}"; }

echo_info "Starting Media Authentication System servers..."

# Start backend server
echo_info "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo_info "Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo_success "Servers started!"
echo_info "Backend PID: $BACKEND_PID"
echo_info "Frontend PID: $FRONTEND_PID"
echo_info ""
echo_info "Access your application at:"
echo_info "  Frontend: http://localhost:3000"
echo_info "  Backend API: http://localhost:8000"
echo_info "  API Docs: http://localhost:8000/docs"
echo_info ""
echo_info "To stop the servers, run:"
echo_info "  kill $BACKEND_PID $FRONTEND_PID" 