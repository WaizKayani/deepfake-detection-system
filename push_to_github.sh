#!/bin/bash

# Simple script to push Deepfake Detection System to GitHub
# Run this after creating a repository on GitHub

echo "🚀 GitHub Push Script for Deepfake Detection System"
echo "=================================================="

# Check if remote already exists
if git remote -v | grep -q "origin"; then
    echo "✅ Remote 'origin' already exists"
    echo "Current remotes:"
    git remote -v
else
    echo "❌ No remote 'origin' found"
    echo ""
    echo "📋 To push to GitHub, follow these steps:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository named 'deepfake-detection-system'"
    echo "3. Make it PUBLIC (for free deployment)"
    echo "4. DON'T initialize with README (we already have one)"
    echo "5. Copy the repository URL (it will look like: https://github.com/YOUR_USERNAME/deepfake-detection-system.git)"
    echo ""
    echo "6. Then run this command (replace YOUR_USERNAME with your GitHub username):"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/deepfake-detection-system.git"
    echo ""
    echo "7. Finally run:"
    echo "   git push -u origin main"
    echo ""
    echo "🔗 After pushing, you can deploy to Render:"
    echo "   - Go to https://dashboard.render.com/"
    echo "   - Click 'New +' → 'Blueprint'"
    echo "   - Connect your GitHub account"
    echo "   - Select your repository"
    echo "   - Click 'Apply' to deploy all services"
    echo ""
fi

# Show current status
echo ""
echo "📊 Current Git Status:"
git status

echo ""
echo "📝 Recent commits:"
git log --oneline -5 