# 🚀 Complete Deployment Guide - DeepShield

**Deploy both backend and frontend in minutes!**

---

## Quick Start

### 1️⃣ Deploy Backend (5 minutes)

**Option A: Railway (Easiest)**
```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Navigate to backend
cd Imageverify

# Deploy
railway init
railway up
```

**Option B: Render**
1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repo
4. Select `Imageverify` folder
5. Build: `pip install -r requirements.txt`
6. Start: `python main.py`
7. Add environment variables (see below)
8. Deploy!

### 2️⃣ Get Backend URL

After deployment, you'll get a URL like:
- Railway: `https://your-app.up.railway.app`
- Render: `https://your-app.onrender.com`

**Save this URL!**

### 3️⃣ Deploy Frontend (5 minutes)

```powershell
cd aptos-verifier-frontend

# Install Vercel CLI if needed
npm install -g vercel

# Deploy
vercel --prod
```

### 4️⃣ Configure Environment Variables

**Backend (Railway/Render Dashboard):**
```
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
HOST=0.0.0.0
PORT=8000
```

**Frontend (Vercel Dashboard):**
```
NEXT_PUBLIC_API_URL=https://your-backend-url.up.railway.app
```

### 5️⃣ Test!

1. Visit your frontend URL
2. Upload an image
3. Verify it works! ✅

---

## Detailed Steps

See `Imageverify/DEPLOY_COMPLETE.md` for detailed instructions.

---

## Environment Variables Reference

### Backend
- `ALLOWED_ORIGINS`: Comma-separated frontend URLs
- `HOST`: Server host (0.0.0.0)
- `PORT`: Server port (8000)

### Frontend
- `NEXT_PUBLIC_API_URL`: Your backend API URL

---

## Troubleshooting

**Backend not accessible?**
- Check environment variables
- Verify deployment logs
- Test with: `curl https://your-backend-url/`

**Frontend can't connect?**
- Verify `NEXT_PUBLIC_API_URL` is set
- Check backend `ALLOWED_ORIGINS` includes frontend URL
- Redeploy after changing env vars

---

## Need Help?

See `Imageverify/DEPLOY_COMPLETE.md` for comprehensive guide.

