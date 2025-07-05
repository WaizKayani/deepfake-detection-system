# 🚀 Render Deployment Guide for Deepfake Detection System

## 📋 Prerequisites

- ✅ GitHub repository with your code
- ✅ MongoDB Atlas database set up
- ✅ Render account (free at [render.com](https://render.com))

## 🔧 Step 1: Prepare Your MongoDB Atlas Connection

1. **Go to MongoDB Atlas Dashboard**
   - Visit: https://cloud.mongodb.com
   - Select your cluster

2. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string

3. **Format Your Connection String**
   ```
   mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority
   ```
   - Replace `username` with your Atlas username
   - Replace `password` with your Atlas password
   - Replace `database` with your database name

## 🎯 Step 2: Update Configuration

### Update render.yaml
Replace `YOUR_MONGODB_ATLAS_URL_HERE` in `render.yaml` with your actual MongoDB Atlas connection string.

## 🌐 Step 3: Deploy on Render

### 3.1 Create Render Account
1. Go to [render.com](https://render.com)
2. Click "Get Started"
3. Sign up with your GitHub account

### 3.2 Deploy Using Blueprint
1. **Click "New +"** in Render dashboard
2. **Select "Blueprint"**
3. **Connect your GitHub repository**
   - Click "Connect account" if not already connected
   - Select your repository: `deepfake-detection-system`
   - Click "Connect"

### 3.3 Configure Services
Render will automatically detect your `render.yaml` and show:

**Backend Service Configuration:**
- ✅ **Name**: `deepfake-backend`
- ✅ **Environment**: Python
- ✅ **Build Command**: `cd backend && pip install -r requirements.txt`
- ✅ **Start Command**: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Frontend Service Configuration:**
- ✅ **Name**: `deepfake-frontend`
- ✅ **Environment**: Static Site
- ✅ **Build Command**: `cd frontend && npm install && npm run build`
- ✅ **Publish Directory**: `./frontend/build`

### 3.4 Set Environment Variables
**CRITICAL**: You must update the MongoDB URL:

1. **Click on the backend service** (`deepfake-backend`)
2. **Go to "Environment" tab**
3. **Find `MONGODB_URL`**
4. **Replace the placeholder** with your actual MongoDB Atlas connection string
5. **Click "Save Changes"**

### 3.5 Deploy
1. **Click "Create Blueprint"**
2. **Wait for deployment** (5-10 minutes)
3. **Both services will deploy automatically**

## ✅ Step 4: Verify Deployment

### 4.1 Check Backend Health
- **URL**: https://deepfake-backend.onrender.com
- **Health Check**: https://deepfake-backend.onrender.com/health
- **API Documentation**: https://deepfake-backend.onrender.com/docs

### 4.2 Check Frontend
- **URL**: https://deepfake-frontend.onrender.com
- **Test**: Upload an image/video to test the system

### 4.3 Test Integration
1. **Open the frontend URL**
2. **Upload a test image**
3. **Check if it connects to the backend**
4. **Verify results are displayed**

## 🔧 Step 5: Environment Variables Reference

### Backend Environment Variables
```yaml
MONGODB_URL: "your_mongodb_atlas_connection_string"
DATABASE_NAME: "deepfake_detection"
API_HOST: "0.0.0.0"
DEBUG: "False"
SECRET_KEY: "auto_generated"
CORS_ORIGINS: "https://deepfake-frontend.onrender.com"
MAX_FILE_SIZE: "104857600"
UPLOAD_DIR: "./uploads"
MODEL_CACHE_DIR: "./ml_models"
HUGGINGFACE_CACHE_DIR: "./cache"
```

### Frontend Environment Variables
```yaml
REACT_APP_API_URL: "https://deepfake-backend.onrender.com"
REACT_APP_ENVIRONMENT: "production"
```

## 🚨 Troubleshooting

### Backend Deployment Issues

**Problem**: Build fails during pip install
**Solution**: 
- Check if all dependencies are in `backend/requirements.txt`
- Ensure Python version compatibility

**Problem**: Service fails to start
**Solution**:
- Check logs in Render dashboard
- Verify MongoDB connection string
- Ensure all environment variables are set

**Problem**: CORS errors
**Solution**:
- Verify `CORS_ORIGINS` includes your frontend URL
- Check if backend is accessible

### Frontend Deployment Issues

**Problem**: Build fails
**Solution**:
- Check if all dependencies are in `frontend/package.json`
- Ensure Node.js version compatibility
- Check for TypeScript errors

**Problem**: Can't connect to backend
**Solution**:
- Verify `REACT_APP_API_URL` is correct
- Check if backend is running
- Ensure CORS is configured properly

### Database Issues

**Problem**: Can't connect to MongoDB
**Solution**:
- Verify MongoDB Atlas connection string
- Check if IP whitelist includes Render's IPs
- Ensure database user has correct permissions

## 📊 Monitoring and Logs

### View Logs
1. **Go to Render Dashboard**
2. **Click on your service**
3. **Go to "Logs" tab**
4. **Monitor real-time logs**

### Health Checks
- **Backend Health**: `GET /health`
- **API Status**: `GET /`
- **Documentation**: `GET /docs`

## 🔄 Updating Your Deployment

### Automatic Updates
- Render automatically redeploys when you push to your GitHub repository
- No manual intervention required

### Manual Updates
1. **Make changes to your code**
2. **Commit and push to GitHub**
3. **Render will automatically redeploy**

## 💰 Cost Considerations

### Free Tier Limits
- **Web Services**: 750 hours/month
- **Static Sites**: Unlimited
- **Bandwidth**: 100GB/month

### Paid Plans
- **Starter**: $7/month per service
- **Standard**: $25/month per service
- **Pro**: $50/month per service

## 🎯 Expected URLs After Deployment

- **Backend API**: https://deepfake-backend.onrender.com
- **Frontend App**: https://deepfake-frontend.onrender.com
- **API Documentation**: https://deepfake-backend.onrender.com/docs
- **Health Check**: https://deepfake-backend.onrender.com/health

## 📞 Support

If you encounter issues:
1. **Check Render logs** first
2. **Verify environment variables**
3. **Test locally** to isolate issues
4. **Check Render documentation**: https://render.com/docs

---

**🎉 Congratulations!** Your Deepfake Detection System is now deployed on Render! 