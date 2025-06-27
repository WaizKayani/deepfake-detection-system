# 🚀 Deployment Guide

This guide will help you deploy the Deepfake Detection System to various platforms.

## 📋 Prerequisites

Before deploying, ensure you have the following installed:

- **Git** - Version control
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Node.js** (16+) - For frontend development
- **Python** (3.9+) - For backend development

## 🎯 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/deepfake-detection-system.git
cd deepfake-detection-system

# Run the automated setup
chmod +x setup_all.sh
./setup_all.sh
```

### 2. Local Development

```bash
# Start all services
./start_servers.sh

# Or start individually
./start_backend.sh
./start_frontend.sh
```

Access the application at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🐳 Docker Deployment

### Local Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or use the deployment script
./deploy.sh deploy-local
```

### Production Docker Deployment

```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d
```

## ☁️ Cloud Deployment

### GitHub Repository Setup

1. **Create GitHub Repository**
   ```bash
   # Go to GitHub.com and create a new repository
   # Then run the setup script
   ./deploy.sh setup-github
   ```

2. **Configure Environment Variables**
   ```bash
   export DOCKER_USERNAME="your-docker-username"
   export DOCKER_PASSWORD="your-docker-password"
   export GITHUB_USERNAME="your-github-username"
   ```

### Heroku Deployment

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Deploy to Heroku
./deploy.sh deploy-cloud --platform heroku
```

### AWS Deployment

```bash
# Install AWS CLI
brew install awscli

# Configure AWS credentials
aws configure

# Deploy to AWS
./deploy.sh deploy-cloud --platform aws
```

### Google Cloud Deployment

```bash
# Install Google Cloud CLI
brew install google-cloud-sdk

# Authenticate
gcloud auth login

# Deploy to GCP
./deploy.sh deploy-cloud --platform gcp
```

### Azure Deployment

```bash
# Install Azure CLI
brew install azure-cli

# Authenticate
az login

# Deploy to Azure
./deploy.sh deploy-cloud --platform azure
```

## 🔧 Manual Deployment Steps

### 1. GitHub Repository

```bash
# Initialize Git repository
git init
git add .
git commit -m "Initial commit: Deepfake Detection System"

# Create repository on GitHub.com
# Then push your code
git remote add origin https://github.com/yourusername/deepfake-detection-system.git
git branch -M main
git push -u origin main
```

### 2. Docker Images

```bash
# Build images
docker build -f backend/Dockerfile -t yourusername/deepfake-backend:latest ./backend
docker build -f frontend/Dockerfile -t yourusername/deepfake-frontend:latest ./frontend

# Push to Docker Hub
docker login
docker push yourusername/deepfake-backend:latest
docker push yourusername/deepfake-frontend:latest
```

### 3. Environment Configuration

Create a `.env` file:

```env
# Database
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=secure-password
DATABASE_NAME=deepfake_detection

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]

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
DOCKER_USERNAME=yourusername
```

## 🔒 Security Considerations

### Production Security

1. **Environment Variables**
   - Use strong, unique passwords
   - Store secrets in environment variables
   - Never commit secrets to Git

2. **SSL/TLS**
   - Enable HTTPS in production
   - Use Let's Encrypt for free certificates
   - Configure proper CORS settings

3. **Database Security**
   - Use strong database passwords
   - Enable authentication
   - Restrict network access

4. **File Upload Security**
   - Validate file types
   - Set size limits
   - Scan for malware

### Security Checklist

- [ ] Change default passwords
- [ ] Enable HTTPS
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Backup strategy
- [ ] Disaster recovery plan

## 📊 Monitoring and Logging

### Prometheus Metrics

The system includes Prometheus metrics for:
- Request rates and response times
- Model prediction accuracy
- System resource usage
- Error rates and types

### Grafana Dashboards

Access Grafana at `http://localhost:3001` (default: admin/admin) for:
- Real-time system performance
- Model accuracy trends
- User activity analytics
- System health monitoring

### Logging

Logs are available in:
- Application logs: `logs/`
- Docker logs: `docker-compose logs`
- System logs: `/var/log/`

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:
- Runs tests on pull requests
- Builds Docker images on main branch
- Deploys to staging/production
- Runs security scans
- Performs code quality checks

### Manual CI/CD Steps

```bash
# Run tests
cd backend && python -m pytest tests/
cd frontend && npm test

# Build and push
./deploy.sh build
./deploy.sh push

# Deploy
./deploy.sh deploy-local
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Docker Build Fails**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker build --no-cache -f backend/Dockerfile ./backend
   ```

3. **MongoDB Connection Issues**
   ```bash
   # Check MongoDB status
   brew services list | grep mongodb
   
   # Restart MongoDB
   brew services restart mongodb-community@6.0
   ```

4. **Frontend Build Issues**
   ```bash
   # Clear npm cache
   npm cache clean --force
   
   # Reinstall dependencies
   rm -rf node_modules package-lock.json
   npm install
   ```

### Debug Mode

Enable debug mode for troubleshooting:

```bash
# Set debug environment variable
export DEBUG=True

# Or in .env file
DEBUG=True
```

### Logs

Check logs for errors:

```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# All logs
docker-compose logs
```

## 📈 Performance Optimization

### Backend Optimization

1. **Database Indexing**
   ```javascript
   // Create indexes for frequently queried fields
   db.analysis_results.createIndex({ "upload_time": -1 })
   db.analysis_results.createIndex({ "file_type": 1 })
   ```

2. **Caching**
   - Enable Redis for caching
   - Cache model predictions
   - Cache API responses

3. **Async Processing**
   - Use Celery for background tasks
   - Process large files asynchronously
   - Queue management

### Frontend Optimization

1. **Code Splitting**
   - Lazy load components
   - Bundle optimization
   - CDN for static assets

2. **Caching**
   - Browser caching
   - Service worker
   - Local storage

## 🔄 Updates and Maintenance

### Updating the System

```bash
# Pull latest changes
git pull origin main

# Rebuild and redeploy
./deploy.sh build
./deploy.sh deploy-local
```

### Database Migrations

```bash
# Backup database
mongodump --db deepfake_detection --out backup/

# Restore database
mongorestore --db deepfake_detection backup/deepfake_detection/
```

### Monitoring Updates

- Check Prometheus targets
- Verify Grafana dashboards
- Review alert rules
- Update dependencies

## 📞 Support

For deployment issues:

1. **Check the logs** for error messages
2. **Review the documentation** for configuration
3. **Create an issue** on GitHub
4. **Contact support** at support@yourdomain.com

## 🎉 Success!

Once deployed, your Deepfake Detection System will be available at:
- **Production URL**: https://your-app.herokuapp.com (or your domain)
- **API Documentation**: https://your-app.herokuapp.com/docs
- **Monitoring**: https://your-app.herokuapp.com:3001 (Grafana)

---

**Happy Deploying! 🚀** 