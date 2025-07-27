#!/bin/bash

echo "🔍 Deepfake Detection System - Deployment Readiness Check"
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check counter
checks_passed=0
checks_total=0

# Function to run a check
run_check() {
    local description="$1"
    local command="$2"
    local expected="$3"
    
    checks_total=$((checks_total + 1))
    print_status "Checking: $description"
    
    if eval "$command" 2>/dev/null | grep -q "$expected"; then
        print_success "✓ $description"
        checks_passed=$((checks_passed + 1))
    else
        print_error "✗ $description"
    fi
}

echo ""
echo "📋 Running deployment readiness checks..."
echo ""

# Check 1: render.yaml exists
run_check "render.yaml configuration file exists" "test -f render.yaml" ""

# Check 2: Backend requirements.txt exists
run_check "Backend requirements.txt exists" "test -f backend/requirements.txt" ""

# Check 3: Frontend package.json exists
run_check "Frontend package.json exists" "test -f frontend/package.json" ""

# Check 4: Backend main.py exists
run_check "Backend main.py exists" "test -f backend/app/main.py" ""

# Check 5: Health endpoint in main.py
run_check "Health endpoint configured" "grep -q 'health_check' backend/app/main.py" ""

# Check 6: CORS configuration
run_check "CORS middleware configured" "grep -q 'CORSMiddleware' backend/app/main.py" ""

# Check 7: FastAPI app creation
run_check "FastAPI app properly configured" "grep -q 'FastAPI(' backend/app/main.py" ""

# Check 8: Frontend build script
run_check "Frontend build script exists" "grep -q '\"build\"' frontend/package.json" ""

# Check 9: React dependencies
run_check "React dependencies configured" "grep -q '\"react\"' frontend/package.json" ""

# Check 10: Docker configuration
run_check "Docker configuration exists" "test -f docker-compose.yml" ""

echo ""
echo "🔧 Configuration Issues to Address:"
echo "==================================="

# Check MongoDB URL placeholder
if grep -q "YOUR_MONGODB_ATLAS_URL_HERE" render.yaml; then
    print_error "✗ MongoDB URL still has placeholder value in render.yaml"
    print_status "   Action: Replace 'YOUR_MONGODB_ATLAS_URL_HERE' with your actual MongoDB Atlas connection string"
else
    print_success "✓ MongoDB URL configured"
    checks_passed=$((checks_passed + 1))
    checks_total=$((checks_total + 1))
fi

# Check if git repository is clean
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    print_warning "⚠ You have uncommitted changes"
    print_status "   Action: Commit your changes before deployment"
else
    print_success "✓ Git repository is clean"
    checks_passed=$((checks_passed + 1))
    checks_total=$((checks_total + 1))
fi

echo ""
echo "📊 Deployment Readiness Summary:"
echo "================================"
echo "Checks passed: $checks_passed/$checks_total"

if [ $checks_passed -eq $checks_total ]; then
    echo ""
    print_success "🎉 Your project is READY for Render deployment!"
    echo ""
    echo "Next steps:"
    echo "1. Update MongoDB URL in render.yaml"
    echo "2. Commit any pending changes"
    echo "3. Run: ./deploy_render.sh"
    echo "4. Follow the manual deployment steps"
else
    echo ""
    print_warning "⚠ Some issues need to be resolved before deployment"
    echo ""
    echo "Please address the issues above before proceeding with deployment."
fi

echo ""
echo "📚 Additional Resources:"
echo "======================="
echo "• Deployment Guide: RENDER_DEPLOYMENT_GUIDE.md"
echo "• Quick Deploy: QUICK_DEPLOY.md"
echo "• Checklist: DEPLOYMENT_CHECKLIST.md" 