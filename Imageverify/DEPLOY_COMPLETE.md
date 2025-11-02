# Complete Deployment Guide - DeepShield Full Stack

This guide will help you deploy **both** the backend API and frontend website to production.

---

## Table of Contents

1. [Backend Deployment](#backend-deployment)
2. [Frontend Deployment](#frontend-deployment)
3. [Configuration](#configuration)
4. [Testing](#testing)

---

## Backend Deployment

### Option 1: Deploy to Railway (Recommended - Easiest)

**Railway** is one of the easiest platforms for deploying Python APIs.

#### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create a new project

#### Step 2: Deploy from GitHub

1. Connect your GitHub repository
2. Railway will automatically detect the Dockerfile
3. Add environment variables (see Configuration section)
4. Deploy!

#### Step 3: Get Your Backend URL

After deployment, Railway will give you a URL like:
`https://your-app-name.up.railway.app`

**Save this URL** - you'll need it for the frontend!

---

### Option 2: Deploy to Render

#### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub

#### Step 2: Deploy

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Select the `Imageverify` directory
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. Add environment variables (see Configuration section)
6. Deploy!

#### Step 3: Get Your Backend URL

After deployment, Render will give you a URL like:
`https://your-app-name.onrender.com`

---

### Option 3: Deploy to Your Own Server/VPS

#### Prerequisites

- VPS or server with Python 3.8+
- SSH access

#### Step 1: Upload Code

```bash
# Upload your Imageverify folder to the server
scp -r Imageverify user@your-server:/opt/deepshield/
```

#### Step 2: Install Dependencies

```bash
ssh user@your-server
cd /opt/deepshield/Imageverify
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 3: Set Up Process Manager (PM2 or systemd)

**Using PM2:**
```bash
npm install -g pm2
pm2 start main.py --name deepshield-api --interpreter python3
pm2 save
pm2 startup
```

**Using systemd:**
Create `/etc/systemd/system/deepshield-api.service`:
```ini
[Unit]
Description=DeepShield API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/opt/deepshield/Imageverify
Environment="PATH=/opt/deepshield/Imageverify/venv/bin"
ExecStart=/opt/deepshield/Imageverify/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable deepshield-api
sudo systemctl start deepshield-api
```

#### Step 4: Set Up Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/deepshield-api`:
```nginx
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/deepshield-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Frontend Deployment

### Deploy to Vercel (Recommended)

#### Step 1: Install Vercel CLI

```powershell
npm install -g vercel
```

#### Step 2: Deploy

```powershell
cd aptos-verifier-frontend
vercel --prod
```

#### Step 3: Configure Environment Variables

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your backend URL (e.g., `https://your-app-name.up.railway.app`)
   - **Environment**: Production, Preview, Development

#### Step 4: Redeploy

After adding environment variables, trigger a redeploy:
```powershell
vercel --prod
```

Or push a new commit to trigger automatic deployment.

---

## Configuration

### Backend Environment Variables

Set these in your hosting platform's dashboard:

| Variable | Description | Example |
|----------|-------------|---------|
| `HOST` | Server host (0.0.0.0 for all interfaces) | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed frontend URLs | `https://your-frontend.vercel.app,http://localhost:3000` |

**For Railway:**
- Go to your project → Variables tab
- Add each variable

**For Render:**
- Go to your service → Environment tab
- Add each variable

**For VPS:**
- Add to systemd service file or `.env` file

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-api.railway.app` |

**For Vercel:**
- Settings → Environment Variables

---

## Quick Deployment Checklist

### Backend
- [ ] Backend deployed to hosting platform
- [ ] Environment variables set (HOST, PORT, ALLOWED_ORIGINS)
- [ ] Backend URL obtained and saved
- [ ] Backend accessible (test with curl or browser)
- [ ] CORS configured correctly

### Frontend
- [ ] Frontend deployed to Vercel
- [ ] `NEXT_PUBLIC_API_URL` environment variable set
- [ ] Frontend URL obtained
- [ ] Frontend can connect to backend (test upload)

### Both
- [ ] Test end-to-end workflow
- [ ] Verify blockchain transactions
- [ ] Check error handling
- [ ] Monitor logs

---

## Testing After Deployment

### 1. Test Backend

```bash
# Test health endpoint
curl https://your-backend-url/

# Test upload (replace with actual file)
curl -X POST https://your-backend-url/verify \
  -F "file=@test-image.jpg"
```

### 2. Test Frontend

1. Visit your frontend URL
2. Upload an image or audio file
3. Verify the result appears
4. Check that blockchain transaction link works

### 3. Test Full Flow

1. Upload from frontend
2. Check backend logs
3. Verify transaction on Aptos Explorer
4. Confirm verdict is recorded

---

## Troubleshooting

### Backend Issues

**Issue: CORS errors**
- Check `ALLOWED_ORIGINS` includes your frontend URL
- Ensure no trailing slashes in URLs
- Verify frontend URL matches exactly

**Issue: Module not found**
- Check `aptos_service.py` has correct `MODULE_ADDRESS_STR`
- Verify private key is correct
- Ensure network URL is correct

**Issue: Server not starting**
- Check logs in hosting platform
- Verify all dependencies installed
- Check Python version (needs 3.8+)

### Frontend Issues

**Issue: Can't connect to backend**
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend is running and accessible
- Test backend URL directly

**Issue: Environment variable not working**
- Ensure variable starts with `NEXT_PUBLIC_`
- Redeploy after changing variables
- Check browser console for errors

---

## Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Environment variables configured
- [ ] CORS properly configured
- [ ] SSL/HTTPS enabled (automatic on Railway/Render/Vercel)
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up (optional)
- [ ] Error logging configured (optional)
- [ ] Backup strategy (optional)

---

## Support

For issues:
1. Check hosting platform logs
2. Verify all environment variables
3. Test backend independently
4. Check browser console for frontend errors
5. Verify blockchain transactions on explorer

---

## Next Steps After Deployment

1. **Monitor Performance**: Watch response times and errors
2. **Set Up Alerts**: Get notified of issues
3. **Scale If Needed**: Add more resources if traffic increases
4. **Optimize**: Improve response times based on usage
5. **Add Features**: Enhance based on user feedback

