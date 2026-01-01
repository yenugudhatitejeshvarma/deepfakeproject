"""
Quick test to verify the model loads correctly.
"""
from transformers import AutoImageProcessor, SiglipForImageClassification

print("Testing model loading...")
model_name = "prithivMLmods/deepfake-detector-model-v1"

try:
    print("Loading model...")
    model = SiglipForImageClassification.from_pretrained(model_name)
    processor = AutoImageProcessor.from_pretrained(model_name)
    
    print("[SUCCESS] Model loaded successfully!")
    print(f"Model: {type(model).__name__}")
    print(f"Processor: {type(processor).__name__}")
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    print("\nModel is ready to use!")
    print("To classify an image, run: python run_model.py <image_path>")
    
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")
    raise

