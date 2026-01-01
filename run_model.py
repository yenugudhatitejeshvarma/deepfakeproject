"""
Run the deepfake detector model on images.
"""
from transformers import AutoImageProcessor, SiglipForImageClassification
from transformers import file_utils
from PIL import Image
import torch
import sys
import os
import time

# Label mapping
id2label = {
    0: "fake",
    1: "real"
}

def get_model_cache_path():
    """Get the path where the model is cached."""
    cache_dir = file_utils.default_cache_path
    model_cache_path = os.path.join(cache_dir, "models--prithivMLmods--deepfake-detector-model-v1")
    return model_cache_path, cache_dir

def load_model():
    """Load the model and processor."""
    model_name = "prithivMLmods/deepfake-detector-model-v1"
    
    print("="*70)
    print("MODEL LOADING INFORMATION")
    print("="*70)
    
    # Show GPU info
    print("\n[1] GPU/Device Check:")
    print(f"    CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"    GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"    CUDA Version: {torch.version.cuda}")
        device = "cuda"
    else:
        print("    Using CPU (no GPU detected)")
        device = "cpu"
    
    # Show model cache location
    model_cache_path, cache_dir = get_model_cache_path()
    print(f"\n[2] Model Cache Location:")
    print(f"    Cache Directory: {cache_dir}")
    print(f"    Model Path: {model_cache_path}")
    print(f"    Model Exists: {os.path.exists(model_cache_path)}")
    
    # Show model source
    print(f"\n[3] Model Source:")
    print(f"    Repository: {model_name}")
    print(f"    Source: Hugging Face Hub (huggingface.co)")
    
    # Load model
    print(f"\n[4] Loading Model...")
    start_time = time.time()
    model = SiglipForImageClassification.from_pretrained(model_name)
    processor = AutoImageProcessor.from_pretrained(model_name)
    load_time = time.time() - start_time
    
    print(f"    Model loaded in {load_time:.2f} seconds")
    print(f"    Model Type: {type(model).__name__}")
    print(f"    Parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Set model to evaluation mode
    model.eval()
    
    # Move to GPU if available
    print(f"\n[5] Moving Model to Device...")
    start_time = time.time()
    model = model.to(device)
    move_time = time.time() - start_time
    print(f"    Model moved to {device.upper()} in {move_time:.2f} seconds")
    
    print("="*70)
    return model, processor, device

def classify_image(image_path, model, processor, device):
    """Classify an image as real or fake."""
    print("\n" + "="*70)
    print("IMAGE PROCESSING & INFERENCE")
    print("="*70)
    
    # Load and preprocess image
    print(f"\n[1] Loading Image:")
    print(f"    Image Path: {os.path.abspath(image_path)}")
    try:
        start_time = time.time()
        image = Image.open(image_path).convert("RGB")
        load_time = time.time() - start_time
        print(f"    Image Size: {image.size}")
        print(f"    Image Mode: {image.mode}")
        print(f"    Loaded in {load_time:.4f} seconds")
    except Exception as e:
        print(f"    Error loading image: {e}")
        return None
    
    # Process image
    print(f"\n[2] Preprocessing Image:")
    start_time = time.time()
    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    prep_time = time.time() - start_time
    print(f"    Input Shape: {inputs['pixel_values'].shape}")
    print(f"    Input Device: {inputs['pixel_values'].device}")
    print(f"    Preprocessed in {prep_time:.4f} seconds")
    
    # Run inference
    print(f"\n[3] Running Inference on {device.upper()}:")
    start_time = time.time()
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=1).squeeze()
    inference_time = time.time() - start_time
    print(f"    Inference completed in {inference_time:.4f} seconds")
    print(f"    Raw Logits: {logits.cpu().tolist()}")
    
    # Get predictions
    probs_list = probs.cpu().tolist()
    prediction = {
        id2label[i]: round(probs_list[i], 4) for i in range(len(probs_list))
    }
    
    # Get the predicted class
    predicted_class_idx = torch.argmax(probs).item()
    predicted_class = id2label[predicted_class_idx]
    confidence = probs_list[predicted_class_idx]
    
    print(f"\n[4] Results:")
    print(f"    Predicted Class: {predicted_class.upper()}")
    print(f"    Confidence: {confidence:.2%}")
    
    return {
        "predictions": prediction,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "inference_time": inference_time
    }

def main():
    """Main function to run the model."""
    total_start_time = time.time()
    
    # Load model
    model, processor, device = load_model()
    
    # Check if image path is provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Interactive mode
        print("\n" + "="*70)
        print("Deepfake Detector - Interactive Mode")
        print("="*70)
        image_path = input("\nEnter the path to an image file: ").strip().strip('"')
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return
    
    # Classify image
    result = classify_image(image_path, model, processor, device)
    
    if result:
        print("\n" + "="*70)
        print("FINAL RESULTS")
        print("="*70)
        print(f"\nPredicted: {result['predicted_class'].upper()}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Inference Time: {result['inference_time']:.4f} seconds")
        print("\nDetailed Probabilities:")
        for label, prob in result['predictions'].items():
            bar_length = int(prob * 30)
            bar = "#" * bar_length + "-" * (30 - bar_length)
            print(f"  {label:5s}: {prob:.2%} [{bar}]")
    
    total_time = time.time() - total_start_time
    print("\n" + "="*70)
    print(f"Total Execution Time: {total_time:.2f} seconds")
    print("="*70)

if __name__ == "__main__":
    main()

