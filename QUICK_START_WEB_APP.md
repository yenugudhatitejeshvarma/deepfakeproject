# 🚀 Quick Start Guide - Deepfake Detection Web App

## ✅ Everything is Ready!

Your web application is set up and ready to run!

## 📋 Quick Start (3 Steps)

### Step 1: Start Backend (Terminal 1)

**PowerShell:**
```powershell
.\start_backend.ps1
```

**OR Batch File:**
```cmd
start_backend.bat
```

**Wait for:** `Running on http://127.0.0.1:5000`

### Step 2: Start Frontend (Terminal 2)

Open a **NEW terminal** and run:

**PowerShell:**
```powershell
.\start_frontend.ps1
```

**OR Batch File:**
```cmd
start_frontend.bat
```

**Wait for:** `Local: http://localhost:3000/`

### Step 3: Open Browser

Open: **http://localhost:3000**

## 🎯 How to Use

1. **Upload Image** - Click "Select Image" or drag & drop
2. **Analyze** - Click "🔬 Analyze Image"
3. **View Results** - See prediction, confidence, model info, and analysis

## 📊 What You'll See

### Results Display:
- ✅ **Prediction:** REAL or FAKE (large, color-coded)
- ✅ **Confidence:** Percentage with visual bar
- ✅ **Probabilities:** Fake vs Real percentages with bars
- ✅ **Model Info:** Which model, device (GPU/CPU), framework
- ✅ **Analysis:** Timing, image size, timestamp
- ✅ **Interpretation:** Human-readable explanation

## 🔧 Troubleshooting

### Backend Issues:
- **Port 5000 in use?** - Change port in `backend_api.py`
- **Module not found?** - Run: `pip install flask flask-cors`
- **Model not loading?** - Run: `python download_model.py`

### Frontend Issues:
- **Port 3000 in use?** - Change port in `vite.config.ts`
- **Dependencies missing?** - Run: `cd frontend/deepfake && npm install`
- **Connection error?** - Make sure backend is running on port 5000

## 📁 Files Created

### Backend:
- ✅ `backend_api.py` - Flask API server
- ✅ `start_backend.bat` / `start_backend.ps1` - Startup scripts

### Frontend:
- ✅ `frontend/deepfake/src/App.tsx` - Main React component
- ✅ `frontend/deepfake/src/App.css` - Styling
- ✅ `start_frontend.bat` / `start_frontend.ps1` - Startup scripts

### Documentation:
- ✅ `README_WEB_APP.md` - Complete documentation
- ✅ `QUICK_START_WEB_APP.md` - This file

## 🎨 Features

- ✅ Modern, beautiful UI with gradients
- ✅ Drag-and-drop image upload
- ✅ Real-time analysis
- ✅ GPU acceleration (automatic)
- ✅ Detailed results display
- ✅ Model information
- ✅ Performance metrics

## 💡 Tips

1. **Keep both terminals open** - Backend and frontend must run simultaneously
2. **GPU will be used automatically** - No configuration needed
3. **First run is slower** - Model loads on first request
4. **Supported formats** - PNG, JPG, JPEG

## 🎉 You're All Set!

Everything is ready to go. Just start both servers and open your browser!

