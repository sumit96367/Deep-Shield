# file: ai_detector.py
from transformers import pipeline
from PIL import Image
from typing import Tuple
import os

# This line initializes the AI pipeline.
# It will automatically download the model on the first run.
print("Loading AI deepfake detection model...")
# We are using a specific, pre-trained image classification model
model_pipeline = pipeline(
    "image-classification", 
    model="dima806/deepfake_vs_real_image_detection"
)
print("AI Model loaded successfully.")

def detect_deepfake(image_path: str) -> Tuple[bool, int]:
    """
    Analyzes a given image file and returns a deepfake verdict.

    Args:
        image_path (str): The file path to the image.

    Returns:
        A tuple (is_fake, confidence_percent):
        - is_fake (bool): True if the image is a deepfake, False otherwise.
        - confidence_percent (int): The model's confidence (0-100).
    """
    try:
        # Open the image using PIL (Python Imaging Library)
        img = Image.open(image_path)

        # Run the AI model on the image
        results = model_pipeline(img)

        # The model's output looks like:
        # [{'label': 'real', 'score': 0.99}, {'label': 'fake', 'score': 0.01}]
        # We need to find the label with the highest score.
        best_result = sorted(results, key=lambda x: x['score'], reverse=True)[0]

        label = best_result['label']
        confidence = best_result['score']

        # Convert confidence (0.0 to 1.0) to a percentage (0 to 100)
        confidence_percent = int(confidence * 100)

        if label.lower() == 'fake':
            # It's a fake!
            return (True, confidence_percent)
        else:
            # It's real!
            return (False, confidence_percent)

    except Exception as e:
        print(f"Error during AI detection: {e}")
        # In case of an error, we'll default to a safe verdict
        return (False, 0)

# --- This block lets us test the file directly ---
if __name__ == "__main__":
    print("\n--- Running AI Detector Self-Test ---")

    # Create a dummy image file for testing
    test_image_name = "test_image.jpg"
    try:
        Image.new('RGB', (100, 100), color = 'blue').save(test_image_name)
        print(f"Created a dummy file: '{test_image_name}'")

        # Run detection on our dummy file
        (is_fake, confidence) = detect_deepfake(test_image_name)

        print("\n--- Test Result ---")
        print(f"File: {test_image_name}")
        print(f"Verdict: Is Fake? -> {is_fake}")
        print(f"Confidence: {confidence}%")

        # Clean up the dummy file
        os.remove(test_image_name)

    except Exception as e:
        print(f"Could not create or test image: {e}")
        print("Please ensure you have 'Pillow' installed: pip install Pillow")