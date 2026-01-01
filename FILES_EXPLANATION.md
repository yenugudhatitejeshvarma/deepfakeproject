# Deepfake Detector Project - Files Explanation

## 📁 Project Structure

### Core Python Files

#### 1. **download_model.py**
**Purpose:** Downloads the deepfake detector model from Hugging Face Hub
- **What it does:**
  - Downloads `prithivMLmods/deepfake-detector-model-v1` from Hugging Face
  - Downloads both the model weights and image processor
  - Caches the model locally for future use
- **When to use:** Run once initially to download the model
- **Output:** Model cached in `~/.cache/huggingface/hub/`
- **Key Functions:**
  - `download_model()` - Main function that downloads and caches the model

#### 2. **run_model.py** ⭐ MAIN SCRIPT
**Purpose:** Runs inference on images to detect deepfakes
- **What it does:**
  - Loads the pre-trained model from cache
  - Processes images (resize, normalize)
  - Runs inference on GPU (if available) or CPU
  - Returns predictions: "real" or "fake" with confidence scores
- **When to use:** Every time you want to classify an image
- **Usage:** `python run_model.py <image_path>`
- **Key Functions:**
  - `load_model()` - Loads model and processor, shows GPU info and cache location
  - `classify_image()` - Processes image and runs inference
  - `main()` - Main entry point
- **Features:**
  - Automatic GPU detection and usage
  - Detailed execution timing
  - Shows model cache location
  - Displays inference statistics

#### 3. **test_model.py**
**Purpose:** Quick verification that the model loads correctly
- **What it does:**
  - Tests model loading
  - Shows model parameters count
  - Verifies model is ready to use
- **When to use:** After downloading to verify installation
- **Output:** Confirmation message with model stats

#### 4. **verify_model.py**
**Purpose:** Comprehensive verification of the model
- **What it does:**
  - Verifies model is real (not dummy)
  - Shows model architecture details
  - Displays weight statistics
  - Confirms model source
- **When to use:** To verify you're using the real trained model

#### 5. **check_gpu.py**
**Purpose:** Check GPU availability
- **What it does:**
  - Checks if CUDA is available
  - Shows GPU device name if available
  - Shows CUDA version
- **When to use:** To check if GPU can be used

### Wrapper Scripts (for easy execution)

#### 6. **run_model.bat**
**Purpose:** Windows batch file to run the model easily
- **What it does:**
  - Activates virtual environment
  - Runs `run_model.py` with arguments
- **Usage:** `run_model.bat 1.png`

#### 7. **run_model.ps1**
**Purpose:** PowerShell script to run the model easily
- **What it does:**
  - Uses venv Python directly
  - Runs `run_model.py` with arguments
- **Usage:** `.\run_model.ps1 1.png`

---

## 📂 Model Storage Location

### Where the Model is Downloaded

The model is **NOT stored in your project directory**. It's cached by Hugging Face transformers library:

**Cache Location:**
```
C:\Users\TWLESH VARMA\.cache\huggingface\hub\models--prithivMLmods--deepfake-detector-model-v1
```

**Cache Structure:**
```
.cache/huggingface/hub/
└── models--prithivMLmods--deepfake-detector-model-v1/
    ├── snapshots/
    │   └── [commit_hash]/
    │       ├── config.json          # Model configuration
    │       ├── model.safetensors     # Model weights (92.8M parameters)
    │       ├── preprocessor_config.json  # Image processor config
    │       └── tokenizer_config.json     # Tokenizer config (if applicable)
    └── refs/
        └── main                      # Points to latest version
```

**Why this location?**
- Standard Hugging Face cache location
- Shared across all projects using the same model
- Automatically managed by transformers library
- Saves disk space (model used by multiple projects)

---

## 🔄 Execution Flow

### How the Model Runs:

1. **Script Execution:**
   ```
   python run_model.py 1.png
   ```

2. **Model Loading (run_model.py):**
   - Checks GPU availability
   - Shows model cache location
   - Loads model from cache (or downloads if not cached)
   - Moves model to GPU (if available) or CPU
   - Loads image processor

3. **Image Processing:**
   - Opens image file
   - Converts to RGB
   - Preprocesses (resize, normalize) using processor
   - Moves to same device as model (GPU/CPU)

4. **Inference:**
   - Runs model forward pass
   - Gets logits (raw predictions)
   - Applies softmax to get probabilities
   - Determines predicted class (real/fake)

5. **Output:**
   - Displays prediction
   - Shows confidence scores
   - Shows execution timing

---

## 📊 Files Used During Execution

### When you run `python run_model.py 1.png`:

1. **run_model.py** - Main script (executed)
2. **transformers library** - Model loading and inference
3. **torch (PyTorch)** - Deep learning framework
4. **PIL (Pillow)** - Image loading and processing
5. **Model files (from cache):**
   - `config.json` - Model configuration
   - `model.safetensors` - Model weights
   - `preprocessor_config.json` - Image processor config
6. **Your image file** - `1.png` (or whatever you specify)

### Dependencies (installed in venv):
- `torch` - PyTorch framework
- `torchvision` - Vision utilities
- `transformers` - Hugging Face transformers
- `pillow` - Image processing
- `huggingface_hub` - Hugging Face Hub API

---

## 🎯 Quick Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `download_model.py` | Download model | Once, initially |
| `run_model.py` | Run inference | Every time |
| `test_model.py` | Test model load | After download |
| `verify_model.py` | Verify real model | To confirm authenticity |
| `check_gpu.py` | Check GPU | To verify GPU setup |
| `run_model.bat` | Easy Windows run | Instead of python command |
| `run_model.ps1` | Easy PowerShell run | Instead of python command |

---

## 💡 Notes

- **GPU Usage:** Model automatically uses GPU if available, falls back to CPU
- **Model Cache:** Model is downloaded once, then cached for future use
- **No Local Model Files:** Model is not in your project directory, it's in Hugging Face cache
- **Virtual Environment:** All scripts should be run with venv activated or use wrapper scripts

