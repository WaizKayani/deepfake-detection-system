#!/bin/bash

# Deepfake Detection System Deployment Script
# This script helps deploy the system to various platforms

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_NAME="deepfake-detection-system"
DOCKER_USERNAME=${DOCKER_USERNAME:-"your-docker-username"}
GITHUB_USERNAME=${GITHUB_USERNAME:-"your-github-username"}

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_commands=()
    
    if ! command_exists git; then
        missing_commands+=("git")
    fi
    
    if ! command_exists docker; then
        missing_commands+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_commands+=("docker-compose")
    fi
    
    if [ ${#missing_commands[@]} -ne 0 ]; then
        print_error "Missing required commands: ${missing_commands[*]}"
        print_status "Please install the missing commands and try again."
        exit 1
    fi
    
    print_success "All prerequisites are installed"
}

# Function to setup GitHub repository
setup_github() {
    print_status "Setting up GitHub repository..."
    
    if [ ! -d ".git" ]; then
        print_status "Initializing Git repository..."
        git init
        git add .
        git commit -m "Initial commit: Deepfake Detection System"
    fi
    
    if ! git remote get-url origin >/dev/null 2>&1; then
        print_status "Adding GitHub remote..."
        git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    fi
    
    print_status "Pushing to GitHub..."
    git branch -M main
    git push -u origin main
    
    print_success "GitHub repository setup complete"
}

# Function to build Docker images
build_docker_images() {
    print_status "Building Docker images..."
    
    # Build backend image
    print_status "Building backend image..."
    docker build -f backend/Dockerfile -t "$DOCKER_USERNAME/deepfake-backend:latest" ./backend
    
    # Build frontend image
    print_status "Building frontend image..."
    docker build -f frontend/Dockerfile -t "$DOCKER_USERNAME/deepfake-frontend:latest" ./frontend
    
    print_success "Docker images built successfully"
}

# Function to push Docker images
push_docker_images() {
    print_status "Pushing Docker images to registry..."
    
    # Login to Docker Hub
    if [ -z "$DOCKER_PASSWORD" ]; then
        print_warning "DOCKER_PASSWORD not set. Please login manually:"
        docker login
    else
        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
    fi
    
    # Push images
    docker push "$DOCKER_USERNAME/deepfake-backend:latest"
    docker push "$DOCKER_USERNAME/deepfake-frontend:latest"
    
    print_success "Docker images pushed successfully"
}

# Function to deploy locally with Docker Compose
deploy_local() {
    print_status "Deploying locally with Docker Compose..."
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating .env file..."
        cat > .env << EOF
# Database
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=password
DATABASE_NAME=deepfake_detection

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Security
SECRET_KEY=$(openssl rand -hex 32)
CORS_ORIGINS=["http://localhost:3000"]

# ML Models
MODEL_CACHE_DIR=./ml_models
HUGGINGFACE_CACHE_DIR=./cache

# File Upload
MAX_FILE_SIZE=104857600
UPLOAD_DIR=./uploads

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
GRAFANA_PASSWORD=admin

# Docker
DOCKER_USERNAME=$DOCKER_USERNAME
EOF
        print_success ".env file created"
    fi
    
    # Start services
    docker-compose -f docker-compose.prod.yml up -d
    
    print_success "Local deployment complete"
    print_status "Services available at:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Grafana: http://localhost:3001"
}

# Function to deploy to cloud platform
deploy_cloud() {
    local platform=$1
    
    case $platform in
        "heroku")
            deploy_heroku
            ;;
        "aws")
            deploy_aws
            ;;
        "gcp")
            deploy_gcp
            ;;
        "azure")
            deploy_azure
            ;;
        *)
            print_error "Unknown platform: $platform"
            print_status "Supported platforms: heroku, aws, gcp, azure"
            exit 1
            ;;
    esac
}

# Function to deploy to Heroku
deploy_heroku() {
    print_status "Deploying to Heroku..."
    
    if ! command_exists heroku; then
        print_error "Heroku CLI not installed. Please install it first."
        exit 1
    fi
    
    # Create Heroku app
    heroku create "$REPO_NAME" || true
    
    # Add MongoDB addon
    heroku addons:create mongolab:sandbox
    
    # Set environment variables
    heroku config:set SECRET_KEY=$(openssl rand -hex 32)
    heroku config:set DEBUG=False
    
    # Deploy
    git push heroku main
    
    print_success "Heroku deployment complete"
    print_status "App URL: https://$(heroku info -s | grep web_url | cut -d= -f2)"
}

