# Backend Deployment Script for Railway
Write-Host "=== DeepShield Backend Deployment to Railway ===" -ForegroundColor Cyan
Write-Host ""

# Check if Railway CLI is installed
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue

if (-not $railwayInstalled) {
    Write-Host "Railway CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g @railway/cli
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install Railway CLI" -ForegroundColor Red
        Write-Host "Please install manually: npm install -g @railway/cli" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "✅ Railway CLI ready" -ForegroundColor Green
Write-Host ""

# Check if already logged in
Write-Host "Checking Railway authentication..." -ForegroundColor Yellow
$railwayCheck = railway whoami 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Not logged in to Railway" -ForegroundColor Yellow
    Write-Host "Please login:" -ForegroundColor Cyan
    railway login
}

Write-Host ""

# Check if project is initialized
if (-not (Test-Path ".railway")) {
    Write-Host "Initializing Railway project..." -ForegroundColor Yellow
    railway init
}

Write-Host ""
Write-Host "🚀 Deploying to Railway..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Important: After deployment, set these environment variables in Railway dashboard:" -ForegroundColor Yellow
Write-Host "  1. ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000" -ForegroundColor Cyan
Write-Host "  2. HOST = 0.0.0.0" -ForegroundColor Cyan
Write-Host "  3. PORT = 8000" -ForegroundColor Cyan
Write-Host ""

# Deploy
railway up

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Go to Railway dashboard: https://railway.app/dashboard" -ForegroundColor Cyan
    Write-Host "2. Select your project" -ForegroundColor Cyan
    Write-Host "3. Go to Variables tab" -ForegroundColor Cyan
    Write-Host "4. Add environment variables (see list above)" -ForegroundColor Cyan
    Write-Host "5. Copy your app URL (e.g., https://your-app.up.railway.app)" -ForegroundColor Cyan
    Write-Host "6. Use this URL for NEXT_PUBLIC_API_URL in frontend" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
}

