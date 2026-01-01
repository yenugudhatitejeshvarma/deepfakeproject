# Deployment Guide

This guide covers deploying the Deepfake Detection application to production.

## Architecture Overview

- **Frontend**: React + TypeScript + Vite (deploy to Vercel)
- **Backend**: Flask API with PyTorch ML model (deploy to Railway/Render/Fly.io)

## Frontend Deployment (Vercel)

### Prerequisites

1. GitHub account (recommended) or GitLab/Bitbucket
2. Vercel account (free tier available)

### Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Set the following configuration:
     - **Root Directory**: `frontend/deepfake`
     - **Framework Preset**: Vite
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
   
3. **Add Environment Variables**
   - In Vercel project settings, go to "Environment Variables"
   - Add: `VITE_API_URL` = `https://your-backend-url.com`
     - Replace with your deployed backend URL

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your frontend
   - Your app will be live at `https://your-project.vercel.app`

### Alternative: Deploy via Vercel CLI

```bash
cd frontend/deepfake
npm install -g vercel
vercel
```

## Backend Deployment

The backend requires Python 3.9+ and has a large ML model dependency. Recommended platforms:

### Option 1: Railway (Recommended)

Railway is excellent for ML models with GPU support.

1. **Create account** at [railway.app](https://railway.app)

2. **Create new project** and connect your GitHub repo

3. **Configure deployment**:
   - **Root Directory**: Leave empty (root of repo)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python backend_api.py`
   - **Python Version**: 3.11 or 3.12

4. **Add Environment Variables** (if needed):
   - `PORT`: Railway will auto-assign, Flask will use it
   - `PYTHON_VERSION`: 3.11

5. **Update backend_api.py** to use Railway's PORT:
   ```python
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port, debug=False)
   ```

6. **Deploy** - Railway will automatically deploy

### Option 2: Render

1. **Create account** at [render.com](https://render.com)

2. **Create new Web Service**
   - Connect your GitHub repository
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python backend_api.py`
   - **Environment**: Python 3
   - **Instance Type**: Standard (2GB RAM minimum)

3. **Environment Variables**:
   - `PORT`: Auto-assigned by Render

4. **Update backend_api.py** same as Railway

### Option 3: Fly.io

1. **Install Fly CLI**: 
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create fly.toml** (provided below)

3. **Deploy**:
   ```bash
   fly launch
   fly deploy
   ```

### Backend Configuration Update

Update `backend_api.py` to handle production deployment:

```python
# At the end of backend_api.py, replace:
app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

# With:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
```

Also update CORS to allow your frontend domain:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://your-frontend.vercel.app",  # Add your Vercel URL
            "https://*.vercel.app"  # Or allow all Vercel apps
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

## Complete Deployment Checklist

### Frontend (Vercel)
- [ ] Code pushed to GitHub
- [ ] Vercel project created
- [ ] Root directory set to `frontend/deepfake`
- [ ] Environment variable `VITE_API_URL` set to backend URL
- [ ] Build successful
- [ ] Frontend accessible via URL

### Backend (Railway/Render/Fly.io)
- [ ] Code pushed to GitHub
- [ ] Backend service created
- [ ] `requirements.txt` exists
- [ ] Backend code updated to use `PORT` environment variable
- [ ] Backend code updated to disable debug mode in production
- [ ] CORS updated to allow frontend domain
- [ ] Model downloads successfully on first run
- [ ] Backend accessible via URL
- [ ] Health check endpoint works: `https://your-backend-url.com/api/health`

### Testing
- [ ] Frontend can connect to backend
- [ ] Image upload works
- [ ] Detection returns results
- [ ] Visualization (heatmap) displays correctly
- [ ] Error handling works

## Environment Variables Reference

### Frontend (.env or Vercel)
- `VITE_API_URL`: Backend API URL (e.g., `https://your-backend.railway.app`)

### Backend (Railway/Render/Fly.io)
- `PORT`: Server port (auto-assigned by platform)
- `FLASK_ENV`: Set to `production` for production (optional)

## Troubleshooting

### Frontend can't connect to backend
- Check CORS configuration in backend
- Verify `VITE_API_URL` is set correctly
- Check backend URL is accessible in browser

### Backend fails to start
- Check logs for missing dependencies
- Verify Python version (3.9+)
- Check model downloads correctly
- Verify PORT environment variable is used

### Model loading fails
- Check internet connection for model download
- Verify HuggingFace token if model is private
- Check disk space on deployment platform

### Build fails
- Check `requirements.txt` is complete
- Verify Python version compatibility
- Check platform memory limits (ML models need 2GB+ RAM)

## Cost Considerations

- **Vercel**: Free tier (100GB bandwidth/month)
- **Railway**: Free tier with $5 credit/month
- **Render**: Free tier available (sleeps after 15 min inactivity)
- **Fly.io**: Free tier available with limitations

For production use, consider:
- Railway Pro ($20/month) for always-on backend
- Vercel Pro ($20/month) for more bandwidth
- Or use a VPS (DigitalOcean, AWS EC2) for full control

