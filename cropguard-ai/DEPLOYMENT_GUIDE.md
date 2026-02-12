# Deployment Guide - Push to GitHub & Deploy to Vercel

## 📋 Prerequisites Checklist

Before deploying, make sure:
- ✅ Backend is running without errors
- ✅ Frontend works correctly (login, upload, predictions)
- ✅ All features tested locally
- ✅ Git is installed and configured

---

## 🚀 Step 1: Push Code to GitHub

### 1.1 Check Current Status

```bash
# Navigate to project directory
cd "c:\Users\chara\OneDrive\Desktop\jyothi project\AID103-Jyothi-ch-tech"

# Check git status
git status

# Check current branch
git branch
```

### 1.2 Stage All Changes

```bash
# Add all modified and new files
git add .

# Or add specific directories
git add cropguard-ai/
```

### 1.3 Commit Changes

```bash
# Commit with a descriptive message
git commit -m "feat: Complete CropGuard AI with multi-page flow and AI predictions

- Implemented multi-page architecture (auth + dashboard)
- Added improved AI prediction service with 38 disease classes
- Created comprehensive recommendation system
- Updated frontend with modern UI/UX
- Fixed model loading and prediction issues"
```

### 1.4 Push to Main Branch

```bash
# Push to main branch
git push origin main

# If you get an error about upstream, use:
git push -u origin main
```

**If you encounter authentication issues:**
- Use GitHub Personal Access Token instead of password
- Or use GitHub Desktop for easier authentication

---

## 🌐 Step 2: Deploy Backend to Render/Railway (Recommended)

**Note**: Vercel is primarily for frontend. For the Flask backend, use Render or Railway.

### Option A: Deploy Backend to Render

1. **Go to**: https://render.com
2. **Sign up/Login** with GitHub
3. **Click**: "New +" → "Web Service"
4. **Connect** your GitHub repository
5. **Configure**:
   - **Name**: `cropguard-ai-backend`
   - **Root Directory**: `cropguard-ai/backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

6. **Environment Variables** (Add these):
   ```
   PYTHON_VERSION=3.12
   PORT=5000
   ```

7. **Click**: "Create Web Service"
8. **Wait** for deployment (5-10 minutes)
9. **Copy** the backend URL (e.g., `https://cropguard-ai-backend.onrender.com`)

### Option B: Deploy Backend to Railway

1. **Go to**: https://railway.app
2. **Sign up/Login** with GitHub
3. **Click**: "New Project" → "Deploy from GitHub repo"
4. **Select** your repository
5. **Configure**:
   - **Root Directory**: `cropguard-ai/backend`
   - **Start Command**: `gunicorn app:app`
6. **Deploy** and copy the URL

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Update Frontend API URL

Before deploying, update the API URL in your frontend:

**Edit**: `cropguard-ai/frontend/auth.js` and `cropguard-ai/frontend/dashboard.js`

```javascript
// Change this line:
const API = "http://127.0.0.1:5000";

// To your deployed backend URL:
const API = "https://cropguard-ai-backend.onrender.com";
```

**Commit this change:**
```bash
git add cropguard-ai/frontend/auth.js cropguard-ai/frontend/dashboard.js
git commit -m "Update API URL for production"
git push origin main
```

### 3.2 Deploy to Vercel

1. **Go to**: https://vercel.com
2. **Sign up/Login** with GitHub
3. **Click**: "Add New" → "Project"
4. **Import** your GitHub repository
5. **Configure**:
   - **Framework Preset**: Other
   - **Root Directory**: `cropguard-ai/frontend`
   - **Build Command**: (leave empty)
   - **Output Directory**: `.` (current directory)
   - **Install Command**: (leave empty)

6. **Click**: "Deploy"
7. **Wait** for deployment (1-2 minutes)
8. **Your app is live!** Copy the URL (e.g., `https://cropguard-ai.vercel.app`)

---

## 🔧 Step 4: Configure CORS (Important!)

After deploying, update your backend CORS settings:

**Edit**: `cropguard-ai/backend/app.py`

```python
from flask_cors import CORS

# Update CORS to allow your Vercel domain
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:*",
            "http://127.0.0.1:*",
            "https://cropguard-ai.vercel.app",  # Your Vercel URL
            "https://*.vercel.app"  # All Vercel preview deployments
        ]
    }
})
```

**Push the update:**
```bash
git add cropguard-ai/backend/app.py
git commit -m "Update CORS for production"
git push origin main
```

Render/Railway will auto-deploy the update.

---

## ✅ Step 5: Test Your Deployed App

1. **Visit** your Vercel URL
2. **Test**:
   - ✅ Registration/Login
   - ✅ Image upload
   - ✅ Disease prediction
   - ✅ Recommendations display
   - ✅ Logout

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch" or CORS errors
**Solution**: 
- Check CORS configuration in backend
- Verify backend URL in frontend is correct
- Check browser console for specific errors

### Issue: Backend not responding
**Solution**:
- Check Render/Railway logs
- Verify `gunicorn` is installed in `requirements.txt`
- Check if backend is sleeping (free tier sleeps after inactivity)

### Issue: Images not uploading
**Solution**:
- Vercel has file size limits (4.5MB for free tier)
- Consider using cloud storage (AWS S3, Cloudinary) for images

---

## 📝 Quick Command Reference

```bash
# Check status
git status

# Stage all changes
git add .

# Commit
git commit -m "your message"

# Push to main
git push origin main

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

## 🎯 Next Steps After Deployment

1. **Custom Domain** (Optional):
   - Add custom domain in Vercel settings
   - Update DNS records

2. **Environment Variables**:
   - Add sensitive data (API keys, DB URLs) in Vercel/Render dashboard
   - Never commit secrets to Git

3. **Monitoring**:
   - Set up error tracking (Sentry)
   - Monitor backend logs in Render/Railway

4. **Database** (Future):
   - Set up MongoDB Atlas
   - Add connection string to environment variables

---

## 🆘 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app

Good luck with your deployment! 🚀
