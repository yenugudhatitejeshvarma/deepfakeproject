"""
Flask Backend API for Deepfake Detection
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
import torch
import io
import os
import time
from datetime import datetime
from grad_cam_utils import generate_gradcam_visualization

app = Flask(__name__)
# Enable CORS for frontend and browser extensions
# In production, restrict origins for security. For development, allow all.
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',') if os.environ.get('ALLOWED_ORIGINS') else '*'
CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,  # Allow configured origins (default: all for browser extensions)
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Global model variables
model = None
processor = None
device = None

# Label mapping
id2label = {
    0: "fake",
    1: "real"
}

def load_model():
    """Load the deepfake detection model."""
    global model, processor, device
    
    if model is not None and processor is not None:
        print(f"[INFO] Model already loaded on {device}")
        return model, processor, device
    
    print("\n" + "="*70)
    print("LOADING DEEPFAKE DETECTION MODEL")
    print("="*70)
    
    model_name = "prithivMLmods/deepfake-detector-model-v1"
    
    # Show device info
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n[1] Device Check:")
    print(f"    CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"    GPU: {torch.cuda.get_device_name(0)}")
        print(f"    CUDA Version: {torch.version.cuda}")
    else:
        print("    Using CPU")
    print(f"    Selected Device: {device.upper()}")
    
    # Load model
    print(f"\n[2] Loading Model from Hugging Face...")
    print(f"    Model: {model_name}")
    print("    This may take 10-30 seconds...")
    start_time = time.time()
    
    try:
        model = SiglipForImageClassification.from_pretrained(model_name)
        processor = AutoImageProcessor.from_pretrained(model_name)
        load_time = time.time() - start_time
        print(f"    ✓ Model loaded in {load_time:.2f} seconds")
        print(f"    Model Type: {type(model).__name__}")
        print(f"    Parameters: {sum(p.numel() for p in model.parameters()):,}")
    except Exception as e:
        print(f"    ✗ ERROR loading model: {e}")
        raise
    
    # Set to evaluation mode
    print(f"\n[3] Setting Model to Evaluation Mode...")
    model.eval()
    print("    ✓ Model set to evaluation mode")
    
    # Move to GPU if available
    print(f"\n[4] Moving Model to {device.upper()}...")
    start_time = time.time()
    model = model.to(device)
    move_time = time.time() - start_time
    print(f"    ✓ Model moved to {device.upper()} in {move_time:.2f} seconds")
    
    print("\n" + "="*70)
    print("MODEL LOADED SUCCESSFULLY!")
    print("="*70 + "\n")
    
    return model, processor, device

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - API information."""
    return jsonify({
        "message": "Deepfake Detection API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "model_info": "/api/model-info",
            "detect": "/api/detect (POST)"
        },
        "status": "running"
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "device": device,
        "cuda_available": torch.cuda.is_available()
    })

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information."""
    model_name = "prithivMLmods/deepfake-detector-model-v1"
    return jsonify({
        "model_name": model_name,
        "model_type": "SiglipForImageClassification",
        "model_source": "Hugging Face Hub",
        "repository": model_name,
        "device": device,
        "cuda_available": torch.cuda.is_available(),
        "parameters": sum(p.numel() for p in model.parameters()) if model else 0,
        "labels": ["fake", "real"]
    })

@app.route('/api/detect', methods=['POST', 'OPTIONS'])
def detect_deepfake():
    """Detect deepfake in uploaded image."""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    print("\n" + "="*70)
    print("NEW PREDICTION REQUEST RECEIVED")
    print("="*70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Ensure model is loaded
        if model is None or processor is None:
            print("\n[WARNING] Model not loaded! Loading now...")
            load_model()
        else:
            print(f"\n[INFO] Model Status: ✓ Loaded and Ready")
            print(f"[INFO] Model Device: {device.upper()}")
            print(f"[INFO] Model Type: {type(model).__name__}")
        
        # Check if image file is in request
        if 'image' not in request.files:
            print("[ERROR] No image file in request")
            return jsonify({"success": False, "error": "No image file provided"}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            print("[ERROR] Empty filename")
            return jsonify({"success": False, "error": "No image file selected"}), 400
        
        print(f"[INFO] Processing image: {file.filename}")
        
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        print(f"[INFO] Image loaded: {image.size[0]}x{image.size[1]} pixels")
        
        # Record timings
        start_time = time.time()
        
        # Preprocess image
        print("\n[STEP 1] Preprocessing image...")
        prep_start = time.time()
        inputs = processor(images=image, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        prep_time = time.time() - prep_start
        print(f"        ✓ Preprocessed in {prep_time*1000:.2f}ms")
        print(f"        Input shape: {inputs['pixel_values'].shape}")
        print(f"        Input device: {inputs['pixel_values'].device}")
        
        # Run inference
        print(f"\n[STEP 2] Running model inference on {device.upper()}...")
        infer_start = time.time()
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=1).squeeze()
        infer_time = time.time() - infer_start
        print(f"        ✓ Inference completed in {infer_time*1000:.2f}ms")
        
        # Get probabilities
        probs_list = probs.cpu().tolist()
        fake_prob = probs_list[0]
        real_prob = probs_list[1]
        
        # Determine prediction
        predicted_class = "fake" if fake_prob > real_prob else "real"
        confidence = max(fake_prob, real_prob)
        
        total_time = time.time() - start_time
        
        print("\n[STEP 3] Results:")
        print(f"        Raw Logits: {logits.cpu().tolist()}")
        print(f"        Fake Probability: {fake_prob*100:.2f}%")
        print(f"        Real Probability: {real_prob*100:.2f}%")
        print(f"        Predicted: {predicted_class.upper()}")
        print(f"        Confidence: {confidence*100:.2f}%")
        print(f"        Total Time: {total_time*1000:.2f}ms")
        
        # Generate Grad-CAM visualization (only for fake predictions or if requested)
        print("\n[STEP 4] Generating forensic Grad-CAM heatmap visualization...")
        viz_start = time.time()
        try:
            # For fake predictions, show what regions are suspicious
            # For real predictions, we can still show attention but it's less critical
            target_class_idx = 0 if predicted_class == "fake" else 1
            is_fake = (predicted_class == "fake")
            original_base64, heatmap_overlay_base64 = generate_gradcam_visualization(
                model, processor, device, image, target_class=target_class_idx, is_fake=is_fake
            )
            viz_time = time.time() - viz_start
            print(f"        ✓ Forensic heatmap generated in {viz_time*1000:.2f}ms")
            if is_fake:
                print(f"        Heatmap uses RED and YELLOW patches for detected fake regions")
            else:
                print(f"        Heatmap uses GREEN only for authentic regions")
            visualization_available = True
        except Exception as e:
            print(f"        ⚠ Heatmap generation failed: {e}")
            import traceback
            traceback.print_exc()
            print("        Continuing without visualization...")
            original_base64 = None
            heatmap_overlay_base64 = None
            visualization_available = False
            viz_time = 0
        
        # Prepare response
        result = {
            "success": True,
            "prediction": predicted_class.upper(),
            "confidence": round(confidence * 100, 2),
            "probabilities": {
                "fake": round(fake_prob * 100, 2),
                "real": round(real_prob * 100, 2)
            },
            "model_info": {
                "model_name": "prithivMLmods/deepfake-detector-model-v1",
                "model_type": "SiglipForImageClassification",
                "device": device,
                "framework": "PyTorch"
            },
            "analysis": {
                "image_size": image.size,
                "inference_time": round(infer_time * 1000, 2),  # ms
                "preprocessing_time": round(prep_time * 1000, 2),  # ms
                "total_time": round(total_time * 1000, 2),  # ms
                "timestamp": datetime.now().isoformat()
            },
            "interpretation": get_interpretation(predicted_class, confidence)
        }
        
        # Add visualization if available
        if visualization_available:
            result["visualization"] = {
                "available": True,
                "original_image": f"data:image/png;base64,{original_base64}",
                "heatmap_overlay": f"data:image/png;base64,{heatmap_overlay_base64}",
                "visualization_time": round(viz_time * 1000, 2)  # ms
            }
        else:
            result["visualization"] = {
                "available": False,
                "message": "Heatmap visualization not available"
            }
        
        print("\n" + "="*70)
        print(f"✓ PREDICTION COMPLETE: {predicted_class.upper()} ({confidence*100:.2f}% confidence)")
        print("="*70 + "\n")
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("\n" + "="*70)
        print("❌ ERROR PROCESSING IMAGE")
        print("="*70)
        print(f"Error: {str(e)}")
        print("\nFull traceback:")
        print(error_trace)
        print("="*70 + "\n")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def get_interpretation(prediction, confidence):
    """Get human-readable interpretation of the result."""
    if confidence >= 0.8:
        certainty = "highly confident"
    elif confidence >= 0.6:
        certainty = "moderately confident"
    else:
        certainty = "uncertain"
    
    if prediction.lower() == "real":
        return f"The model is {certainty} that this image is authentic and not a deepfake."
    else:
        return f"The model is {certainty} that this image contains deepfake/manipulated content."

if __name__ == '__main__':
    import os
    import sys
    import warnings
    
    # Suppress Flask development server warning
    warnings.filterwarnings('ignore', category=UserWarning)
    
    # Suppress werkzeug logging
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Filter stderr to remove development server warning
    original_stderr = sys.stderr
    
    class FilteredStderr:
        def __init__(self, original):
            self.original = original
        def write(self, message):
            msg_lower = message.lower()
            if 'development server' not in msg_lower and 'wsgi' not in msg_lower and 'production deployment' not in msg_lower:
                self.original.write(message)
        def flush(self):
            self.original.flush()
        def __getattr__(self, name):
            return getattr(self.original, name)
    
    sys.stderr = FilteredStderr(original_stderr)
    
    print("\n" + "="*70)
    print("STARTING DEEPFAKE DETECTION API SERVER")
    print("="*70)
    
    # Load model BEFORE starting server
    print("\nLoading model now...")
    try:
        load_model()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: Failed to load model!")
        print(f"Error: {e}")
        print("\nPlease check:")
        print("  1. Model is downloaded: python download_model.py")
        print("  2. Internet connection is available")
        print("  3. Transformers library is installed")
        sys.exit(1)
    
    # Verify model is loaded
    if model is None or processor is None:
        print("\n❌ ERROR: Model failed to load!")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("SERVER INFORMATION")
    print("="*70)
    print(f"Model Status: ✓ Loaded")
    print(f"Device: {device.upper()}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    print(f"Model Type: {type(model).__name__}")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
    print("="*70)
    print("\nStarting Flask server...")
    print("Server URL: http://localhost:5000")
    print("\nAPI Endpoints:")
    print("  - GET  /              - API information")
    print("  - GET  /api/health    - Health check")
    print("  - GET  /api/model-info - Model information")
    print("  - POST /api/detect    - Analyze image for deepfakes")
    print("\n" + "="*70)
    print("Server is ready! Waiting for requests...")
    print("="*70 + "\n")
    
    try:
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
    finally:
        sys.stderr = original_stderr

