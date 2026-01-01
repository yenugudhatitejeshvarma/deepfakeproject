# 🌐 Browser Extension Setup Guide

## ✅ Browser Extension Created!

Your Deepfake Detector web app can now run as a browser extension in **Microsoft Edge** and **Google Chrome**!

## 📁 Files Created

```
chrome-extension/
├── manifest.json       # Extension configuration
├── popup.html         # Extension popup UI
├── popup.js           # Extension logic
├── background.js      # Background service worker
├── icons/             # Extension icons (create these)
└── README.md          # Extension documentation
```

## 🚀 Quick Start

### Step 1: Start Backend (REQUIRED)

The extension needs your backend to be running:

```powershell
.\start_backend.ps1
```

### Step 2: Load Extension in Browser

**For Microsoft Edge:**
1. Open Microsoft Edge
2. Go to: `edge://extensions/`
3. Enable **Developer mode** (bottom-left toggle)
4. Click **"Load unpacked"**
5. Select the `chrome-extension` folder
6. Done!

**For Google Chrome:**
1. Open Chrome
2. Go to: `chrome://extensions/`
3. Enable **Developer mode** (top-right toggle)
4. Click **"Load unpacked"**
5. Select the `chrome-extension` folder
6. Done!

### Step 3: Use It!

1. Click the extension icon in Chrome toolbar
2. Select an image
3. Click "Analyze Image"
4. View results in the popup!

## 🎨 Features

- ✅ Same classic black and white UI
- ✅ Compact popup design
- ✅ Full deepfake detection
- ✅ All results displayed
- ✅ Easy to use

## 📝 Important Notes

1. **Backend Required:** Extension needs backend running on `http://localhost:5000`
2. **Works in Edge & Chrome:** Same extension works in both browsers
3. **Icons Optional:** Extension works without icon files (you can add them later)
4. **Same Functionality:** All features from web app work in extension
5. **No Icons:** Clean text-only interface (as requested)

## 🔧 Customization

To modify the extension:
- Edit `popup.html` for UI changes
- Edit `popup.js` for functionality
- Edit `manifest.json` for extension settings
- Reload extension in `chrome://extensions/` after changes

## 📖 More Info

See `chrome-extension/README.md` for detailed documentation.

## 🎯 That's It!

Your Chrome extension is ready. Just load it in Chrome and start using it!

