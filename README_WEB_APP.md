# 🌐 Deepfake Detection Web Application

A full-stack web application for detecting deepfakes in images using AI.

## 🎯 Features

- ✅ **Image Upload Interface** - Easy drag-and-drop or click to upload
- ✅ **Real-time Analysis** - Fast deepfake detection using GPU acceleration
- ✅ **Detailed Results** - Shows:
  - Prediction (Real/Fake)
  - Confidence percentage
  - Fake/Real probabilities
  - Model information
  - Analysis details (timing, image size)
  - Human-readable interpretation

## 🏗️ Architecture

### Backend (Flask API)
- **Location:** `backend_api.py`
- **Port:** 5000
- **Framework:** Flask + Flask-CORS
- **Model:** SiglipForImageClassification from Hugging Face
- **Device:** GPU (CUDA) if available, falls back to CPU

### Frontend (React + TypeScript)
- **Location:** `frontend/deepfake/`
- **Port:** 3000
- **Framework:** React 19 + TypeScript + Vite
- **Styling:** Custom CSS with modern gradient design

## 🚀 Quick Start

### Prerequisites
- Python 3.x with virtual environment
- Node.js and npm installed
- GPU (optional but recommended for faster inference)

### Step 1: Install Frontend Dependencies

```bash
cd frontend/deepfake
npm install
```

### Step 2: Start Backend Server

**Option A: Using PowerShell**
```powershell
.\start_backend.ps1
```

**Option B: Using Batch File**
```cmd
start_backend.bat
```

**Option C: Manual**
```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run backend
python backend_api.py
```

The backend will start on `http://localhost:5000`

### Step 3: Start Frontend Server

**Option A: Using PowerShell**
```powershell
.\start_frontend.ps1
```

**Option B: Using Batch File**
```cmd
start_frontend.bat
```

**Option C: Manual**
```bash
cd frontend/deepfake
npm run dev
```

The frontend will start on `http://localhost:3000`

### Step 4: Use the Application

1. Open your browser and go to `http://localhost:3000`
2. Click "Select Image" or drag and drop an image
3. Click "🔬 Analyze Image"
4. View the results!

## 📡 API Endpoints

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda",
  "cuda_available": true
}
```

### `GET /api/model-info`
Get model information.

**Response:**
```json
{
  "model_name": "prithivMLmods/deepfake-detector-model-v1",
  "model_type": "SiglipForImageClassification",
  "device": "cuda",
  "parameters": 92885762
}
```

### `POST /api/detect`
Analyze an image for deepfakes.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `image` (file)

**Response:**
```json
{
  "success": true,
  "prediction": "REAL",
  "confidence": 85.23,
  "probabilities": {
    "fake": 14.77,
    "real": 85.23
  },
  "model_info": {
    "model_name": "prithivMLmods/deepfake-detector-model-v1",
    "model_type": "SiglipForImageClassification",
    "device": "cuda",
    "framework": "PyTorch"
  },
  "analysis": {
    "image_size": [1920, 1080],
    "inference_time": 45.23,
    "preprocessing_time": 2.15,
    "total_time": 47.38,
    "timestamp": "2025-12-31T14:00:00"
  },
  "interpretation": "The model is highly confident that this image is authentic..."
}
```

## 🎨 UI Features

### Upload Section
- Drag and drop image upload
- Click to browse files
- Image preview before analysis
- Clear button to reset

### Results Display
- **Prediction Card** - Large, color-coded result (Green for Real, Red for Fake)
- **Confidence Bar** - Visual confidence indicator
- **Probability Bars** - Side-by-side fake/real probabilities
- **Interpretation** - Human-readable explanation
- **Model Information** - Which model was used, device, framework
- **Analysis Details** - Timing metrics, image size, timestamp

## 🖥️ System Requirements

### Backend
- Python 3.8+
- 4GB+ RAM
- GPU (recommended) or CPU
- ~3GB disk space (for model cache)

### Frontend
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Node.js 16+ (for development)

## 📁 Project Structure

```
deepfakeproject/
├── backend_api.py              # Flask backend API
├── start_backend.bat           # Windows batch script to start backend
├── start_backend.ps1           # PowerShell script to start backend
├── start_frontend.bat          # Windows batch script to start frontend
├── start_frontend.ps1          # PowerShell script to start frontend
├── frontend/
│   └── deepfake/
│       ├── src/
│       │   ├── App.tsx         # Main React component
│       │   ├── App.css         # Styles
│       │   └── main.tsx        # Entry point
│       ├── package.json        # Dependencies
│       └── vite.config.ts      # Vite configuration
└── venv/                       # Python virtual environment
```

## 🔧 Configuration

### Backend Port
Edit `backend_api.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Frontend Port
Edit `frontend/deepfake/vite.config.ts`:
```typescript
server: {
  port: 3000,
  // ...
}
```

### API URL
Edit `frontend/deepfake/src/App.tsx`:
```typescript
const response = await fetch('http://localhost:5000/api/detect', {
  // ...
})
```

## 🐛 Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check that all dependencies are installed: `pip install flask flask-cors`
- Verify model is downloaded: `python download_model.py`

### Frontend won't start
- Make sure you're in `frontend/deepfake` directory
- Install dependencies: `npm install`
- Check Node.js version: `node --version` (should be 16+)

### Connection Error
- Make sure backend is running on port 5000
- Check if port 5000 is not blocked by firewall
- Verify CORS is enabled in backend

### Model not loading
- Check GPU drivers (if using GPU)
- Verify model cache exists
- Run `python download_model.py` to re-download

## 📊 Performance

### With GPU (RTX 3050)
- Model Loading: ~2-3 seconds (first time)
- Inference: ~40-60ms per image
- Total: ~50-80ms per image

### With CPU
- Model Loading: ~1-2 seconds (first time)
- Inference: ~200-300ms per image
- Total: ~250-350ms per image

## 🔐 Security Notes

- This is a development setup
- For production, add:
  - Authentication
  - Rate limiting
  - File size limits
  - Input validation
  - HTTPS
  - Environment variables for configuration

## 📝 License

This project uses the deepfake detection model from Hugging Face:
- Model: `prithivMLmods/deepfake-detector-model-v1`
- License: Check Hugging Face model card

## 🤝 Contributing

Feel free to improve the UI, add features, or optimize the backend!

## 📧 Support

For issues or questions, check:
1. Model documentation on Hugging Face
2. Flask documentation
3. React documentation

