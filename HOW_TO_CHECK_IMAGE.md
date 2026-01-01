# How to Check an Image with the Deepfake Detector

## Quick Command

```bash
python run_model.py <image_path>
```

## Examples

### 1. Image in Current Directory
```bash
python run_model.py 1.png
python run_model.py i.png
python run_model.py myimage.jpg
```

### 2. Image in Another Directory (Full Path)
```bash
python run_model.py "C:\Users\YourName\Pictures\image.png"
python run_model.py "T:\deepfakeproject\images\test.jpg"
```

### 3. Image in Subdirectory (Relative Path)
```bash
python run_model.py images\i.png
python run_model.py data\test\photo.jpg
```

### 4. Using Wrapper Scripts
```powershell
# PowerShell
.\run_model.ps1 i.png

# Batch file
run_model.bat i.png
```

## Supported Image Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- Any format supported by PIL/Pillow

## Interactive Mode
If you don't provide an image path, it will ask you:
```bash
python run_model.py
# Then enter the path when prompted
```

## Current Available Images
Based on your directory, you currently have:
- `1.png` ✅

## If Your Image is Named "i.png"
1. Make sure the file exists in the directory
2. Check the exact filename (case-sensitive on some systems)
3. Use the full path if it's in another location

