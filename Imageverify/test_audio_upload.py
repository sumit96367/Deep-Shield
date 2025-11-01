# file: test_audio_upload.py
# Example script to test uploading audio files to the API

import requests
import sys
import os

def upload_audio_file(audio_file_path: str, api_url: str = "http://127.0.0.1:8000/verify"):
    """
    Upload an audio file to the deepfake detection API.
    
    Args:
        audio_file_path: Path to the audio file (e.g., "test.wav", "audio.mp3")
        api_url: The API endpoint URL (default: http://127.0.0.1:8000/verify)
    """
    if not os.path.exists(audio_file_path):
        print(f"Error: File '{audio_file_path}' not found!")
        return
    
    print(f"Uploading audio file: {audio_file_path}")
    print(f"To API: {api_url}")
    
    try:
        # Open the audio file and upload it
        with open(audio_file_path, 'rb') as audio_file:
            files = {'file': (os.path.basename(audio_file_path), audio_file, 'audio/wav')}
            
            # Send POST request
            response = requests.post(api_url, files=files)
        
        # Print the response
        print(f"\n--- Response Status: {response.status_code} ---")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Filename: {result.get('filename')}")
            print(f"Hash: {result.get('image_hash_hex')}")
            print(f"\nAI Verdict:")
            print(f"  Is Deepfake: {result['ai_verdict']['is_deepfake']}")
            print(f"  Confidence: {result['ai_verdict']['confidence']}%")
            print(f"\nBlockchain:")
            print(f"  Transaction Hash: {result['blockchain_result']['transaction_hash']}")
            print(f"  Explorer URL: {result['blockchain_result']['explorer_url']}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to API at {api_url}")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_audio_upload.py <audio_file_path>")
        print("\nExample:")
        print("  python test_audio_upload.py test.wav")
        print("  python test_audio_upload.py audio.mp3")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    upload_audio_file(audio_file)

