# Quick Deployment Steps

## 🚀 Step-by-Step Commands (Copy & Paste)

### Step 1: Add All Changes to Git
```bash
cd "c:\Users\chara\OneDrive\Desktop\jyothi project\AID103-Jyothi-ch-tech"
git add .
```

### Step 2: Commit Changes
```bash
git commit -m "Complete CropGuard AI with multi-page flow and AI predictions"
```

### Step 3: Push to GitHub
```bash
git push origin main
```

**If you get authentication error**, use GitHub Desktop or create a Personal Access Token.

---

## 🌐 After Pushing to GitHub

### Deploy Backend (Choose ONE):

**Option A: Render** (Recommended - Easier)
1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Select your repository
5. Settings:
   - **Root Directory**: `cropguard-ai/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"
7. **Copy the URL** (e.g., `https://cropguard-ai-xxx.onrender.com`)

**Option B: Railway**
1. Go to https://railway.app
2. Sign in with GitHub
3. "New Project" → "Deploy from GitHub"
4. Select repository
5. Set root directory: `cropguard-ai/backend`
6. Deploy and copy URL

### Deploy Frontend (Vercel):

1. Go to https://vercel.com
2. Sign in with GitHub
3. "Add New" → "Project"
4. Import your repository
5. Settings:
   - **Root Directory**: `cropguard-ai/frontend`
   - Leave other settings as default
6. Click "Deploy"
7. Done! Your frontend is live

### Update Frontend API URL:

After deploying backend, update these files:

**File 1**: `cropguard-ai/frontend/auth.js`
**File 2**: `cropguard-ai/frontend/dashboard.js`

Change:
```javascript
const API = "http://127.0.0.1:5000";
```

To:
```javascript
const API = "https://your-backend-url.onrender.com";  // Your actual backend URL
```

Then push again:
```bash
git add cropguard-ai/frontend/auth.js cropguard-ai/frontend/dashboard.js
git commit -m "Update API URL for production"
git push origin main
```

Vercel will auto-deploy the update!

---

## ✅ That's It!

Your app is now live on:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.onrender.com`

Test it and enjoy! 🎉
