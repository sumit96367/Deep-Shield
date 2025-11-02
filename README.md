# 🛡️ DeepShield

**AI-Powered Deepfake Detection with Blockchain Verification**

<div align="center">

![DeepShield Logo](aptos-verifier-frontend/public/deepshield-logo.svg)

**Combat misinformation with AI and blockchain technology**

[Features](#key-features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Deployment](#deployment)

</div>

---

## 📋 Overview

DeepShield is a comprehensive platform that detects deepfakes using advanced AI models and permanently records verification results on the Aptos blockchain. This creates an immutable, tamper-proof ledger of authenticity that can be trusted by anyone.

### 🌟 Key Highlights

- 🤖 **AI-Powered Detection**: State-of-the-art ML models for image and audio deepfake detection
- ⛓️ **Blockchain Immutability**: Permanent, verifiable records on Aptos Testnet
- 🔒 **Trust & Transparency**: Public verification of any previously checked file
- 🎨 **Modern UI/UX**: Beautiful, intuitive web interface
- ⚡ **Fast & Efficient**: Real-time processing with instant blockchain confirmation

---

## ✨ Key Features

### AI Detection
- ✅ Image deepfake detection with confidence scoring
- ✅ Audio deepfake detection
- ✅ Multiple AI model support
- ✅ Real-time analysis

### Blockchain Integration
- ✅ Immutable verdict storage on Aptos
- ✅ SHA-256 hash-based verification
- ✅ Public query interface
- ✅ Complete audit trail with timestamps

### User Interface
- ✅ Drag-and-drop file upload
- ✅ Real-time verification feedback
- ✅ Blockchain explorer integration
- ✅ Responsive design

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Aptos CLI (for smart contract deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sumit96367/Deep-Shield.git
   cd DeepShield
   ```

2. **Backend Setup**
   ```bash
   cd Imageverify
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd aptos-verifier-frontend
   npm install
   ```

4. **Run Backend**
   ```bash
   cd Imageverify
   python main.py
   ```

5. **Run Frontend**
   ```bash
   cd aptos-verifier-frontend
   npm run dev
   ```

6. **Access Application**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

---

## 📦 Project Structure

```
DeepShield/
├── Imageverify/              # Backend API
│   ├── sources/              # Move smart contracts
│   ├── main.py              # FastAPI server
│   ├── aptos_service.py    # Blockchain integration
│   ├── ai_detector.py      # Image detection
│   ├── audio_detector.py   # Audio detection
│   └── requirements.txt    # Python dependencies
│
└── aptos-verifier-frontend/  # Frontend
    ├── app/                # Next.js app directory
    ├── public/             # Static assets
    └── package.json       # Node dependencies
```

---

## 🔗 Contract Information

**Network:** Aptos Testnet

**Module Address:** `0x1bfd6b534cc0b44d9c8339286b494a5cfceefb6cec2e0868051644f94cc3517e`

**Module:** `image_verifier`

**Explorer:** [View on Aptos Explorer](https://explorer.aptoslabs.com/account/0x1bfd6b534cc0b44d9c8339286b494a5cfceefb6cec2e0868051644f94cc3517e?network=testnet)

---

## 🛠️ Deployment

### Backend Deployment

Deploy to Railway, Render, or your own server. See `COMPLETE_DEPLOYMENT.md` for detailed instructions.

**Quick Deploy (Railway):**
```bash
cd Imageverify
railway login
railway init
railway up
```

### Frontend Deployment

Deploy to Vercel (recommended for Next.js):

```bash
cd aptos-verifier-frontend
vercel --prod
```

See `COMPLETE_DEPLOYMENT.md` for complete deployment guide.

---

## 📚 Documentation

- [Complete Deployment Guide](COMPLETE_DEPLOYMENT.md)
- [Full Project Documentation](Imageverify/DEPLOY_FULL_PROJECT.md)
- [Project Overview](PROJECT_OVERVIEW.md)
- [Frontend Deployment](aptos-verifier-frontend/DEPLOYMENT.md)

---

## 🎯 Use Cases

- **Journalism**: Verify media authenticity before publication
- **Legal**: Create immutable proof of content verification
- **Social Media**: Combat misinformation and fake content
- **Content Creation**: Prove authenticity of original work
- **Forensics**: Permanent record of digital analysis

---

## 🗺️ Roadmap

### ✅ Completed
- Smart contract deployment
- AI detection models integration
- Full-stack application
- Blockchain transaction recording

### 🚧 In Progress
- Production deployment
- Performance optimization

### 📋 Planned
- Video analysis support
- Mainnet deployment
- Decentralized oracle network
- NFT verification badges
- Multi-chain support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 🙏 Acknowledgments

- Aptos Foundation for blockchain infrastructure
- Hugging Face for AI models
- FastAPI and Next.js communities

---

<div align="center">

**Built with ❤️ for a more trustworthy digital world**

[Website](#) • [Documentation](#) • [Contract](#contract-information)

</div>

