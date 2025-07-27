# 🗄️ MongoDB Atlas Setup Guide

## Step-by-Step Setup for Deepfake Detection System

### 1. Create MongoDB Atlas Account
- Visit: https://cloud.mongodb.com/user/signup
- Sign up with your email or GitHub account
- Choose the **FREE** tier (M0 Sandbox)

### 2. Create a Cluster
1. Click "Build a Database"
2. Choose "FREE" tier (M0 Sandbox)
3. Select your preferred cloud provider (AWS, Google Cloud, or Azure)
4. Choose a region close to you
5. Click "Create"

### 3. Set Up Database Access
1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username (e.g., `deepfake_user`)
5. Generate a secure password (save this!)
6. Select "Read and write to any database"
7. Click "Add User"

### 4. Set Up Network Access
1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for Render deployment)
4. Click "Confirm"

### 5. Get Your Connection String
1. Go back to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string

### 6. Format Your Connection String
Replace the placeholder with your actual credentials:

```
mongodb+srv://deepfake_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/deepfake_detection?retryWrites=true&w=majority
```

**Important:**
- Replace `deepfake_user` with your actual username
- Replace `YOUR_PASSWORD` with your actual password
- Replace `cluster0.xxxxx.mongodb.net` with your actual cluster URL
- The database name `deepfake_detection` will be created automatically

### 7. Test Your Connection
Once you have your connection string, we'll test it before deployment.

---

## 🔧 Next Steps After Setup

1. **Update render.yaml** with your connection string
2. **Test the connection** locally
3. **Deploy to Render**

---

## 📋 What You'll Get

- **Free Tier Limits:**
  - 512MB storage
  - Shared RAM
  - Perfect for development and small production apps

- **Features:**
  - Automatic backups
  - Built-in security
  - Global distribution
  - Real-time monitoring

---

## 🚨 Security Notes

- Keep your password secure
- Never commit credentials to Git
- Use environment variables in production
- Consider IP whitelisting for production

---

## 📞 Need Help?

- MongoDB Atlas Documentation: https://docs.atlas.mongodb.com/
- Community Support: https://community.mongodb.com/ 