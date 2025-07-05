# 🚀 Quick Render Deployment

## ⚡ Immediate Steps (5 minutes)

### 1. Get Your MongoDB Atlas URL
- Go to: https://cloud.mongodb.com
- Click "Connect" → "Connect your application"
- Copy the connection string

### 2. Update render.yaml
Replace `YOUR_MONGODB_ATLAS_URL_HERE` with your actual MongoDB Atlas connection string.

### 3. Deploy on Render
1. Go to: https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repo: `deepfake-detection-system`
4. Click "Connect"
5. **IMPORTANT**: Update `MONGODB_URL` in backend environment variables
6. Click "Create Blueprint"
7. Wait 5-10 minutes

## ✅ Expected Results

- **Backend**: https://deepfake-backend.onrender.com
- **Frontend**: https://deepfake-frontend.onrender.com
- **API Docs**: https://deepfake-backend.onrender.com/docs

## 🎯 Test Your Deployment

1. Visit the frontend URL
2. Upload a test image
3. Check if deepfake detection works
4. Verify results are displayed

## 📞 Need Help?

- Check `RENDER_DEPLOYMENT_GUIDE.md` for detailed instructions
- Use `DEPLOYMENT_CHECKLIST.md` to track progress
- Check Render logs if something fails

---

**Your project is ready to deploy! 🎉** 