# Script to check balance and deploy once funded
Write-Host "`n=== Checking Account Balance ===" -ForegroundColor Cyan

$maxAttempts = 12
$attempt = 0

while ($attempt -lt $maxAttempts) {
    $attempt++
    Write-Host "`nAttempt $attempt of $maxAttempts: Checking balance..." -ForegroundColor Yellow
    
    $balanceResult = aptos account balance --profile testnet 2>&1 | ConvertFrom-Json
    
    if ($balanceResult.Result -and $balanceResult.Result.Count -gt 0) {
        $balance = $balanceResult.Result[0].balance
        
        if ($balance -gt 0) {
            Write-Host "`n✅ Account funded! Balance: $balance" -ForegroundColor Green
            Write-Host "`nProceeding with deployment...`n" -ForegroundColor Cyan
            Start-Sleep -Seconds 2
            
            # Run deployment script and automatically skip funding check
            $deployScript = Get-Content "deploy.ps1" -Raw
            # We'll modify the script to skip the funding prompt
            $deployScript = $deployScript -replace 'Read-Host "Press Enter to continue \(or type ''skip'' to skip funding check\)"', '"skip"'
            Invoke-Expression $deployScript
            break
        }
    }
    
    Write-Host "Balance is still 0. Waiting 15 seconds before next check..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
}

if ($attempt -eq $maxAttempts) {
    Write-Host "`n❌ Account still not funded after $maxAttempts attempts." -ForegroundColor Red
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "1. Make sure you clicked the 'Mint' button on the faucet page" -ForegroundColor Cyan
    Write-Host "2. Check if there were any errors on the faucet page" -ForegroundColor Cyan
    Write-Host "3. Try the faucet again if needed" -ForegroundColor Cyan
}

