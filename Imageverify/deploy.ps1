# DeepShield Deployment Script
# This script deploys the ImageVerifier module to Aptos Testnet

Write-Host "=== DeepShield Deployment Script ===" -ForegroundColor Cyan
Write-Host "Deploying to: Aptos Testnet" -ForegroundColor Yellow
Write-Host ""

# Read the verifier_admin address from Move.toml
$moveTomlPath = "Move.toml"
if (-not (Test-Path $moveTomlPath)) {
    Write-Host "❌ Error: Move.toml not found in current directory" -ForegroundColor Red
    exit 1
}

# Extract address from Move.toml
$moveTomlContent = Get-Content $moveTomlPath -Raw
if ($moveTomlContent -match 'verifier_admin\s*=\s*"([^"]+)"') {
    $VERIFIER_ADMIN_ADDRESS = $matches[1]
    Write-Host "Found verifier_admin address: $VERIFIER_ADMIN_ADDRESS" -ForegroundColor Green
}
else {
    Write-Host "❌ Error: Could not find verifier_admin address in Move.toml" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 1: Compile the contract
Write-Host "Step 1: Compiling Move contract..." -ForegroundColor Yellow
aptos move compile

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Compilation failed. Please fix errors before deploying." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Compilation successful!" -ForegroundColor Green
Write-Host ""

# Step 2: Fund the account (if needed)
Write-Host "Step 2: Fund your Testnet account (if needed)" -ForegroundColor Yellow
Write-Host "Visit: https://faucet.testnet.aptoslabs.com/?address=$VERIFIER_ADMIN_ADDRESS" -ForegroundColor Green
Write-Host "Or use CLI: aptos account fund-with-faucet --account default --amount 100000000" -ForegroundColor Cyan
Write-Host ""
$fundConfirm = Read-Host "Press Enter to continue (or type 'skip' to skip funding check)"

if ($fundConfirm -ne "skip") {
    Write-Host "Checking account balance..." -ForegroundColor Yellow
    $balanceInfo = aptos account balance --profile testnet 2>&1 | ConvertFrom-Json
    if ($balanceInfo.Result -and $balanceInfo.Result.Count -gt 0) {
        $balance = $balanceInfo.Result[0].balance
        Write-Host "Current balance: $balance" -ForegroundColor Cyan
    }
}
else {
    Write-Host "Skipping funding check and proceeding to deployment..." -ForegroundColor Yellow
}

# Step 3: Publish the module
Write-Host ""
Write-Host "Step 3: Publishing module to Testnet..." -ForegroundColor Yellow
aptos move publish `
    --named-addresses verifier_admin=$VERIFIER_ADMIN_ADDRESS `
    --profile testnet `
    --assume-yes `
    --max-gas 50000

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Module published successfully!" -ForegroundColor Green
    Write-Host ""
    
    # Step 4: Initialize the module
    Write-Host "Step 4: Initializing module..." -ForegroundColor Yellow
    aptos move run `
        --function-id "$VERIFIER_ADMIN_ADDRESS::image_verifier::initialize_module" `
        --profile testnet `
        --assume-yes `
        --max-gas 50000
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Module initialized successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "=== Deployment Complete ===" -ForegroundColor Cyan
        Write-Host "Module Address: $VERIFIER_ADMIN_ADDRESS" -ForegroundColor Green
        Write-Host "Module Name: image_verifier" -ForegroundColor Green
        Write-Host "Network: Testnet" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next Steps:" -ForegroundColor Yellow
        Write-Host "1. Update aptos_service.py with MODULE_ADDRESS_STR = `"$VERIFIER_ADMIN_ADDRESS`"" -ForegroundColor Cyan
        Write-Host "2. Update aptos_service.py NODE_URL to Testnet: https://fullnode.testnet.aptoslabs.com/v1" -ForegroundColor Cyan
        Write-Host "3. Ensure your private key in aptos_service.py matches your Testnet account" -ForegroundColor Cyan
        Write-Host "4. Start your Python API server: python main.py" -ForegroundColor Cyan
    }
    else {
        Write-Host ""
        Write-Host "❌ Failed to initialize module" -ForegroundColor Red
        Write-Host "The module was published but not initialized. You can initialize it manually:" -ForegroundColor Yellow
        Write-Host "aptos move run --function-id `"$VERIFIER_ADMIN_ADDRESS::image_verifier::initialize_module`" --profile testnet" -ForegroundColor Cyan
    }
}
else {
    Write-Host ""
    Write-Host "❌ Failed to publish module" -ForegroundColor Red
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "  1. Account has sufficient funds (use faucet if needed)" -ForegroundColor Yellow
    Write-Host "  2. Network connection is stable" -ForegroundColor Yellow
    Write-Host "  3. Move.toml is configured correctly" -ForegroundColor Yellow
    Write-Host "  4. You're using the correct Aptos profile (testnet)" -ForegroundColor Yellow
    exit 1
}



