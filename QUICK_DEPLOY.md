# Quick Deployment Guide

## Frontend → Vercel (5 minutes)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repo
   - **IMPORTANT**: Set **Root Directory** to `frontend/deepfake`:
     - Click **"Edit"** next to "Root Directory" 
     - Enter: `frontend/deepfake`
     - Click **Save**
   - Framework will auto-detect as Vite
   - Add Environment Variable: `VITE_API_URL` = `https://your-backend-url.com`
   - Click **Deploy**
   
   **If you see "No flask entrypoint found" error:**
   - Go to Project Settings → General → Root Directory
   - Make sure it's set to `frontend/deepfake`
   - Save and Redeploy
   
   **Note**: The root `vercel.json` prevents Flask detection, but setting Root Directory is the best solution.

3. **Done!** Your frontend is live at `https://your-project.vercel.app`

## Backend → Railway (Recommended)

1. **Go to** [railway.app/new](https://railway.app/new)

2. **New Project** → **Deploy from GitHub repo**

3. **Settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python backend_api.py`

4. **Get your URL** from Railway dashboard (e.g., `https://your-app.railway.app`)

5. **Update Frontend**: In Vercel, set `VITE_API_URL` = your Railway URL

## Alternative: Render.com

1. **Go to** [render.com/dashboard](https://render.com/dashboard)

2. **New** → **Web Service**

3. **Settings**:
   - Build: `pip install -r requirements.txt`
   - Start: `python backend_api.py`
   - Instance: Standard (2GB RAM)

4. **Deploy** and copy your URL

## Testing

1. Frontend: Upload an image
2. Check browser console for errors
3. Verify API calls go to your backend URL

## Troubleshooting

- **Frontend can't connect**: Check `VITE_API_URL` in Vercel settings
- **Backend fails**: Check Railway/Render logs
- **CORS errors**: Backend allows all origins by default (check `backend_api.py`)

## Cost

- **Vercel**: Free (100GB/month)
- **Railway**: $5 free credit/month
- **Render**: Free (sleeps after 15 min)