# Function to deploy to AWS
deploy_aws() {
    print_status "Deploying to AWS..."
    
    if ! command_exists aws; then
        print_error "AWS CLI not installed. Please install it first."
        exit 1
    fi
    
    # Check if AWS credentials are configured
    if ! aws sts get-caller-identity >/dev/null 2>&1; then
        print_error "AWS credentials not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    # Create ECR repositories
    aws ecr create-repository --repository-name deepfake-backend || true
    aws ecr create-repository --repository-name deepfake-frontend || true
    
    # Get ECR login token
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin "$(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com"
    
    # Tag and push images
    local account_id=$(aws sts get-caller-identity --query Account --output text)
    local region="us-east-1"
    
    docker tag "$DOCKER_USERNAME/deepfake-backend:latest" "$account_id.dkr.ecr.$region.amazonaws.com/deepfake-backend:latest"
    docker tag "$DOCKER_USERNAME/deepfake-frontend:latest" "$account_id.dkr.ecr.$region.amazonaws.com/deepfake-frontend:latest"
    
    docker push "$account_id.dkr.ecr.$region.amazonaws.com/deepfake-backend:latest"
    docker push "$account_id.dkr.ecr.$region.amazonaws.com/deepfake-frontend:latest"
    
    print_success "AWS ECR deployment complete"
    print_status "Images pushed to ECR. Use ECS/Fargate to deploy the containers."
}

# Function to deploy to Google Cloud
deploy_gcp() {
    print_status "Deploying to Google Cloud..."
    
    if ! command_exists gcloud; then
        print_error "Google Cloud CLI not installed. Please install it first."
        exit 1
    fi
    
    # Create GKE cluster
    gcloud container clusters create deepfake-cluster --num-nodes=3 --zone=us-central1-a
    
    # Get credentials
    gcloud container clusters get-credentials deepfake-cluster --zone=us-central1-a
    
    # Apply Kubernetes manifests
    kubectl apply -f k8s/
    
    print_success "Google Cloud deployment complete"
}

# Function to deploy to Azure
deploy_azure() {
    print_status "Deploying to Azure..."
    
    if ! command_exists az; then
        print_error "Azure CLI not installed. Please install it first."
        exit 1
    fi
    
    # Create AKS cluster
    az aks create --resource-group deepfake-rg --name deepfakeCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys
    
    # Get credentials
    az aks get-credentials --resource-group deepfake-rg --name deepfakeCluster
    
    # Apply Kubernetes manifests
    kubectl apply -f k8s/
    
    print_success "Azure deployment complete"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  setup-github     Setup GitHub repository and push code"
    echo "  build            Build Docker images"
    echo "  push             Push Docker images to registry"
    echo "  deploy-local     Deploy locally with Docker Compose"
    echo "  deploy-cloud     Deploy to cloud platform"
    echo "  all              Run all steps (setup-github, build, push, deploy-local)"
    echo ""
    echo "Options for deploy-cloud:"
    echo "  --platform PLATFORM    Cloud platform (heroku, aws, gcp, azure)"
    echo ""
    echo "Environment Variables:"
    echo "  DOCKER_USERNAME         Docker Hub username"
    echo "  DOCKER_PASSWORD         Docker Hub password"
    echo "  GITHUB_USERNAME         GitHub username"
    echo ""
    echo "Examples:"
    echo "  $0 setup-github"
    echo "  $0 deploy-local"
    echo "  $0 deploy-cloud --platform heroku"
    echo "  $0 all"
}

# Main script
main() {
    local command=$1
    local platform=$2
    
    # Check prerequisites
    check_prerequisites
    
    case $command in
        "setup-github")
            setup_github
            ;;
        "build")
            build_docker_images
            ;;
        "push")
            push_docker_images
            ;;
        "deploy-local")
            deploy_local
            ;;
        "deploy-cloud")
            if [ -z "$platform" ]; then
                print_error "Platform not specified. Use --platform PLATFORM"
                exit 1
            fi
            deploy_cloud "$platform"
            ;;
        "all")
            setup_github
            build_docker_images
            push_docker_images
            deploy_local
            ;;
        *)
            show_usage
            exit 1
            ;;
    esac
}

# Parse command line arguments
case $1 in
    "deploy-cloud")
        if [ "$2" = "--platform" ]; then
            main "$1" "$3"
        else
            print_error "Invalid arguments for deploy-cloud"
            show_usage
            exit 1
        fi
        ;;
    *)
        main "$1"
        ;;
esac 