#!/bin/bash

# Colors for output
green='\033[0;32m'
red='\033[0;31m'
yellow='\033[1;33m'
blue='\033[0;34m'
reset='\033[0m'

echo_success() { echo -e "${green}✓ $1${reset}"; }
echo_error() { echo -e "${red}✗ $1${reset}"; }
echo_warning() { echo -e "${yellow}⚠ $1${reset}"; }
echo_info() { echo -e "${blue}ℹ $1${reset}"; }

echo_info "Media Authentication System Status"
echo "======================================"

# Check backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo_success "Backend API (http://localhost:8000) - RUNNING"
else
    echo_error "Backend API (http://localhost:8000) - NOT RUNNING"
fi

# Check frontend
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo_success "Frontend (http://localhost:3000) - RUNNING"
else
    echo_error "Frontend (http://localhost:3000) - NOT RUNNING"
fi

# Check MongoDB
if brew services list | grep mongodb-community | grep started > /dev/null 2>&1; then
    echo_success "MongoDB - RUNNING"
elif pgrep mongod > /dev/null 2>&1; then
    echo_success "MongoDB - RUNNING (manual)"
else
    echo_warning "MongoDB - NOT RUNNING"
fi

echo ""
echo_info "Access URLs:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Documentation: http://localhost:8000/docs"
echo "  Health Check: http://localhost:8000/health"

echo ""
echo_info "To start services:"
echo "  Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "  Frontend: cd frontend && npm start"
echo "  MongoDB: brew services start mongodb-community@6.0"

echo ""
echo_info "To stop services:"
echo "  Backend: Ctrl+C in backend terminal"
echo "  Frontend: Ctrl+C in frontend terminal"
echo "  MongoDB: brew services stop mongodb-community@6.0" 