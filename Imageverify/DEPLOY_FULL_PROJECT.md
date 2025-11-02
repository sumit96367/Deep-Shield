# Full Project Deployment Guide - DeepShield

This guide will help you deploy your entire DeepShield project to Aptos Testnet, including:
- Smart Contract (Move module)
- Python FastAPI Backend
- Next.js Frontend

---

## Prerequisites

- **Python 3.8+** installed
- **Node.js 18+** installed
- **Aptos CLI** installed and configured
- **Git** installed
- An Aptos Testnet account with test coins

---

## Step 1: Deploy Smart Contract to Testnet

### 1.1 Navigate to Imageverify Directory
```powershell
cd Imageverify
```

### 1.2 Verify Move.toml Configuration
Check that `Move.toml` has your account address:
```toml
[addresses]
verifier_admin = "0xYOUR_ACCOUNT_ADDRESS"
```

### 1.3 Run Deployment Script
```powershell
.\deploy.ps1
```

The script will:
1. Read your address from `Move.toml`
2. Compile the Move contract
3. Guide you to fund your account (if needed)
4. Publish the module to Testnet
5. Initialize the module

**Important:** After deployment, save the module address shown at the end!

### 1.4 Manual Deployment (Alternative)
If the script doesn't work, deploy manually:

```powershell
# Compile
aptos move compile

# Publish
aptos move publish `
    --named-addresses verifier_admin=0xYOUR_ACCOUNT_ADDRESS `
    --profile testnet `
    --assume-yes

# Initialize
aptos move run `
    --function-id "0xYOUR_ACCOUNT_ADDRESS::image_verifier::initialize_module" `
    --profile testnet `
    --assume-yes
```

---

## Step 2: Configure Python Backend

### 2.1 Update aptos_service.py
Edit `aptos_service.py` and update these values with your deployed module address:

```python
# Your deployed module address (from Step 1)
MODULE_ADDRESS_STR = "0xYOUR_DEPLOYED_MODULE_ADDRESS" 

# Your Testnet account private key (from .aptos/config.yaml)
ORACLE_PRIVATE_KEY_STR = "ed25519-priv-0xYOUR_PRIVATE_KEY"

# Testnet node URL (already configured)
NODE_URL = "https://fullnode.testnet.aptoslabs.com/v1"
```

### 2.2 Get Your Private Key
If you need your private key:
```powershell
# View your Aptos config
cat $HOME\.aptos\config.yaml
# Or
type $HOME\.aptos\config.yaml
```

Look for the `private_key` under the `testnet` profile.

### 2.3 Install Python Dependencies
```powershell
# Create virtual environment (if not already created)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**Note:** The first time you run the API, it will download AI models (several GB). This may take 10-30 minutes.

### 2.4 Test Backend Configuration
```powershell
python -c "from aptos_service import CLIENT; print('✅ Backend configured correctly!')"
```

If you see errors, verify:
- Module address matches your deployed contract
- Private key matches your Testnet account
- Network URL is correct

---

## Step 3: Start Python Backend Server

### 3.1 Start the Server
```powershell
# Make sure virtual environment is activated
.venv\Scripts\Activate.ps1

# Start the server
python main.py
```

You should see:
```
Loading AI deepfake detection model...
AI Model loaded successfully.
Aptos Service Loaded.
Starting FastAPI server...
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 3.2 Test the API
Open another terminal and test:
```powershell
# Test health endpoint
curl http://127.0.0.1:8000/

# Test with an image (use a real image file)
curl -X POST "http://127.0.0.1:8000/verify" -F "file=@path/to/your/image.jpg"
```

Or visit: http://127.0.0.1:8000/docs for interactive API documentation

---

## Step 4: Deploy Frontend (Optional)

### 4.1 Navigate to Frontend Directory
```powershell
cd ..\aptos-verifier-frontend
```

### 4.2 Install Dependencies
```powershell
npm install
```

### 4.3 Configure API Endpoint
If your frontend needs to connect to the backend, update the API endpoint in your frontend code to point to your backend URL (e.g., `http://127.0.0.1:8000` or your deployed backend URL).

### 4.4 Development Mode
```powershell
npm run dev
```

The frontend will be available at: http://localhost:3000

### 4.5 Production Build
```powershell
# Build for production
npm run build

# Start production server
npm start
```

---

## Step 5: Verify Complete Deployment

### 5.1 Test End-to-End Flow
1. **Upload an image or audio** through your frontend or API
2. **Check the transaction** on Aptos Explorer:
   - Visit: https://explorer.aptoslabs.com/?network=testnet
   - Search for the transaction hash from the API response
3. **Verify the verdict** is recorded on-chain:
   ```powershell
   # Check hash endpoint
   curl http://127.0.0.1:8000/check-hash/YOUR_HASH_HEX
   ```

### 5.2 Verify On-Chain Data
You can also check directly on the blockchain using Aptos CLI:
```powershell
# Call the view function
aptos move view `
    --function-id "0xYOUR_MODULE_ADDRESS::image_verifier::get_verdict" `
    --args hex:YOUR_HASH_HEX `
    --profile testnet
```

---

## Configuration Checklist

Before running the full system, ensure:

- [ ] Smart contract deployed to Testnet
- [ ] Module initialized on-chain
- [ ] `aptos_service.py` has correct MODULE_ADDRESS_STR
- [ ] `aptos_service.py` has correct ORACLE_PRIVATE_KEY_STR
- [ ] `aptos_service.py` NODE_URL points to Testnet
- [ ] Python dependencies installed
- [ ] Backend server starts without errors
- [ ] Frontend configured (if using)
- [ ] API endpoints accessible
- [ ] Test upload works end-to-end

---

## Troubleshooting

### Issue: "Module not found" when calling functions
**Solution:** 
- Verify module address in `aptos_service.py` matches deployed address
- Ensure you're using Testnet (not devnet/mainnet)
- Check module was initialized successfully

### Issue: "Transaction failed" or "Insufficient balance"
**Solution:**
- Fund your account: https://faucet.testnet.aptoslabs.com/
- Check balance: `aptos account list --profile testnet`

### Issue: "Model not found" or slow first startup
**Solution:**
- First run downloads AI models from HuggingFace (this is normal)
- Ensure stable internet connection
- Wait for download to complete (may take 10-30 minutes)

### Issue: Backend won't start
**Solution:**
- Verify virtual environment is activated
- Check all dependencies installed: `pip install -r requirements.txt`
- Verify `aptos_service.py` configuration is correct

---

## Network URLs Reference

- **Devnet:** https://fullnode.devnet.aptoslabs.com/v1 (for early development)
- **Testnet:** https://fullnode.testnet.aptoslabs.com/v1 (current - more stable)
- **Mainnet:** https://fullnode.mainnet.aptoslabs.com/v1 (production)

---

## Next Steps

After successful deployment:
- Monitor your API usage
- Set up logging and monitoring
- Consider production deployment infrastructure
- Add authentication/API keys for security
- Scale the service for higher traffic

---

## Support

For issues:
1. Check this troubleshooting guide
2. Verify all addresses and keys are correct
3. Ensure you're on the correct network (Testnet)
4. Check Aptos Explorer for transaction status

