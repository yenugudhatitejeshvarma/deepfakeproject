# Deepfake Detector Browser Extension

A browser extension version of the Deepfake Detection web application. Works in both **Chrome** and **Microsoft Edge**.

## Installation

### For Microsoft Edge

1. Open Edge and go to `edge://extensions/`
2. Enable "Developer mode" (toggle in bottom-left)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. Done! See `EDGE_INSTALL.md` for detailed instructions

### For Google Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. Done! See `INSTALL.md` for detailed instructions

### Icons (Optional)

Icons are optional - the extension works without them. If you want icons:
- Create icon files in `chrome-extension/icons/`:
  - `icon16.png` (16x16 pixels)
  - `icon48.png` (48x48 pixels)
  - `icon128.png` (128x128 pixels)

### Step 4: Start Backend Server

**Important:** The backend must be running for the extension to work!

```powershell
# In your project directory
.\start_backend.ps1
```

Or:

```cmd
start_backend.bat
```

Make sure the backend is running on `http://localhost:5000`

### Step 5: Use the Extension

1. Click the extension icon in Chrome toolbar
2. Click "Select Image" to choose an image
3. Click "Analyze Image"
4. View the results in the popup

## Features

- ✅ Clean, classic black and white UI
- ✅ Image upload and preview
- ✅ Deepfake detection analysis
- ✅ Detailed results display
- ✅ Model information
- ✅ Analysis metrics

## Requirements

- Microsoft Edge or Google Chrome browser (latest version)
- Backend server running on `http://localhost:5000`
- Backend API must be accessible

## Troubleshooting

### Extension doesn't work

1. Make sure backend is running: `http://localhost:5000/api/health`
2. Check browser console for errors:
   - **Edge:** Right-click extension icon > Inspect popup
   - **Chrome:** Right-click extension icon > Inspect popup
3. Verify backend URL in `popup.js` (should be `http://localhost:5000`)

### CORS Errors

The extension should work because it uses `host_permissions` in manifest.json. If you see CORS errors:
1. Make sure backend has CORS enabled
2. Check that backend is running on the correct port

### Icons Missing

Icons are optional. You can:
- Create simple PNG icons
- Or ignore the warning - extension will work without icons

## File Structure

```
chrome-extension/
├── manifest.json      # Extension configuration
├── popup.html        # Popup HTML
├── popup.js          # Popup functionality
├── background.js     # Background service worker
├── icons/            # Extension icons (optional)
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── README.md         # This file
```

## Development

To modify the extension:
1. Edit files in `chrome-extension/`
2. Go to `edge://extensions/` (Edge) or `chrome://extensions/` (Chrome)
3. Click the refresh icon on the extension card
4. Test your changes

## Notes

- The extension connects to your local backend
- Works only when backend is running
- Classic black and white design
- No external dependencies required (after loading)

