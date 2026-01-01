# 🔧 Connection Fix - Backend and Frontend

## ✅ What Was Fixed

1. **Added Root Route** - Now `/` endpoint returns API information
2. **Improved CORS Configuration** - Explicitly allows localhost:3000
3. **Added OPTIONS Handler** - Better CORS preflight support
4. **Enhanced Error Handling** - Better error messages

## 🚀 How to Fix Connection Issues

### Step 1: Restart Backend

**Stop the current backend** (Ctrl+C in the backend terminal), then restart:

```powershell
.\start_backend.ps1
```

**OR**

```cmd
start_backend.bat
```

Wait for this message:
```
============================================================
Server starting on http://localhost:5000
 * Running on http://0.0.0.0:5000
```

### Step 2: Verify Backend is Working

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

### Step 3: Check Frontend Connection

1. Make sure frontend is running on **http://localhost:3000**
2. Open browser console (F12)
3. Try uploading an image
4. Check for any errors in console

## 🔍 Troubleshooting

### "Not Found" Error

**If you see "Not Found" error:**

1. **Check the URL** - Make sure you're accessing `/api/detect` (POST), not `/`
2. **Verify backend is running** - Check http://localhost:5000/api/health
3. **Check frontend console** - Look for CORS or connection errors

### CORS Errors

**If you see CORS errors in browser console:**

1. Make sure backend has restarted with new CORS configuration
2. Check that frontend is on `http://localhost:3000`
3. Verify CORS is enabled in backend

### Connection Refused

**If you see "Connection Refused":**

1. Backend is not running - Start it with `.\start_backend.ps1`
2. Port 5000 is blocked - Check firewall settings
3. Wrong port - Verify backend is on port 5000

## ✅ Testing the Connection

### Test 1: Backend Health Check
```powershell
# In PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/api/health" -UseBasicParsing
```

### Test 2: Backend Root
```powershell
# In PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/" -UseBasicParsing
```

### Test 3: Frontend to Backend
1. Open http://localhost:3000 in browser
2. Open Developer Tools (F12)
3. Go to Network tab
4. Upload an image and click Analyze
5. Check if request to `/api/detect` succeeds

## 📝 Important Notes

1. **Backend must be running first** - Always start backend before frontend
2. **Restart after changes** - If you modify backend code, restart it
3. **Check ports** - Backend: 5000, Frontend: 3000
4. **CORS is configured** - Should work automatically now

## 🎯 Expected Flow

1. User uploads image in frontend (http://localhost:3000)
2. Frontend sends POST request to http://localhost:5000/api/detect
3. Backend processes image with deepfake detection model
4. Backend returns JSON response with results
5. Frontend displays results

## ✅ Success Indicators

- ✅ Backend shows "Running on http://0.0.0.0:5000"
- ✅ http://localhost:5000/api/health returns JSON
- ✅ Frontend loads without errors
- ✅ Image upload works
- ✅ Analysis results appear

If all these work, your connection is fixed! 🎉

