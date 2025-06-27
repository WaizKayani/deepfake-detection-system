# Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you get the Media Authentication System up and running quickly.

## Prerequisites

- **Python 3.9+**
- **Node.js 16+**
- **MongoDB** (or Docker)
- **Git**

## Option 1: Automated Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd deepfake-detection-system
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the application**
   ```bash
   # Terminal 1 - Backend
   ./start_backend.sh
   
   # Terminal 2 - Frontend
   ./start_frontend.sh
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Option 2: Manual Setup

### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp ../env.example .env
   # Edit .env with your settings
   ```

4. **Start backend**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**
   ```bash
   cp ../env.example .env
   # Edit .env with your settings
   ```

3. **Start frontend**
   ```bash
   npm start
   ```

## Option 3: Docker Setup

1. **Start all services**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001 (admin/admin)

## 🧪 Test the System

### Upload a Test File

1. Open http://localhost:3000
2. Click "Upload File"
3. Select an image, video, or audio file
4. Wait for analysis to complete
5. View results with confidence score

### API Testing

1. Open http://localhost:8000/docs
2. Try the `/api/v1/upload/` endpoint
3. Upload a file and get the file ID
4. Use the file ID to check results at `/api/v1/analyze/{file_id}`

### Health Checks

- Backend health: http://localhost:8000/health
- Detailed health: http://localhost:8000/api/v1/health/detailed
- Metrics: http://localhost:8000/metrics

## 📊 Monitoring

### Prometheus Metrics
- Access: http://localhost:9090
- View system metrics and performance data

### Grafana Dashboards
- Access: http://localhost:3001
- Username: `admin`
- Password: `admin`
- View pre-configured dashboards

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Database
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=deepfake_detection

# File Upload
MAX_FILE_SIZE=100MB
UPLOAD_DIR=./uploads

# Model Settings
CONFIDENCE_THRESHOLD=0.7
```

### Supported File Types

**Images**: JPG, JPEG, PNG, BMP, TIFF
**Videos**: MP4, AVI, MOV, MKV, WEBM
**Audio**: WAV, MP3, FLAC, M4A, AAC

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port
   lsof -i :8000
   # Kill process
   kill -9 <PID>
   ```

2. **MongoDB connection failed**
   ```bash
   # Start MongoDB
   mongod
   # Or use Docker
   docker run -d -p 27017:27017 mongo:6.0
   ```

3. **Frontend can't connect to backend**
   - Check CORS settings in backend `.env`
   - Ensure backend is running on correct port
   - Check network connectivity

4. **File upload fails**
   - Check file size limits
   - Verify file type is supported
   - Ensure upload directory exists and is writable

### Logs

- **Backend logs**: Check terminal output or `logs/` directory
- **Frontend logs**: Check browser console
- **Docker logs**: `docker-compose logs <service-name>`

## 📚 Next Steps

1. **Read the full documentation**
   - [README.md](README.md) - Complete project overview
   - [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
   - [docs/API.md](docs/API.md) - API documentation

2. **Explore the codebase**
   - Backend: `backend/app/` - FastAPI application
   - Frontend: `frontend/src/` - React components
   - Tests: `backend/tests/` - Test suites

3. **Customize the system**
   - Add new ML models
   - Modify UI components
   - Extend API endpoints
   - Configure monitoring

4. **Deploy to production**
   - Set up cloud infrastructure
   - Configure SSL certificates
   - Set up monitoring and alerting
   - Implement backup strategies

## 🆘 Support

- **Issues**: Create a GitHub issue
- **Documentation**: Check the docs folder
- **Community**: Join our discussions

---

**Happy detecting! 🕵️‍♂️** 