# Deployment Guide

This guide will help you deploy BioRoute Builder online using free/low-cost hosting services.

## Architecture

- **Frontend**: Deploy to Vercel (recommended) or Netlify
- **Backend**: Deploy to Render (recommended) or Railway
- **Database**: Use Render PostgreSQL or Supabase

## Option 1: Render (Recommended - All-in-One)

Render provides both backend hosting and PostgreSQL database on their free tier.

### Step 1: Deploy Backend to Render

1. **Create a Render account**: https://render.com

2. **Create a new PostgreSQL database**:
   - Go to https://dashboard.render.com/new/database
   - Name: `bioroute-db`
   - Database: `bioroute`
   - User: `bioroute`
   - Click "Create Database"
   - **Copy the Internal Database URL** (starts with `postgresql://`)

3. **Create a new Web Service**:
   - Go to https://dashboard.render.com/create?type=web
   - Connect your GitHub repository: `aikiesan/lego_rotas`
   - Configure:
     - **Name**: `bioroute-backend`
     - **Region**: Choose closest to you
     - **Branch**: `claude/setup-bioroute-project-016kVaJNX3KPteK92yLwh6kV` (or main after merging)
     - **Root Directory**: `backend`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables** (in Render dashboard):
   ```
   DATABASE_URL=<paste-your-internal-database-url>
   POSTGRES_PASSWORD=<your-db-password-from-render>
   DEBUG=False
   ```

5. **Deploy**: Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Copy your backend URL: `https://bioroute-backend.onrender.com`

### Step 2: Deploy Frontend to Vercel

1. **Create a Vercel account**: https://vercel.com

2. **Import your GitHub repository**:
   - Go to https://vercel.com/new
   - Import `aikiesan/lego_rotas`
   - Configure:
     - **Framework Preset**: `Vite`
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

3. **Add Environment Variable**:
   - Go to Settings → Environment Variables
   - Add:
     ```
     VITE_API_URL=https://bioroute-backend.onrender.com/api
     ```
   - (Replace with your actual Render backend URL)

4. **Deploy**: Click "Deploy"
   - Wait 2-3 minutes
   - Your frontend will be live at: `https://bioroute-builder.vercel.app`

### Step 3: Update CORS

Update your backend to allow your Vercel domain:

1. Edit `backend/main.py` line 16-21:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://bioroute-builder.vercel.app",  # Your Vercel domain
           "http://localhost:3000"  # For local development
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. Commit and push to trigger redeploy on Render.

---

## Option 2: Railway (Alternative)

Railway offers similar services with a generous free tier.

### Deploy Backend to Railway

1. **Create Railway account**: https://railway.app

2. **Create New Project**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `aikiesan/lego_rotas`
   - Choose `backend` directory

3. **Add PostgreSQL**:
   - In your project, click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically create DATABASE_URL variable

4. **Configure Service**:
   - Select your backend service
   - Settings → Environment:
     ```
     PORT=8000
     DEBUG=False
     ```
   - Settings → Deploy:
     - Root Directory: `backend`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Generate Domain**:
   - Settings → Networking → "Generate Domain"
   - Copy your URL: `https://bioroute-backend.up.railway.app`

### Deploy Frontend to Vercel

(Same as Option 1 Step 2 above, but use your Railway backend URL)

---

## Option 3: Netlify (Frontend Alternative)

If you prefer Netlify over Vercel for the frontend:

1. **Create Netlify account**: https://netlify.com

2. **Deploy**:
   - Import from GitHub: `aikiesan/lego_rotas`
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **Environment Variables**:
   - Site settings → Environment variables
   - Add: `VITE_API_URL=https://your-backend-url.onrender.com/api`

4. **Deploy**: Click "Deploy site"

---

## Quick Start (Fastest Deployment)

### 1-Click Deploy to Render (Backend + Database)

Create a `render.yaml` file in your repository root:

```yaml
services:
  - type: web
    name: bioroute-backend
    runtime: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DEBUG
        value: False

databases:
  - name: bioroute-db
    databaseName: bioroute
    user: bioroute
```

Then click: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

---

## Post-Deployment Checklist

- [ ] Backend is accessible at your Render/Railway URL
- [ ] Test API: `https://your-backend.onrender.com/api/technologies`
- [ ] Frontend loads at your Vercel/Netlify URL
- [ ] Frontend can connect to backend (check browser console)
- [ ] CORS is configured correctly
- [ ] Environment variables are set
- [ ] PostgreSQL database is connected
- [ ] Try loading a template and calculating results

---

## Cost Estimates

### Free Tier (Sufficient for MVP/Testing)
- **Render**: Free tier includes 750 hours/month
- **Vercel**: Unlimited bandwidth for personal projects
- **PostgreSQL**: 1GB free on Render
- **Total**: $0/month

### Paid (For Production)
- **Render**: $7/month (web service) + $7/month (PostgreSQL)
- **Vercel**: Free (Pro: $20/month for team features)
- **Total**: ~$14-34/month

---

## Monitoring

### Render Dashboard
- View logs: Dashboard → Your service → Logs
- Check metrics: CPU, Memory usage
- Database connections: PostgreSQL service → Metrics

### Vercel Analytics
- Enable in Project Settings → Analytics
- Track page views, performance, errors

---

## Troubleshooting

### Backend Won't Start
- Check Render logs for Python errors
- Verify `requirements.txt` has all dependencies
- Ensure `DATABASE_URL` environment variable is set

### Frontend Can't Connect to Backend
- Verify `VITE_API_URL` is set correctly
- Check CORS settings in `backend/main.py`
- Test backend API directly in browser

### Database Connection Errors
- Verify `DATABASE_URL` format: `postgresql://user:password@host:port/database`
- Check database is running in Render dashboard
- Ensure backend and database are in same region

### 502 Bad Gateway
- Backend is starting (wait 1-2 minutes)
- Or backend crashed (check logs)

---

## Custom Domain (Optional)

### Vercel (Frontend)
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### Render (Backend)
1. Go to Service Settings → Custom Domain
2. Add your domain
3. Update CNAME record in your DNS

---

## Scaling for Production

When you're ready to handle more traffic:

1. **Render**: Upgrade to Standard instance ($7/month)
2. **PostgreSQL**: Upgrade to 4GB ($7/month) or 16GB ($15/month)
3. **Enable Auto-scaling**: Configure in Render dashboard
4. **Add Redis**: For caching calculation results
5. **CDN**: Vercel handles this automatically
6. **Monitoring**: Add Sentry or LogRocket

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app

Happy deploying! 🚀
