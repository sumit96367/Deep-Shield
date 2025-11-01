# Deployment Guide: Deepfake Detection API

This guide will walk you through deploying the Deepfake Detection project, which includes:
- FastAPI backend server for AI-powered deepfake detection
- Aptos smart contract for on-chain verification storage
- Support for both image and audio deepfake detection

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Install Dependencies](#step-1-install-dependencies)
3. [Step 2: Configure Aptos Blockchain](#step-2-configure-aptos-blockchain)
4. [Step 3: Deploy Smart Contract](#step-3-deploy-smart-contract)
5. [Step 4: Configure Python API](#step-4-configure-python-api)
6. [Step 5: Start the API Server](#step-5-start-the-api-server)
7. [Step 6: Test the Deployment](#step-6-test-the-deployment)
8. [Step 7: Production Deployment (Optional)](#step-7-production-deployment-optional)

---

## Prerequisites

Before starting, ensure you have:
- **Python 3.8+** installed
- **Aptos CLI** installed ([Install Guide](https://aptos.dev/tools/aptos-cli/))
- **Git** installed
- An Aptos account with test coins (for Devnet) or real APT (for Mainnet)
- **Internet connection** (for downloading AI models from HuggingFace)

---

## Step 1: Install Dependencies

### 1.1 Create Virtual Environment
```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# Or on Windows CMD
.venv\Scripts\activate.bat
```

### 1.2 Install Python Packages
```powershell
pip install -r requirements.txt
```

**Note:** This will install:
- FastAPI and Uvicorn (web server)
- Transformers and PyTorch (AI models)
- Aptos SDK (blockchain integration)
- Other dependencies

The first time you run the API, it will download AI models from HuggingFace (this may take several minutes).

---

## Step 2: Configure Aptos Blockchain

### 2.1 Set Up Aptos Account

If you don't have an Aptos account yet:

```powershell
# For Devnet (recommended for testing)
aptos init --network devnet

# For Mainnet (production)
aptos init --network mainnet
```

### 2.2 Fund Your Account (Devnet Only)

For Devnet testing, get free test coins:
```powershell
# Visit https://faucet.devnet.aptoslabs.com/ and enter your account address
# Or use CLI:
aptos account fund-with-faucet --account default --amount 100000000
```

### 2.3 Update Config File

Edit `.aptos/config.yaml` to ensure your profile has:
- `rest_url` configured (should end with `/v1`)
- Correct `private_key`, `public_key`, and `account`

**Example:**
```yaml
profiles:
  devnet:
    network: Devnet
    private_key: ed25519-priv-0x...
    public_key: ed25519-pub-0x...
    account: 0x...
    rest_url: "https://fullnode.devnet.aptoslabs.com/v1"
```

---

## Step 3: Deploy Smart Contract

### 3.1 Update Move.toml

Ensure `Move.toml` has the correct address:
```toml
[addresses]
verifier_admin = "0xYOUR_ACCOUNT_ADDRESS"
```

### 3.2 Compile the Contract

```powershell
aptos move compile
```

### 3.3 Publish the Contract

**For Devnet:**
```powershell
aptos move publish --named-addresses verifier_admin=0xYOUR_ACCOUNT_ADDRESS --profile devnet
```

**For Mainnet:**
```powershell
aptos move publish --named-addresses verifier_admin=0xYOUR_ACCOUNT_ADDRESS --profile mainnet
```

**Note:** Save the transaction hash - you'll need the module address!

### 3.4 Get Your Module Address

After publishing, get your module address:
```powershell
aptos account list --profile devnet
```

The module address will be your account address (the one you used for `verifier_admin`).

### 3.5 Initialize the Module

Initialize the smart contract (one-time setup):
```powershell
# For Devnet
aptos move run --function-id "0xYOUR_MODULE_ADDRESS::image_verifier::initialize_module" --profile devnet

# For Mainnet (if using mainnet profile)
aptos move run --function-id "mainnet::image_verifier::initialize_module" --profile mainnet
```

**Note:** If you get a gas error, try:
```powershell
aptos move run --function-id "0xYOUR_MODULE_ADDRESS::image_verifier::initialize_module" --profile devnet --max-gas 10000
```

---

## Step 4: Configure Python API

### 4.1 Update `aptos_service.py`

Edit `aptos_service.py` and update these values:

```python
# Your module publisher address (from Step 3.4)
MODULE_ADDRESS_STR = "0xYOUR_MODULE_ADDRESS" 

# Your account private key (from .aptos/config.yaml)
ORACLE_PRIVATE_KEY_STR = "ed25519-priv-0xYOUR_PRIVATE_KEY"

# Choose your network
NODE_URL = "https://fullnode.devnet.aptoslabs.com/v1"  # Devnet
# OR
# NODE_URL = "https://fullnode.mainnet.aptoslabs.com/v1"  # Mainnet
```

### 4.2 Verify Configuration

Test that the Aptos service loads correctly:
```powershell
python -c "from aptos_service import CLIENT; print('Aptos service configured correctly!')"
```

If you see an error, check:
- Module address is correct (matches your account)
- Private key is correct (matches your `.aptos/config.yaml`)
- Network URL matches your deployment network

---

## Step 5: Start the API Server

### 5.1 Start the Server

```powershell
python main.py
```

You should see output like:
```
Loading AI deepfake detection model...
AI Model loaded successfully.
Aptos Service Loaded.
Starting FastAPI server...
```

**Important:** The first time you run this, it will download AI models (several GB). This may take 10-30 minutes depending on your internet speed.

### 5.2 Server Endpoints

Once running, your server will be available at:
- **API Base:** `http://127.0.0.1:8000`
- **Interactive Docs:** `http://127.0.0.1:8000/docs`
- **Health Check:** `http://127.0.0.1:8000/`

### 5.3 Run in Background (Optional)

For production, you may want to run it as a service or use a process manager like `supervisor` or `systemd`.

---

## Step 6: Test the Deployment

### 6.1 Test with Python Script

```powershell
# Test image upload
python test_audio_upload.py test_image.jpg

# Test audio upload (if you have a .wav file)
python test_audio_upload.py test_audio.wav
```

### 6.2 Test via cURL

**Upload an image:**
```powershell
curl -X POST "http://127.0.0.1:8000/verify" -F "file=@test_image.jpg"
```

**Check a hash:**
```powershell
curl "http://127.0.0.1:8000/check-hash/YOUR_HASH_HEX"
```

### 6.3 Test via Browser

1. Visit `http://127.0.0.1:8000/docs`
2. Click on `/verify` endpoint
3. Click "Try it out"
4. Upload a test file
5. Click "Execute"

### 6.4 Verify Blockchain Transaction

After uploading a file, you'll receive a transaction hash. Check it on:
- **Devnet:** https://explorer.aptoslabs.com/txn/{tx_hash}?network=devnet
- **Mainnet:** https://explorer.aptoslabs.com/txn/{tx_hash}?network=mainnet

---

## Step 7: Production Deployment (Optional)

### 7.1 Environment Variables

For production, use environment variables instead of hardcoded values:

Create `.env` file:
```env
APTOS_MODULE_ADDRESS=0xYOUR_ADDRESS
APTOS_PRIVATE_KEY=ed25519-priv-0x...
APTOS_NODE_URL=https://fullnode.mainnet.aptoslabs.com/v1
```

Then update `aptos_service.py` to read from environment:
```python
import os
from dotenv import load_dotenv

load_dotenv()

MODULE_ADDRESS_STR = os.getenv("APTOS_MODULE_ADDRESS")
ORACLE_PRIVATE_KEY_STR = os.getenv("APTOS_PRIVATE_KEY")
NODE_URL = os.getenv("APTOS_NODE_URL")
```

### 7.2 Update CORS Settings

For production, restrict CORS origins:
```python
# In main.py, update CORS middleware:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### 7.3 Use Production Server

For production, use a production ASGI server:
```powershell
# Install gunicorn with uvicorn workers
pip install gunicorn

# Run with multiple workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 7.4 Set Up Reverse Proxy (Nginx/Apache)

Configure Nginx or Apache to:
- Handle HTTPS/SSL
- Route requests to your FastAPI server
- Serve static files if needed

### 7.5 Deploy to Cloud Platforms

**Heroku:**
```powershell
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

**AWS/DigitalOcean:**
- Use Docker containerization
- Deploy to EC2/Droplet
- Set up load balancer if needed

---

## Troubleshooting

### Issue: "No rest url given"
**Solution:** Ensure `.aptos/config.yaml` has `rest_url` ending with `/v1`

### Issue: "Model not found" or "401 Unauthorized"
**Solution:** 
- Check internet connection
- For private models, authenticate: `huggingface-cli login`
- Audio model loads lazily - this is normal

### Issue: "Transaction failed"
**Solution:**
- Check account has sufficient balance
- Verify module address is correct
- Ensure module was initialized

### Issue: "Module not found" when calling functions
**Solution:**
- Verify module was published successfully
- Check module address matches in `aptos_service.py`
- Ensure you're using the correct network (devnet vs mainnet)

---

## Summary Checklist

- [ ] Python dependencies installed
- [ ] Aptos CLI installed and configured
- [ ] Aptos account created and funded (for devnet)
- [ ] Smart contract compiled
- [ ] Smart contract published to blockchain
- [ ] Module initialized on-chain
- [ ] `aptos_service.py` configured with correct addresses/keys
- [ ] API server starts without errors
- [ ] Test upload works
- [ ] Blockchain transactions succeed
- [ ] Hash lookup works

---

## Next Steps

After deployment, you can:
- Build a frontend web interface
- Add authentication/API keys
- Set up monitoring and logging
- Scale the service for higher traffic
- Deploy to production infrastructure

---

## Support

For issues:
1. Check the troubleshooting section
2. Review Aptos documentation: https://aptos.dev
3. Check FastAPI documentation: https://fastapi.tiangolo.com
4. Review logs in terminal output

