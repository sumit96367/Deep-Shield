# Script to wait for funds and deploy automatically
Write-Host "`n=== Waiting for Account Funding ===" -ForegroundColor Cyan
Write-Host "This script will check your balance every 15 seconds" -ForegroundColor Yellow
Write-Host "Once funds are detected, deployment will start automatically.`n" -ForegroundColor Green

$maxAttempts = 20
$attempt = 0

while ($attempt -lt $maxAttempts) {
    $attempt++
    Write-Host "Attempt $attempt of $maxAttempts: Checking balance..." -ForegroundColor Yellow
    
    $balanceResult = aptos account balance --profile testnet 2>&1 | ConvertFrom-Json
    
    if ($balanceResult.Result -and $balanceResult.Result.Count -gt 0) {
        $balance = $balanceResult.Result[0].balance
        
        if ($balance -gt 0) {
            Write-Host "`n✅ Account funded! Balance: $balance" -ForegroundColor Green
            Write-Host "`nProceeding with deployment...`n" -ForegroundColor Cyan
            Start-Sleep -Seconds 2
            
            # Run deployment
            & ".\deploy-now.ps1"
            exit 0
        } else {
            Write-Host "Balance is still 0. Waiting 15 seconds..." -ForegroundColor Yellow
            Start-Sleep -Seconds 15
        }
    } else {
        Write-Host "Error checking balance. Retrying in 15 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 15
    }
}

Write-Host "`n❌ Timeout: Account not funded after $($maxAttempts * 15) seconds." -ForegroundColor Red
Write-Host "`nPlease try minting again from the faucet:" -ForegroundColor Yellow
Write-Host "https://faucet.testnet.aptoslabs.com/?address=0x1bfd6b534cc0b44d9c8339286b494a5cfceefb6cec2e0868051644f94cc3517e" -ForegroundColor Cyan

