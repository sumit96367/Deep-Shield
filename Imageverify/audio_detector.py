# file: audio_detector.py
from transformers import pipeline
import os
import soundfile
import librosa

# Lazy loading: Model will be loaded on first use
audio_pipeline = None

def _load_audio_model():
    """Load the audio detection model lazily."""
    global audio_pipeline
    if audio_pipeline is not None:
        return audio_pipeline
    
    print("Loading AI audio deepfake model... (This may take a moment)")
    # Try alternative models if the primary one fails
    # Note: These models need to be publicly available on HuggingFace
    model_options = [
        "wis-ai/bravov1-synthetic-speech-detector",  # Alternative mentioned in comments
    ]
    
    for model_name in model_options:
        try:
            audio_pipeline = pipeline(
                "audio-classification",
                model=model_name
            )
            print(f"AI Audio Model loaded successfully: {model_name}")
            return audio_pipeline
        except Exception as e:
            print(f"Failed to load model {model_name}: {e}")
            if model_name == model_options[-1]:
                # Last model failed, raise the error with helpful message
                raise Exception(
                    f"Could not load audio detection model '{model_name}'. "
                    "The model may be private, unavailable, or require authentication. "
                    "Please check:\n"
                    "1. The model exists and is public on HuggingFace\n"
                    "2. You have internet connection\n"
                    "3. If using a private model, authenticate with: huggingface-cli login"
                )
    return audio_pipeline

def detect_audio_deepfake(file_path: str) -> (bool, int):
    """
    Analyzes an audio file and returns a verdict on whether it's synthetic.

    Returns:
        A tuple (is_fake, confidence_percent):
    """
    try:
        # Load the model lazily if not already loaded
        pipeline = _load_audio_model()
        
        # Load the audio file.
        # We must resample it to 16000 Hz, as required by this model.
        speech, sample_rate = librosa.load(file_path, sr=16000)
        
        # We need to save it as a dictionary for the pipeline
        audio_input = {"raw": speech, "sampling_rate": 16000}

        # Run the AI model
        results = pipeline(audio_input)
        
        # The output looks like:
        # [{'label': 'bonafide', 'score': 0.99}, {'label': 'spoof', 'score': 0.01}]
        
        best_result = sorted(results, key=lambda x: x['score'], reverse=True)[0]
        
        label = best_result['label']
        confidence = best_result['score']
        
        confidence_percent = int(confidence * 100)
        
        # This model uses 'spoof' (fake) and 'bonafide' (real)
        if label.lower() == 'spoof':
            return (True, confidence_percent)
        else:
            # The other label is 'bonafide'
            return (False, confidence_percent)

    except Exception as e:
        print(f"Error during Audio AI detection: {e}")
        return (False, 0)

# --- Test this file directly ---
if __name__ == "__main__":
    print("\n--- Running Audio Detector Self-Test ---")
    print("NOTE: This test requires a valid .wav file to work.")
    print("Please download a test .wav file and change 'your_test_file.wav' below.")
    
    test_file = "your_test_file.wav" # <-- PUT A REAL .WAV FILE HERE
    
    if os.path.exists(test_file):
        (is_fake, confidence) = detect_audio_deepfake(test_file)
        print("\n--- Test Result ---")
        print(f"File: {test_file}")
        print(f"Verdict: Is Fake? -> {is_fake}")
        print(f"Confidence: {confidence}%")
    else:
        print(f"Test file not found: {test_file}. Skipping self-test.")