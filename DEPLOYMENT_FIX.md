# Vercel Deployment Fix Instructions

## The Problem
Vercel is detecting Flask backend files in the root directory and trying to deploy them as a serverless function, causing the error:
```
Error: No flask entrypoint found. Add an 'app' script...
```

## The Solution (Choose ONE method)

### Method 1: Set Root Directory in Vercel Settings (RECOMMENDED)

1. Go to your Vercel project dashboard
2. Click **Settings** → **General**
3. Scroll down to **Root Directory**
4. Click **Edit**
5. Enter: `frontend/deepfake`
6. Click **Save**
7. Go to **Deployments** tab and click **Redeploy**

This tells Vercel to ONLY look at the `frontend/deepfake` directory and ignore everything else.

### Method 2: Use the Root vercel.json (Alternative)

If you can't set Root Directory, we've added a minimal `vercel.json` at the root that prevents Flask detection. This should work automatically.

## Verify It's Working

After deploying, check the build logs. You should see:
- ✅ Building frontend/deepfake
- ✅ npm install
- ✅ npm run build
- ✅ Deploying dist/

You should NOT see:
- ❌ Flask detection
- ❌ Python backend errors
- ❌ "No flask entrypoint found"

## Still Having Issues?

If you still see Flask errors:

1. **Double-check Root Directory setting** in Vercel project settings
2. **Clear Vercel cache**: Settings → General → Clear Build Cache
3. **Redeploy**: Deployments → Latest → Redeploy

## Current Configuration

- Root `vercel.json`: Minimal config to prevent Flask detection
- `frontend/deepfake/vercel.json`: Frontend build configuration
- `.vercelignore`: Additional ignore patterns (backup)

The frontend should build and deploy successfully!

