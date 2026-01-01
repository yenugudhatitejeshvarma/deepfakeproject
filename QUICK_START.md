# Quick Start Guide - Check Images for Deepfakes

## ✅ How to Check an Image (Easy Way)

### Method 1: Use PowerShell Script (Recommended)
```powershell
.\run_model.ps1 1.png
```

### Method 2: Use Batch File
```cmd
run_model.bat 1.png
```

### Method 3: Use Python Directly (If you remember the path)
```powershell
.\venv\Scripts\python.exe run_model.py 1.png
```

## ❌ Common Error: "ModuleNotFoundError: No module named 'transformers'"

**Problem:** You're using system Python instead of venv Python.

**Solution:** Always use one of the methods above, or activate venv first:
```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Then run
python run_model.py 1.png
```

## 📊 Understanding Results

When you run the model, you'll see:

```
Predicted: REAL (or FAKE)
Confidence: 50.36%
```

- **REAL** = Authentic image (not a deepfake)
- **FAKE** = Deepfake/manipulated image
- **Confidence** = How sure the model is (higher = more confident)

## 🎯 Example Results from 1.png

```
Predicted: REAL
Confidence: 50.36%

Detailed Probabilities:
  fake : 49.64% [##############----------------]
  real : 50.36% [###############---------------]
```

This means:
- The model thinks it's **REAL** (50.36% confidence)
- But it's a close call (only 0.72% difference)
- The image could be borderline or ambiguous

## 💡 Tips

1. **Always use the wrapper scripts** (`run_model.ps1` or `run_model.bat`) to avoid import errors
2. **Check multiple images** to see different results
3. **Higher confidence** (like 80%+) means the model is more certain
4. **Close probabilities** (like 50/50) mean the image is ambiguous

## 🚀 Quick Commands

```powershell
# Check 1.png
.\run_model.ps1 1.png

# Check any image
.\run_model.ps1 "C:\path\to\your\image.jpg"

# Interactive mode (will ask for image path)
.\run_model.ps1
```

