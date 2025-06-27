# 🤖 AI-Powered Deepfake Detection & Media Authentication System

A comprehensive full-stack system for detecting deepfake images, videos, and audio using advanced AI models and traditional computer vision techniques.

## 🚀 Features

- **Multi-Modal Detection**: Images, videos, and audio analysis
- **Real AI Models**: Hugging Face integration with ResNet-50 and custom heuristics
- **Traditional CV**: Fallback analysis using computer vision techniques
- **Real-time Processing**: Background processing with status updates
- **Modern UI**: React frontend with Tailwind CSS
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Database**: MongoDB for persistent storage
- **Monitoring**: Prometheus and Grafana integration
- **Docker Support**: Containerized deployment
- **CI/CD Ready**: GitHub Actions workflow

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │   MongoDB       │
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│  AI Models      │◄─────────────┘
                        │  • Hugging Face │
                        │  • ResNet-50    │
                        │  • CV Analysis  │
                        └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database
- **Hugging Face** - Pre-trained AI models
- **OpenCV** - Computer vision processing
- **Librosa** - Audio analysis
- **PyTorch** - Deep learning framework

### Frontend
- **React** - JavaScript framework
- **Tailwind CSS** - Utility-first CSS
- **Axios** - HTTP client
- **React Router** - Navigation

### DevOps
- **Docker** - Containerization
- **Prometheus** - Monitoring
- **Grafana** - Visualization
- **GitHub Actions** - CI/CD

## 📦 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB
- Docker (optional)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/deepfake-detection-system.git
cd deepfake-detection-system
```

### 2. Automated Setup
```bash
# Run the complete setup script
chmod +x setup_all.sh
./setup_all.sh
```

### 3. Manual Setup (Alternative)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
npm install
```

#### Database Setup
```bash
# Install MongoDB (macOS)
brew install mongodb-community@6.0
brew services start mongodb-community@6.0

# Or use Docker
docker run -d -p 27017:27017 --name mongodb mongo:6.0
```

### 4. Start Services
```bash
# Start all services
./start_servers.sh

# Or start individually
./start_backend.sh
./start_frontend.sh
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Monitoring**: http://localhost:9090 (Prometheus)

## 🚀 Deployment

### GitHub Repository Setup

1. **Initialize Git Repository**
```bash
git init
git add .
git commit -m "Initial commit: Deepfake Detection System"
```

2. **Create GitHub Repository**
- Go to GitHub.com
- Create a new repository
- Follow the instructions to push your code

3. **Push to GitHub**
```bash
git remote add origin https://github.com/yourusername/deepfake-detection-system.git
git branch -M main
git push -u origin main
```

### Docker Deployment

1. **Build and Run with Docker Compose**
```bash
docker-compose up -d
```

2. **Production Docker Setup**
```bash
# Build production images
docker build -f backend/Dockerfile -t deepfake-backend .
docker build -f frontend/Dockerfile -t deepfake-frontend .

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment Options

#### Heroku
```bash
# Install Heroku CLI
heroku create your-deepfake-app
heroku addons:create mongolab:sandbox
git push heroku main
```

#### AWS (ECS/Fargate)
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker tag deepfake-backend:latest your-account.dkr.ecr.us-east-1.amazonaws.com/deepfake-backend:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/deepfake-backend:latest
```

#### Google Cloud (GKE)
```bash
# Deploy to GKE
gcloud container clusters create deepfake-cluster --num-nodes=3
kubectl apply -f k8s/
```

#### Azure (AKS)
```bash
# Create AKS cluster
az aks create --resource-group myResourceGroup --name deepfakeCluster --node-count 3
az aks get-credentials --resource-group myResourceGroup --name deepfakeCluster
kubectl apply -f k8s/
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
MONGODB_URL=mongodb://localhost:27017/deepfake_detection
DATABASE_NAME=deepfake_detection

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000"]

# ML Models
MODEL_CACHE_DIR=./ml_models
HUGGINGFACE_CACHE_DIR=./cache

# File Upload
MAX_FILE_SIZE=100MB
UPLOAD_DIR=./uploads

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
```

## 📊 API Documentation

### Core Endpoints

- `POST /api/v1/` - Upload and analyze media files
- `GET /api/v1/{file_id}` - Get analysis results
- `GET /api/v1/logs/` - Get analysis history
- `GET /api/v1/models/` - Get available models
- `GET /health` - Health check

### Example Usage

```bash
# Upload and analyze an image
curl -X POST -F "file=@image.jpg" http://localhost:8000/api/v1/

# Get analysis results
curl http://localhost:8000/api/v1/{file_id}

# Get analysis logs
curl http://localhost:8000/api/v1/logs/
```

## 🤖 AI Models

### Image Analysis
- **Hugging Face ResNet-50**: Pre-trained model with custom heuristics
- **Traditional CV**: Compression artifacts, noise patterns, color consistency
- **Face Detection**: Face recognition and artifact analysis

### Video Analysis
- **Frame Extraction**: Temporal analysis of video frames
- **Temporal Consistency**: Analysis of frame-to-frame consistency
- **Multi-frame Aggregation**: Combined analysis of multiple frames

### Audio Analysis
- **Spectral Analysis**: MFCC, spectral centroid, rolloff
- **Phase Analysis**: Phase consistency and discontinuities
- **Artifact Detection**: Audio compression and manipulation artifacts

## 📈 Monitoring & Analytics

### Prometheus Metrics
- Request rates and response times
- Model prediction accuracy
- System resource usage
- Error rates and types

### Grafana Dashboards
- Real-time system performance
- Model accuracy trends
- User activity analytics
- System health monitoring

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
./run_integration_tests.sh
```

## 🔧 Configuration

### Backend Configuration
```python
# backend/app/core/config.py
class Settings:
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "deepfake_detection"
```

### Frontend Configuration
```javascript
// frontend/src/config.js
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const UPLOAD_ENDPOINT = `${API_BASE_URL}/api/v1/`;
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for pre-trained models
- OpenCV for computer vision capabilities
- FastAPI for the excellent web framework
- React and Tailwind CSS for the frontend

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/deepfake-detection-system/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/deepfake-detection-system/wiki)
- **Email**: support@yourdomain.com

## 🔄 Version History

- **v1.0.0** - Initial release with basic deepfake detection
- **v1.1.0** - Added video and audio analysis
- **v1.2.0** - Hugging Face model integration
- **v1.3.0** - Production deployment support

---

**Made with ❤️ for a safer digital world** 