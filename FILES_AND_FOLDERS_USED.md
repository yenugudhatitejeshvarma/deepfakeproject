# 📁 Files and Folders Used by the Deepfake Detector Project

## 🗂️ Project Directory Structure

```
T:\deepfakeproject\
│
├── 📄 Python Scripts (Core Files)
│   ├── download_model.py          # Downloads model from Hugging Face
│   ├── run_model.py              # ⭐ MAIN: Runs inference on images
│   ├── test_model.py             # Quick model verification
│   ├── verify_model.py           # Detailed model verification
│   └── check_gpu.py              # Check GPU availability
│
├── 🚀 Wrapper Scripts (Easy Execution)
│   ├── run_model.bat             # Windows batch file wrapper
│   └── run_model.ps1             # PowerShell script wrapper
│
├── 📚 Documentation Files
│   ├── FILES_EXPLANATION.md      # Detailed file explanations
│   ├── EXECUTION_SUMMARY.md      # Execution breakdown
│   ├── PROJECT_OVERVIEW.md       # Complete overview
│   ├── HOW_TO_CHECK_IMAGE.md     # How to check images
│   ├── QUICK_START.md            # Quick start guide
│   ├── GPU_SETUP_COMPLETE.md     # GPU setup info
│   └── FILES_AND_FOLDERS_USED.md # This file
│
├── 🖼️ Image Files (Your Test Images)
│   ├── 1.png                     # Test image 1
│   └── 2.png                     # Test image 2
│
├── 🐍 Virtual Environment
│   └── venv/                     # Python virtual environment
│       ├── Scripts/              # Executables (python.exe, pip.exe)
│       ├── Lib/                  # Installed packages
│       │   └── site-packages/    # All Python packages
│       │       ├── torch/        # PyTorch (with CUDA)
│       │       ├── transformers/ # Hugging Face transformers
│       │       ├── PIL/          # Pillow (image processing)
│       │       └── ...           # Other dependencies
│       └── pyvenv.cfg            # Venv configuration
│
└── 📦 Cache (Auto-generated)
    └── __pycache__/              # Python bytecode cache
```

---

## 📍 Files Used During Execution

### When you run: `python run_model.py 1.png`

#### **1. Python Scripts (Executed)**
- ✅ `run_model.py` - Main script that runs everything
- ✅ `transformers` library (from venv) - Model framework
- ✅ `torch` (PyTorch) - Deep learning backend (from venv)
- ✅ `PIL` (Pillow) - Image processing (from venv)

#### **2. Model Files (From Hugging Face Cache)**
**Location:** `C:\Users\TWLESH VARMA\.cache\huggingface\hub\models--prithivMLmods--deepfake-detector-model-v1\`

- ✅ `config.json` - Model architecture configuration
- ✅ `model.safetensors` - Model weights (92.8M parameters)
- ✅ `preprocessor_config.json` - Image processor settings
- ✅ `tokenizer_config.json` - Tokenizer configuration (if applicable)

#### **3. Input Files**
- ✅ `1.png` or `2.png` - Your image files to analyze

#### **4. Virtual Environment Files**
- ✅ `venv/Scripts/python.exe` - Python interpreter
- ✅ `venv/Lib/site-packages/` - All installed packages

---

## 🗂️ Folder Structure Details

### **Project Root (`T:\deepfakeproject\`)**
- Contains all your scripts and test images
- This is where you run commands from

### **Virtual Environment (`venv/`)**
- **Purpose:** Isolated Python environment with all dependencies
- **Size:** ~2-3 GB (includes PyTorch with CUDA)
- **Contents:**
  - `Scripts/` - Executables (python.exe, pip.exe, etc.)
  - `Lib/site-packages/` - All Python packages:
    - `torch/` - PyTorch with CUDA support
    - `transformers/` - Hugging Face transformers
    - `PIL/` - Pillow for image processing
    - `huggingface_hub/` - Hugging Face Hub API
    - And many more dependencies

### **Hugging Face Cache (External)**
**Location:** `C:\Users\TWLESH VARMA\.cache\huggingface\hub\`

- **Purpose:** Stores downloaded models
- **Not in project folder** - This is the standard Hugging Face cache location
- **Size:** ~350-400 MB (for this model)
- **Contents:**
  - Model weights
  - Model configuration
  - Image processor config

### **Python Cache (`__pycache__/`)**
- **Purpose:** Stores compiled Python bytecode
- **Auto-generated:** Created automatically when Python runs
- **Can be deleted:** Will be regenerated as needed

---

## 📊 File Sizes (Approximate)

| Item | Size | Location |
|------|------|----------|
| **Project Scripts** | ~50 KB | `T:\deepfakeproject\` |
| **Virtual Environment** | ~2-3 GB | `T:\deepfakeproject\venv\` |
| **Model Cache** | ~350-400 MB | `C:\Users\...\.cache\huggingface\hub\` |
| **Test Images** | Varies | `T:\deepfakeproject\` |

---

## 🔍 What Gets Created/Used When Running

### **First Time Running:**
1. Model downloaded to Hugging Face cache
2. Model loaded into memory
3. Python cache created (`__pycache__/`)

### **Every Time Running:**
1. Script reads from Hugging Face cache (model already there)
2. Script loads your image file
3. Model processes image
4. Results displayed

### **Files Modified:**
- `__pycache__/` - Updated with compiled Python code
- Hugging Face cache - Model files read (not modified)

---

## 🎯 Key Directories

### **1. Project Directory**
```
T:\deepfakeproject\
```
- Your main working directory
- Contains all scripts and test images
- Where you run commands from

### **2. Virtual Environment**
```
T:\deepfakeproject\venv\
```
- Isolated Python environment
- Contains all dependencies
- Must use `venv\Scripts\python.exe` to run scripts

### **3. Model Cache (External)**
```
C:\Users\TWLESH VARMA\.cache\huggingface\hub\
```
- Hugging Face standard cache location
- Stores downloaded models
- Shared across all projects using same models

---

## 📝 Summary

### **Files You Created/Modified:**
- ✅ All `.py` scripts in project root
- ✅ All `.md` documentation files
- ✅ Wrapper scripts (`.bat`, `.ps1`)
- ✅ Test images (`1.png`, `2.png`)

### **Files Auto-Generated:**
- ✅ `__pycache__/` - Python bytecode cache
- ✅ Model cache in Hugging Face directory

### **Files NOT in Project:**
- ❌ Model files (in Hugging Face cache)
- ❌ Python packages (in venv, but managed)

### **Total Space Used:**
- **Project:** ~50 KB (scripts + docs)
- **Venv:** ~2-3 GB (all dependencies)
- **Model Cache:** ~350-400 MB
- **Total:** ~3-4 GB

---

## 🚀 Quick Reference

**To see all files:**
```powershell
Get-ChildItem -Recurse | Select-Object FullName
```

**To see only Python files:**
```powershell
Get-ChildItem -Recurse -Filter "*.py"
```

**To see image files:**
```powershell
Get-ChildItem -Filter "*.png"
```

**Model cache location:**
```
C:\Users\TWLESH VARMA\.cache\huggingface\hub\models--prithivMLmods--deepfake-detector-model-v1
```

