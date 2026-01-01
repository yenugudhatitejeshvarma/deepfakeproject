# How to Install Deepfake Detector Chrome Extension

## Quick Installation Guide

### 1. Create Icons Folder (Optional)

Create a folder called `icons` inside `chrome-extension/`:

```
chrome-extension/
  └── icons/
```

Icons are optional - the extension works without them.

### 2. Start Backend Server

**IMPORTANT:** You must start the backend server first!

```powershell
# In your project root directory
.\start_backend.ps1
```

Wait for: `Running on http://0.0.0.0:5000`

### 3. Load Extension in Chrome

1. Open Chrome browser
2. Go to: `chrome://extensions/`
3. Enable **Developer mode** (toggle switch in top-right corner)
4. Click **"Load unpacked"** button
5. Navigate to and select the `chrome-extension` folder
6. The extension should appear in your extensions list

### 4. Pin Extension (Optional)

1. Click the puzzle piece icon in Chrome toolbar
2. Click the pin icon next to "Deepfake Detector"
3. Now you can access it easily from the toolbar

### 5. Use the Extension

1. Click the extension icon in Chrome toolbar
2. Click "Select Image"
3. Choose an image file
4. Click "Analyze Image"
5. View results!

## Verification

To verify everything works:

1. Backend running? Check: http://localhost:5000/api/health
2. Extension loaded? Check: chrome://extensions/
3. Extension working? Click icon and try uploading an image

## Troubleshooting

### "Failed to connect to backend"

- Make sure backend is running: `.\start_backend.ps1`
- Check backend is on port 5000
- Verify: http://localhost:5000/api/health works in browser

### Extension not showing

- Make sure you enabled Developer mode
- Try reloading the extension (click refresh icon)
- Check for errors in chrome://extensions/

### Icons missing

- This is okay! Extension works without icons
- Create icon PNG files if you want (16x16, 48x48, 128x128)

## That's It!

Your extension is ready to use. Just make sure the backend is running whenever you want to use it.

