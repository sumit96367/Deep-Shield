# file: main.py
import uvicorn
import hashlib
import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware # To allow our webpage to talk to it

from ai_detector import detect_deepfake
from audio_detector import detect_audio_deepfake # <-- ADD THIS
from aptos_service import register_verdict_on_chain, get_verdict_from_chain
# --- Import our other Python modules ---
from ai_detector import detect_deepfake       # Our AI Model (Phase 2)
from aptos_service import register_verdict_on_chain # Our Aptos Connector (Step 4)

# --- Create the FastAPI App ---
app = FastAPI(
    title="Deepfake Detection API",
    description="An API to detect deepfakes and log results on the Aptos blockchain."
)

# --- Add CORS Middleware ---
# This is required to allow our (future) HTML webpage to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (unsafe for production, fine for hackathon)
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

@app.get("/")
def read_root():
    """ A simple 'hello' endpoint to check if the server is running. """
    return {
        "message": "Welcome to the Deepfake Verifier API. Use the POST /verify endpoint to upload an image or audio file.",
        "endpoints": {
            "verify": "POST /verify - Upload an image or audio file for deepfake detection",
            "docs": "GET /docs - Interactive API documentation"
        }
    }


@app.post("/verify")
async def verify_image_endpoint(file: UploadFile = File(...)):
    """
    This is the main endpoint for our project.
    It performs the full end-to-end verification process.
    """

    # 1. Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"\n--- New Request: Verifying {file.filename} ---")

    try:
        # 2. Calculate the image's SHA-256 hash
        print("Calculating image hash...")
        sha256_hash = hashlib.sha256()
        with open(temp_file_path, "rb") as f:
            # Read in 4K chunks
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        image_hash_bytes = sha256_hash.digest() # The raw bytes
        image_hash_hex = image_hash_bytes.hex() # The string representation
        print(f"Hash: {image_hash_hex}")

        # 3. Run AI Detection (based on file type)
        print(f"File content type: {file.content_type}")
        
        if file.content_type.startswith("image/"):
            print("Routing to image detector...")
            (is_fake, confidence) = detect_deepfake(temp_file_path)
        
        elif file.content_type.startswith("audio/"):
            print("Routing to audio detector...")
            (is_fake, confidence) = detect_audio_deepfake(temp_file_path)
        
        else:
            # If it's not an image or audio, reject it.
            print(f"Unsupported file type: {file.content_type}")
            raise HTTPException(
                status_code=415, # 415 Unsupported Media Type
                detail=f"Unsupported file type: {file.content_type}. Only images and audio are allowed."
            )
        
        print(f"AI Verdict: is_fake={is_fake}, confidence={confidence}%")
        
        # 4. Submit to Aptos Blockchain (from aptos_service.py)
        print("Submitting verdict to Aptos blockchain...")
        tx_hash = await register_verdict_on_chain(
            image_hash=image_hash_bytes,
            is_fake=is_fake,
            confidence=confidence
        )
        print(f"Blockchain TX Hash: {tx_hash}")

        # 5. Return the full result to the user
        return {
            "filename": file.filename,
            "image_hash_hex": image_hash_hex,
            "ai_verdict": {
                "is_deepfake": is_fake,
                "confidence": confidence
            },
            "blockchain_result": {
                "transaction_hash": tx_hash,
                "explorer_url": f"https://explorer.aptoslabs.com/txn/{tx_hash}?network=devnet"
            }
        }

    except Exception as e:
        # If anything fails (e.g., blockchain transaction)
        print(f"An error occurred during verification: {e}")
        return {"error": str(e)}

    finally:
        # 6. Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/check-hash/{hash_hex}")
async def check_hash_endpoint(hash_hex: str):
    """
    Checks the on-chain ledger for a pre-existing verdict.
    """
    try:
        # Call our new service function
        result = await get_verdict_from_chain(hash_hex)
        
        if not result["found"]:
            raise HTTPException(
                status_code=404, # 404 Not Found
                detail="This hash has not been verified yet. No verdict was found on the blockchain."
            )
        
        # Return the data
        return result

    except Exception as e:
        print(f"Error in /check-hash: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while checking the blockchain."
        )

# --- This block lets us run the server directly ---
if __name__ == "__main__":
    print("Starting FastAPI server...")
    # Make sure your `aptos_service.py` is configured before running this!
    uvicorn.run(app, host="127.0.0.1", port=8000)