# 🚀 How to Run the Deepfake Detection Web App

## ⚠️ IMPORTANT: You MUST Start Backend First!

The backend must be running before you use the frontend.

## 🎯 Quick Start (Easiest Way)

### Option 1: Start Everything at Once (Recommended)

**PowerShell:**
```powershell
.\START_ALL.ps1
```

**OR Batch File:**
```cmd
START_ALL.bat
```

This will open two separate windows:
- One for Backend (port 5000)
- One for Frontend (port 3000)

### Option 2: Start Manually (Step by Step)

#### Step 1: Start Backend (Terminal 1)

**PowerShell:**
```powershell
.\start_backend.ps1
```

**OR Batch File:**
```cmd
start_backend.bat
```

**OR Manual:**
```powershell
.\venv\Scripts\python.exe backend_api.py
```

**Wait for this message:**
```
============================================================
Starting Deepfake Detection API...
============================================================
Model device: cuda
CUDA available: True
Model loaded: True
============================================================
Server starting on http://localhost:5000
 * Running on http://0.0.0.0:5000
```

#### Step 2: Start Frontend (Terminal 2)

Open a **NEW terminal window** and run:

**PowerShell:**
```powershell
.\start_frontend.ps1
```

**OR Batch File:**
```cmd
start_frontend.bat
```

**OR Manual:**
```powershell
cd frontend\deepfake
npm run dev
```

**Wait for this message:**
```
  VITE v7.2.4  ready in XXX ms

  ➜  Local:   http://localhost:3000/
```

#### Step 3: Open Browser

Go to: **http://localhost:3000**

## ✅ Verify Backend is Running

Before using the frontend, test if backend is working:

```powershell
python test_backend.py
```

This will test all API endpoints.

## 🐛 Troubleshooting

### Error: "Failed to connect to server"

**Problem:** Backend is not running

**Solution:**
1. Check if backend is running on port 5000
2. Open a new terminal and run: `.\start_backend.ps1`
3. Wait for "Running on http://0.0.0.0:5000"
4. Then try the frontend again

### Error: "Port 5000 already in use"

**Problem:** Another process is using port 5000

**Solution:**
1. Find what's using port 5000:
   ```powershell
   netstat -ano | findstr :5000
   ```
2. Kill that process, OR
3. Change port in `backend_api.py`:
   ```python
   app.run(host='0.0.0.0', port=5001, debug=True)
   ```
4. Update frontend to use new port in `App.tsx`

### Error: "ModuleNotFoundError: No module named 'flask'"

**Problem:** Dependencies not installed

**Solution:**
```powershell
.\venv\Scripts\python.exe -m pip install flask flask-cors
```

### Backend Starts but Model Not Loading

**Problem:** Model not downloaded

**Solution:**
```powershell
python download_model.py
```

### Frontend Shows Blank Page

**Problem:** Frontend dependencies not installed

**Solution:**
```powershell
cd frontend\deepfake
npm install
npm run dev
```

## 📋 Checklist

Before using the app, make sure:

- [ ] Backend is running (see "Running on http://0.0.0.0:5000")
- [ ] Frontend is running (see "Local: http://localhost:3000/")
- [ ] No error messages in backend terminal
- [ ] Browser is open to http://localhost:3000
- [ ] Backend terminal shows model loaded successfully

## 🔍 Testing the Connection

### Test Backend Health:
Open browser and go to: **http://localhost:5000/api/health**

You should see:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda",
  "cuda_available": true
}
```

### Test Model Info:
Go to: **http://localhost:5000/api/model-info**

You should see model information in JSON format.

## 💡 Tips

1. **Always start backend first** - Frontend needs backend to work
2. **Keep both terminals open** - Don't close them while using the app
3. **Check for errors** - Look at backend terminal for error messages
4. **Use START_ALL scripts** - They make it easier to start both servers

## 🎯 Using the App

1. **Upload Image** - Click "Select Image" or drag & drop
2. **Click Analyze** - Click "🔬 Analyze Image" button
3. **View Results** - See prediction, confidence, model info, and analysis

## 📞 Need Help?

1. Check backend terminal for errors
2. Check frontend browser console (F12) for errors
3. Run `python test_backend.py` to test backend
4. Make sure both servers are running

