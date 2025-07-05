# 🚀 Fly.io Deployment Guide

## 📋 Why Fly.io?

Fly.io is an **excellent choice** for your Deepfake Detection System because:

✅ **Free Tier**: 3 shared-cpu VMs (generous!)  
✅ **Global Deployment**: Multiple regions worldwide  
✅ **Python Support**: Perfect for FastAPI  
✅ **PostgreSQL**: Free database included  
✅ **File Storage**: Persistent volumes  
✅ **Background Processing**: Long-running AI tasks  
✅ **Auto-scaling**: Based on demand  
✅ **Docker-based**: Easy deployment  

## 🛠️ Prerequisites

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io)
2. **Fly CLI**: Install the Fly CLI tool
3. **Docker**: Ensure Docker is installed
4. **GitHub Repository**: Your code is already on GitHub

## 🚀 Quick Deployment

### Step 1: Install Fly CLI

```bash
# macOS
brew install flyctl

# Or download from: https://fly.io/docs/hands-on/install-flyctl/
```

### Step 2: Login to Fly.io

```bash
fly auth login
```

### Step 3: Create App

```bash
# Create the app
fly apps create deepfake-detection-system

# Set the primary region (choose closest to you)
fly apps update --primary-region iad
```

### Step 4: Create PostgreSQL Database

```bash
# Create PostgreSQL database
fly postgres create deepfake-db

# Attach to your app
fly postgres attach deepfake-db --app deepfake-detection-system
```

### Step 5: Create Volume for File Storage

```bash
# Create volume for uploads
fly volumes create deepfake_data --size 10 --region iad
```

### Step 6: Set Environment Variables

```bash
# Set environment variables
fly secrets set \
  DATABASE_NAME=deepfake_detection \
  API_HOST=0.0.0.0 \
  DEBUG=False \
  SECRET_KEY=$(openssl rand -hex 32) \
  CORS_ORIGINS=https://deepfake-detection-system.fly.dev \
  MAX_FILE_SIZE=104857600 \
  UPLOAD_DIR=./uploads \
  MODEL_CACHE_DIR=./ml_models \
  HUGGINGFACE_CACHE_DIR=./cache \
  REACT_APP_API_URL=https://deepfake-detection-system.fly.dev \
  REACT_APP_ENVIRONMENT=production
```

### Step 7: Deploy

```bash
# Deploy your application
fly deploy
```

## 🔧 Configuration Details

### Backend Configuration
- **Port**: 8080 (Fly.io standard)
- **Health Check**: `/health` endpoint
- **Memory**: 1024MB (configurable)
- **CPU**: 1 shared CPU

### Frontend Configuration
- **Build**: Static files served by FastAPI
- **Path**: `/frontend/build`
- **Environment**: Production build

### Database Configuration
- **Type**: PostgreSQL
- **Plan**: Free tier
- **Connection**: Automatic via `DATABASE_URL`

### File Storage
- **Volume**: `deepfake_data`
- **Path**: `/app/uploads`
- **Size**: 10GB (configurable)

## 🌐 Access Your App

After deployment:
- **Main App**: `https://deepfake-detection-system.fly.dev`
- **API Docs**: `https://deepfake-detection-system.fly.dev/docs`
- **Health Check**: `https://deepfake-detection-system.fly.dev/health`

## 💰 Cost Breakdown

**Free Tier**:
- **3 shared-cpu VMs**: Free
- **PostgreSQL**: Free (3GB storage)
- **Volume Storage**: Free (3GB)
- **Bandwidth**: Free (160GB/month)
- **Total**: **$0/month** (within free limits!)

## 🔄 Updates

To update your app:
```bash
# Push changes to GitHub
git push origin main

# Deploy to Fly.io
fly deploy
```

## 🆘 Troubleshooting

### Common Issues:

1. **Build fails**:
   ```bash
   fly logs
   fly status
   ```

2. **Database connection**:
   ```bash
   fly postgres connect -a deepfake-db
   ```

3. **Volume issues**:
   ```bash
   fly volumes list
   fly volumes show deepfake_data
   ```

4. **Memory issues**:
   ```bash
   # Scale up memory
   fly scale memory 2048
   ```

### Useful Commands:
```bash
# View logs
fly logs

# SSH into app
fly ssh console

# Check status
fly status

# Scale app
fly scale count 1

# Monitor resources
fly dashboard
```

## 🎯 Advantages of Fly.io

### ✅ **Pros**:
- **Truly Free**: 3 VMs + database + storage
- **Global CDN**: Fast worldwide access
- **Auto-scaling**: Based on demand
- **PostgreSQL**: Better than MongoDB for analytics
- **Docker**: Standard containerization
- **CLI-first**: Developer-friendly

### ⚠️ **Cons**:
- **Learning curve**: CLI-based deployment
- **Database migration**: MongoDB → PostgreSQL
- **Configuration**: More complex than Railway

## 🔄 Migration from MongoDB to PostgreSQL

Since Fly.io uses PostgreSQL, you'll need to:

1. **Update database models** (I can help with this)
2. **Migrate data** (if any)
3. **Update connection strings**

## 🎯 Recommendation

**Fly.io is excellent** if you want:
- ✅ **Truly free hosting**
- ✅ **Global deployment**
- ✅ **Professional features**
- ✅ **Docker-based deployment**

**Railway is better** if you want:
- ✅ **Easier setup**
- ✅ **Web-based deployment**
- ✅ **Keep MongoDB**
- ✅ **Faster initial deployment**

## 🚀 Next Steps

1. **Choose your platform**: Fly.io vs Railway
2. **If Fly.io**: I'll help migrate to PostgreSQL
3. **If Railway**: Use the existing MongoDB setup
4. **Deploy and test**: Both platforms work great!

Which platform would you prefer? I can help with either! 🚀 