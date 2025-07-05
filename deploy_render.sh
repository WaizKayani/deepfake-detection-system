#!/bin/bash

echo "🚀 Deepfake Detection System - Render Deployment Script"
echo "======================================================"

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

# Check if git is available
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "render.yaml" ]; then
    print_error "render.yaml not found. Please run this script from the project root."
    exit 1
fi

print_status "Starting deployment process..."

# Step 1: Check git status
print_status "Checking git status..."
if [ -n "$(git status --porcelain)" ]; then
    print_warning "You have uncommitted changes. Committing them..."
    git add .
    git commit -m "Prepare for Render deployment"
fi

# Step 2: Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    print_error "No remote origin found. Please add your GitHub repository as origin."
    print_status "Example: git remote add origin https://github.com/username/repo.git"
    exit 1
fi

# Step 3: Push to GitHub
print_status "Pushing to GitHub..."
if git push origin main; then
    print_success "Code pushed to GitHub successfully!"
else
    print_warning "Push failed. Trying force push..."
    if git push --force origin main; then
        print_success "Force push successful!"
    else
        print_error "Failed to push to GitHub. Please resolve conflicts manually."
        exit 1
    fi
fi

# Step 4: Display deployment instructions
echo ""
echo "🎯 Manual Deployment Steps Required:"
echo "===================================="
echo ""
echo "1. 📝 Update MongoDB URL in render.yaml:"
echo "   - Open render.yaml"
echo "   - Replace 'YOUR_MONGODB_ATLAS_URL_HERE' with your actual MongoDB Atlas connection string"
echo ""
echo "2. 🌐 Go to Render Dashboard:"
echo "   - Visit: https://dashboard.render.com"
echo "   - Sign up/Login with GitHub"
echo ""
echo "3. 🚀 Deploy using Blueprint:"
echo "   - Click 'New +' → 'Blueprint'"
echo "   - Connect your GitHub repository"
echo "   - Select: $(basename $(pwd))"
echo "   - Click 'Connect'"
echo ""
echo "4. ⚙️ Configure Environment Variables:"
echo "   - In the backend service, go to 'Environment' tab"
echo "   - Update MONGODB_URL with your Atlas connection string"
echo "   - Click 'Save Changes'"
echo ""
echo "5. 🎯 Deploy:"
echo "   - Click 'Create Blueprint'"
echo "   - Wait 5-10 minutes for deployment"
echo ""
echo "6. ✅ Verify Deployment:"
echo "   - Backend: https://deepfake-backend.onrender.com"
echo "   - Frontend: https://deepfake-frontend.onrender.com"
echo "   - API Docs: https://deepfake-backend.onrender.com/docs"
echo ""

print_success "Deployment script completed! Follow the manual steps above."
print_status "Your project will be deployed as:"
print_status "- Backend: https://deepfake-backend.onrender.com"
print_status "- Frontend: https://deepfake-frontend.onrender.com" 