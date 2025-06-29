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


### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Monitoring**: http://localhost:9090 (Prometheus)


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


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for pre-trained models
- OpenCV for computer vision capabilities
- FastAPI for the excellent web framework
- React and Tailwind CSS for the frontend


## 🔄 Version History

- **v1.0.0** - Initial release with basic deepfake detection
- **v1.1.0** - Added video and audio analysis
- **v1.2.0** - Hugging Face model integration
- **v1.3.0** - Production deployment support

---
<img width="1710" alt="Screenshot 2025-06-27 at 3 01 53 PM" src="https://github.com/user-attachments/assets/9be7d6be-42f7-4939-8310-f22cfdc49e25" />

**Made with ❤️ for a safer digital world** 



