"""
Download the deepfake detector model from Hugging Face.
This model uses SigLIP for image classification to detect deepfakes.
"""
from transformers import AutoImageProcessor, SiglipForImageClassification
import os

def download_model():
    """Download the deepfake detector model from Hugging Face."""
    model_name = "prithivMLmods/deepfake-detector-model-v1"
    
    print(f"Downloading model: {model_name}")
    print("This may take a few minutes depending on your internet connection...")
    print("The model will be cached for future use.\n")
    
    try:
        # Download model and processor
        print("Downloading model weights...")
        model = SiglipForImageClassification.from_pretrained(model_name)
        
        print("Downloading image processor...")
        processor = AutoImageProcessor.from_pretrained(model_name)
        
        print("\n[SUCCESS] Model downloaded successfully!")
        print(f"Model type: {type(model).__name__}")
        print(f"Processor type: {type(processor).__name__}")
        
        # The model is automatically cached by transformers
        # You can find it in: ~/.cache/huggingface/hub/
        print("\nModel is cached and ready to use!")
        print("You can now run the model using run_model.py")
        
        return model, processor
        
    except Exception as e:
        print(f"Error downloading model: {e}")
        print("\nMake sure you have:")
        print("  - Internet connection")
        print("  - transformers library installed: pip install transformers")
        print("  - huggingface_hub installed: pip install huggingface_hub")
        raise

if __name__ == "__main__":
    download_model()

