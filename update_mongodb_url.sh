#!/bin/bash

echo "🗄️ MongoDB URL Update Script"
echo "============================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found. Please run this script from the project root."
    exit 1
fi

echo ""
print_info "This script will help you update the MongoDB URL in render.yaml"
echo ""

# Check current status
if grep -q "YOUR_MONGODB_ATLAS_URL_HERE" render.yaml; then
    print_warning "Current status: MongoDB URL still has placeholder value"
else
    print_success "Current status: MongoDB URL already configured"
    echo ""
    print_info "Current MongoDB URL:"
    grep "MONGODB_URI" render.yaml | sed 's/.*value: //'
    exit 0
fi

echo ""
print_info "Please enter your MongoDB Atlas connection string:"
print_info "Format: mongodb+srv://username:password@cluster.mongodb.net/database"
echo ""

read -p "MongoDB URL: " mongodb_url

# Validate the URL format
if [[ $mongodb_url == mongodb+srv://* ]]; then
    print_success "✅ Valid MongoDB URL format detected"
else
    print_warning "⚠️  URL format doesn't look like a standard MongoDB Atlas URL"
    print_info "Expected format: mongodb+srv://username:password@cluster.mongodb.net/database"
    echo ""
    read -p "Continue anyway? (y/N): " continue_anyway
    if [[ $continue_anyway != "y" && $continue_anyway != "Y" ]]; then
        echo "Update cancelled."
        exit 1
    fi
fi

# Create backup
cp render.yaml render.yaml.backup
print_info "Created backup: render.yaml.backup"

# Update the file
sed -i.bak "s|YOUR_MONGODB_ATLAS_URL_HERE|$mongodb_url|g" render.yaml

# Verify the update
if grep -q "$mongodb_url" render.yaml; then
    print_success "✅ MongoDB URL updated successfully!"
    echo ""
    print_info "Updated render.yaml:"
    grep "MONGODB_URI" render.yaml | sed 's/.*value: //'
else
    print_warning "⚠️  Update may have failed. Please check render.yaml manually"
fi

echo ""
print_info "Next steps:"
echo "1. Test the connection locally (optional)"
echo "2. Commit your changes: git add render.yaml && git commit -m 'Update MongoDB URL'"
echo "3. Deploy: ./deploy_render.sh"
echo ""

# Clean up backup file
rm -f render.yaml.bak

print_success "🎉 MongoDB URL update complete!" 