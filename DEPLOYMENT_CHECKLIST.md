# ✅ Render Deployment Checklist

## Pre-Deployment
- [ ] MongoDB Atlas database created
- [ ] MongoDB connection string ready
- [ ] GitHub repository updated with latest code
- [ ] render.yaml file configured

## Deployment Steps
- [ ] Sign up for Render account
- [ ] Connect GitHub repository to Render
- [ ] Create Blueprint deployment
- [ ] Update MongoDB URL in environment variables
- [ ] Deploy services
- [ ] Wait for deployment to complete (5-10 minutes)

## Post-Deployment Verification
- [ ] Backend health check: https://deepfake-backend.onrender.com/health
- [ ] API documentation: https://deepfake-backend.onrender.com/docs
- [ ] Frontend loads: https://deepfake-frontend.onrender.com
- [ ] Upload test image/video
- [ ] Verify deepfake detection works
- [ ] Check database connection

## Troubleshooting (if needed)
- [ ] Check Render logs
- [ ] Verify environment variables
- [ ] Test MongoDB connection
- [ ] Check CORS configuration
- [ ] Verify file upload limits

## Final URLs
- **Backend**: https://deepfake-backend.onrender.com
- **Frontend**: https://deepfake-frontend.onrender.com
- **API Docs**: https://deepfake-backend.onrender.com/docs

---
**Status**: Ready for deployment! 🚀 