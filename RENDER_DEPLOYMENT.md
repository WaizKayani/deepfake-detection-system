# 🚀 Render Deployment Guide

This guide will help you deploy your Deepfake Detection System to Render's free tier.

## 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **Render CLI**: Install the Render CLI tool
3. **Git**: Ensure Git is installed

## 🛠️ Installation

### 1. Install Render CLI

```bash
# macOS
brew install render

# Or download from: https://render.com/docs/cli
```

### 2. Login to Render

```bash
render login
```

## 🚀 Quick Deployment

### Option 1: Automated Deployment

```bash
# Run the automated deployment script
./deploy_render.sh all
```

### Option 2: Manual Deployment

1. **Initialize Git** (if not already done):
```bash
git init
git add .
git commit -m "Initial commit: Deepfake Detection System"
```

2. **Deploy using Render Blueprint**:
```bash
render blueprint apply render.yaml
```

## 📊 What Gets Deployed

The `render.yaml` file creates:

- **Backend API**: Python FastAPI service
- **Frontend**: React static site
- **Database**: MongoDB instance
- **Environment**: All necessary environment variables

## 🔗 Service URLs

After deployment, your services will be available at:

- **Frontend**: `https://deepfake-frontend.onrender.com`
- **Backend API**: `https://deepfake-backend.onrender.com`
- **API Documentation**: `https://deepfake-backend.onrender.com/docs`

## ⚙️ Environment Variables

The deployment automatically configures:

- `MONGODB_URL`: Connected to Render's MongoDB
- `SECRET_KEY`: Auto-generated secure key
- `CORS_ORIGINS`: Configured for frontend domain
- `DEBUG`: Set to False for production

## 🔄 Updates

To update your deployment:

```bash
# Make your changes
git add .
git commit -m "Update: description of changes"

# Deploy updates
render blueprint apply render.yaml
```

## 📈 Monitoring

Monitor your services in the Render dashboard:

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. View service logs and metrics
3. Check deployment status

## 🆓 Free Tier Limits

Render's free tier includes:

- **Web Services**: 750 hours/month
- **Databases**: 90 days free trial
- **Static Sites**: Unlimited
- **Bandwidth**: 100GB/month

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check the build logs in Render dashboard
   - Ensure all dependencies are in requirements.txt

2. **Database Connection**:
   - Verify MongoDB URL is correctly set
   - Check database is running

3. **CORS Issues**:
   - Ensure CORS_ORIGINS includes your frontend URL
   - Check browser console for errors

### Getting Help

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Render Support**: Available in dashboard
- **Community**: [Render Community](https://community.render.com)

## 🎉 Success!

Once deployed, your Deepfake Detection System will be live and accessible worldwide!

---

**Happy Deploying! 🚀** 