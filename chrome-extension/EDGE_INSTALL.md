# How to Install in Microsoft Edge

## Quick Installation Guide for Edge

### 1. Start Backend Server

**IMPORTANT:** You must start the backend server first!

```powershell
# In your project root directory
.\start_backend.ps1
```

Wait for: `Running on http://0.0.0.0:5000`

### 2. Load Extension in Microsoft Edge

1. Open Microsoft Edge browser
2. Go to: `edge://extensions/`
3. Enable **Developer mode** (toggle switch in bottom-left corner)
4. Click **"Load unpacked"** button
5. Navigate to and select the `chrome-extension` folder
6. The extension should appear in your extensions list

### 3. Pin Extension (Optional)

1. Click the puzzle piece icon in Edge toolbar
2. Click the pin icon next to "Deepfake Detector"
3. Now you can access it easily from the toolbar

### 4. Use the Extension

1. Click the extension icon in Edge toolbar
2. Click "Select Image"
3. Choose an image file
4. Click "Analyze Image"
5. View results!

## Verification

To verify everything works:

1. Backend running? Check: http://localhost:5000/api/health
2. Extension loaded? Check: edge://extensions/
3. Extension working? Click icon and try uploading an image

## Troubleshooting

### "Failed to connect to backend"

- Make sure backend is running: `.\start_backend.ps1`
- Check backend is on port 5000
- Verify: http://localhost:5000/api/health works in browser

### Extension not showing

- Make sure you enabled Developer mode
- Try reloading the extension (click refresh icon)
- Check for errors in edge://extensions/

### Icons missing

- This is okay! Extension works without icons
- Create icon PNG files if you want (16x16, 48x48, 128x128)

## Edge vs Chrome

The extension works identically in both browsers:
- ✅ Same functionality
- ✅ Same UI
- ✅ Same backend connection
- ✅ Same features

## That's It!

Your extension is ready to use in Microsoft Edge. Just make sure the backend is running whenever you want to use it.

