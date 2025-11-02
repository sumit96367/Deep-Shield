# Complete Deployment Script - DeepShield
Write-Host "=== Complete DeepShield Deployment ===" -ForegroundColor Cyan
Write-Host "This script will help you deploy both backend and frontend`n" -ForegroundColor Yellow

Write-Host "Choose deployment method:" -ForegroundColor Yellow
Write-Host "1. Railway (Backend) + Vercel (Frontend) - Recommended" -ForegroundColor Green
Write-Host "2. Render (Backend) + Vercel (Frontend)" -ForegroundColor Green
Write-Host "3. Manual deployment guide" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`n=== Deploying Backend to Railway ===" -ForegroundColor Cyan
        cd Imageverify
        .\deploy-backend-railway.ps1
        
        Write-Host "`n`n=== Backend URL ===" -ForegroundColor Yellow
        Write-Host "After Railway deployment, copy your backend URL" -ForegroundColor Cyan
        $backendUrl = Read-Host "Paste your backend URL here"
        
        Write-Host "`n=== Deploying Frontend to Vercel ===" -ForegroundColor Cyan
        cd ..\aptos-verifier-frontend
        Write-Host "Setting up environment variable..." -ForegroundColor Yellow
        
        # Create .env.production for Vercel
        "NEXT_PUBLIC_API_URL=$backendUrl" | Out-File -FilePath ".env.production" -Encoding UTF8
        
        Write-Host "✅ Environment variable saved to .env.production" -ForegroundColor Green
        Write-Host "`nDeploying to Vercel..." -ForegroundColor Cyan
        .\deploy-vercel.ps1
        
        Write-Host "`n✅ Complete!" -ForegroundColor Green
        Write-Host "Don't forget to add NEXT_PUBLIC_API_URL in Vercel dashboard too!" -ForegroundColor Yellow
    }
    "2" {
        Write-Host "`n=== Render + Vercel Deployment ===" -ForegroundColor Cyan
        Write-Host "`nFor Render deployment:" -ForegroundColor Yellow
        Write-Host "1. Go to https://render.com" -ForegroundColor Cyan
        Write-Host "2. New → Web Service" -ForegroundColor Cyan
        Write-Host "3. Connect GitHub repo" -ForegroundColor Cyan
        Write-Host "4. Select Imageverify folder" -ForegroundColor Cyan
        Write-Host "5. Build: pip install -r requirements.txt" -ForegroundColor Cyan
        Write-Host "6. Start: python main.py" -ForegroundColor Cyan
        Write-Host "7. Add environment variables" -ForegroundColor Cyan
        Write-Host "8. Deploy!" -ForegroundColor Cyan
        
        Write-Host "`nAfter Render deployment, get your backend URL and continue with frontend..." -ForegroundColor Yellow
        $backendUrl = Read-Host "Paste your backend URL here"
        
        cd aptos-verifier-frontend
        "NEXT_PUBLIC_API_URL=$backendUrl" | Out-File -FilePath ".env.production" -Encoding UTF8
        .\deploy-vercel.ps1
    }
    "3" {
        Write-Host "`nOpening deployment guide..." -ForegroundColor Cyan
        Start-Process "Imageverify\DEPLOY_COMPLETE.md"
    }
    default {
        Write-Host "Invalid choice" -ForegroundColor Red
    }
}

