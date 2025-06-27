# 🚀 Railway Deployment Guide

## 📋 Why Railway?

Railway is the **best free option** for your Deepfake Detection System because:

✅ **Free Tier**: $5 credit monthly (enough for your app)  
✅ **Full-Stack Support**: Backend + Frontend + Database  
✅ **Python Support**: Perfect for FastAPI  
✅ **MongoDB**: Built-in database support  
✅ **File Uploads**: Persistent storage  
✅ **Background Processing**: Long-running AI tasks  
✅ **Auto-Deployment**: From GitHub  
✅ **Global CDN**: Fast worldwide access  

## 🛠️ Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code is already on GitHub
3. **Railway CLI** (optional): `npm install -g @railway/cli`

## 🚀 Quick Deployment

### Step 1: Connect to Railway
1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Connect your GitHub account
5. Select: `WaizKayani/deepfake-detection-system`

### Step 2: Configure Services
Railway will automatically detect your project structure and create:

1. **Backend Service** (FastAPI)
   - Environment: Python
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Frontend Service** (React)
   - Environment: Node.js
   - Build Command: `cd frontend && npm install && npm run build`
   - Start Command: `cd frontend && npm start`

3. **Database Service** (MongoDB)
   - Railway will provision a MongoDB instance
   - Connection string automatically set

### Step 3: Set Environment Variables
Railway will automatically set these from your `railway.toml`:

```bash
# Backend
MONGODB_URL={{.Database.DATABASE_URL}}
DATABASE_NAME=deepfake_detection
API_HOST=0.0.0.0
DEBUG=False
SECRET_KEY={{.Secret.SECRET_KEY}}
CORS_ORIGINS={{.Service.FRONTEND_URL}}
MAX_FILE_SIZE=104857600
UPLOAD_DIR=./uploads
MODEL_CACHE_DIR=./ml_models
HUGGINGFACE_CACHE_DIR=./cache

# Frontend
REACT_APP_API_URL={{.Service.BACKEND_URL}}
REACT_APP_ENVIRONMENT=production
```

### Step 4: Deploy
1. Click **"Deploy Now"**
2. Railway will build and deploy all services
3. You'll get public URLs for each service

## 🔧 Manual Configuration (if needed)

### Backend Service
- **Environment**: Python 3.9
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check**: `/health`

### Frontend Service
- **Environment**: Node.js 18
- **Build Command**: `cd frontend && npm install && npm run build`
- **Start Command**: `cd frontend && npm start`

### Database Service
- **Type**: MongoDB
- **Plan**: Free tier (512MB storage)

## 🌐 Access Your App

After deployment, you'll get:
- **Frontend**: `https://your-app-name.railway.app`
- **Backend API**: `https://your-backend-name.railway.app`
- **API Docs**: `https://your-backend-name.railway.app/docs`

## 💰 Cost Breakdown

**Free Tier ($5 credit/month)**:
- Backend: ~$2-3/month
- Frontend: ~$1/month  
- Database: ~$1/month
- **Total**: ~$4-5/month (covered by free credit!)

## 🔄 Updates

To update your app:
1. Push changes to GitHub
2. Railway automatically redeploys
3. Zero downtime updates

## 🆘 Troubleshooting

### Common Issues:
1. **Build fails**: Check Python/Node.js versions
2. **Database connection**: Verify MongoDB URL
3. **File uploads**: Check storage limits
4. **Memory issues**: Optimize AI model loading

### Support:
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Documentation: [docs.railway.app](https://docs.railway.app)

## 🎯 Next Steps

1. **Deploy to Railway** (recommended)
2. **Test all features**: Upload, analyze, dashboard
3. **Monitor usage**: Stay within free tier limits
4. **Scale up**: Upgrade if needed

Railway is perfect for your project! 🚀 