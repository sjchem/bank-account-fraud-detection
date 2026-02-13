# 🚀 ShieldBank Deployment Guide

This guide covers **two deployment strategies**:
1. **Local Development** - Run everything locally
2. **Cloud Deployment** - Dashboard on Streamlit Cloud + API on Railway/Render/Heroku

---

## 🏠 Local Development Setup

Use this for development and testing on your machine.

### 1. Install Dependencies
```bash
pip install -r requirements-local.txt
```

### 2. Run FastAPI Backend
```bash
make run_api
# Or manually:
uvicorn api.fastapi:app --reload --host 0.0.0.0 --port 8000
```

### 3. Run Streamlit Dashboard (New Terminal)
```bash
make run_streamlit
# Or manually:
streamlit run streamlit_app/app.py
```

### 4. Access Applications
- **Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/

### ✅ Local Benefits
- Full functionality (all 3 tabs working)
- Fast iteration and testing
- No deployment costs
- Complete control

---

## ☁️ Cloud Deployment (2-Part Strategy)

Deploy dashboard and API separately for public access.

### Part A: Deploy Dashboard to Streamlit Cloud

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy ShieldBank"
git push origin main
```

#### Step 2: Deploy on Streamlit Cloud
1. Visit: https://share.streamlit.io
2. Click "New app"
3. Repository: `your-username/bank-account-fraud-detection`
4. Branch: `main`
5. Main file path: `streamlit_app/app.py`
6. Click "Deploy" 🚀

#### Step 3: Wait ~2-3 minutes
Your dashboard will be live at: `https://your-app-name.streamlit.app`

**What works:** Tabs 1 & 3 (Executive Summary, Model Performance)
**What needs API:** Tab 2 (Fraud Deep Dive predictions)

---

### Part B: Deploy API to Cloud

Choose **ONE** of these platforms:

---

#### 🚂 Option 1: Railway (Recommended - Easiest)

1. **Visit Railway**
   - Go to: https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `bank-account-fraud-detection`

3. **Configure**
   - Railway auto-detects `railway.json`
   - It will use `requirements-api.txt` automatically
   - Click "Deploy"

4. **Get API URL**
   - After deployment, click "Settings" → "Domains"
   - Generate domain: `your-app.railway.app`
   - Your API URL: `https://your-app.railway.app`

5. **Test API**
   ```bash
   curl https://your-app.railway.app/
   # Should return: {"status": "ok", "message": "ShieldBank API"}
   ```

**Railway Free Tier:** $5 credit/month, ~500 hours

---

#### 🎨 Option 2: Render

1. **Visit Render**
   - Go to: https://render.com
   - Sign in with GitHub

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect repository: `bank-account-fraud-detection`

3. **Configure Settings**
   - Name: `shieldbank-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements-api.txt`
   - Start Command: `uvicorn api.fastapi:app --host 0.0.0.0 --port $PORT`

4. **Deploy**
   - Click "Create Web Service"
   - Wait ~5 minutes for deployment

5. **Get API URL**
   - Find URL in dashboard: `https://shieldbank-api.onrender.com`

**Render Free Tier:** Unlimited, but spins down after 15 min inactivity

---

#### 🟣 Option 3: Heroku

1. **Install Heroku CLI**
   ```bash
   # Mac
   brew install heroku/brew/heroku

   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create shieldbank-api
   ```

3. **Configure**
   ```bash
   # Heroku auto-detects Procfile
   git push heroku main
   ```

4. **Get API URL**
   ```bash
   heroku open
   # URL: https://shieldbank-api.herokuapp.com
   ```

**Heroku Free Tier:** Discontinued (requires $5/month Eco plan)

---

### Part C: Connect Dashboard to API

After deploying API, update Streamlit dashboard:

1. **Edit streamlit_app/app.py**
   ```python
   # Line 12 - Replace with your API URL
   API_URL = "https://your-app.railway.app/predict"
   # Or for Render: "https://shieldbank-api.onrender.com/predict"
   # Or for Heroku: "https://shieldbank-api.herokuapp.com/predict"
   ```

2. **Push Changes**
   ```bash
   git add streamlit_app/app.py
   git commit -m "Connect to cloud API"
   git push origin main
   ```

3. **Streamlit Cloud Auto-Redeploys**
   - Wait ~1 minute
   - Tab 2 will now work with predictions!

---

## 📋 Deployment Comparison

| Platform | Dashboard | API | Free Tier | Best For |
|----------|-----------|-----|-----------|----------|
| **Local** | ✅ | ✅ | Unlimited | Development |
| **Streamlit Cloud** | ✅ | ❌ | Unlimited | Dashboard demos |
| **Railway** | ❌ | ✅ | $5 credit/mo | API (recommended) |
| **Render** | ❌ | ✅ | Unlimited* | API (free) |
| **Heroku** | ❌ | ✅ | $5/month | Legacy projects |

*Render free tier spins down after 15 min inactivity (cold start: 30s)

---

## 🎯 Recommended Setup

**For Development:**
```bash
# Run everything locally
pip install -r requirements-local.txt
make run_api && make run_streamlit
```

**For Portfolio/Demo:**
```bash
# Dashboard on Streamlit Cloud (free)
# API on Railway (free $5 credit)
# Full functionality with zero cost
```

**For Production:**
```bash
# Dashboard on Streamlit Cloud
# API on Railway/Render with paid tier
# Add authentication & monitoring
```

---

## 🐛 Troubleshooting

### Dashboard deployed but Tab 2 doesn't work?
- Check if API is running: Visit `https://your-api-url.com/`
- Verify `API_URL` in streamlit_app/app.py matches your API URL
- Check Railway/Render logs for errors

### NumPy version conflicts on Streamlit Cloud?
- Make sure you're using `requirements.txt` (not requirements-local.txt)
- Check numpy version: `numpy>=1.23.0,<2.0.0`

### Railway deployment failing?
- Verify `railway.json` exists
- Check `requirements-api.txt` has all needed packages
- View build logs in Railway dashboard

### API returns 404 on /predict?
- Visit `/docs` endpoint: `https://your-api-url.com/docs`
- Test prediction endpoint there
- Check FastAPI route is `/predict` (not `/api/predict`)

---

## 📦 Dependency Files Reference

| File | Purpose | Used By |
|------|---------|---------|
| `requirements.txt` | Streamlit Cloud | Streamlit Cloud deployment |
| `requirements-local.txt` | Full local dev | Local development |
| `requirements-api.txt` | API only (minimal) | Railway/Render/Heroku |
| `Procfile` | Heroku start command | Heroku |
| `railway.json` | Railway config | Railway |
| `render.yaml` | Render config | Render |

---

## ✅ Quick Checklist

### Before Deploying:
- [ ] Code pushed to GitHub
- [ ] Model files exist in `models/` folder
- [ ] API works locally (`localhost:8000/docs`)
- [ ] Dashboard works locally (`localhost:8501`)

### After Deploying:
- [ ] Dashboard loads on Streamlit Cloud
- [ ] Tab 1 & 3 work without errors
- [ ] API is accessible (test `/` endpoint)
- [ ] Tab 2 connects to API successfully
- [ ] Predictions return valid results

---

**Need help?** Check logs:
- Streamlit Cloud: Click "Manage app" → "Logs"
- Railway: Dashboard → "Deployments" → "View Logs"
- Render: Dashboard → "Logs" tab

---

## 🎨 Customization

Edit `.streamlit/config.toml` to change:
- Colors (bank blue theme)
- Fonts
- Layout

Already configured with ShieldBank branding! 🛡️

---

## 📊 Your Live Demo Link

After deployment, share your link:
```
🌐 https://shieldbank-fraud-detection.streamlit.app
```

Perfect for:
- Portfolio showcase
- Job applications
- Hackathon demos
- Client presentations

---

## 🆘 Troubleshooting

**Build fails with dependency errors:**
→ Use `requirements-minimal.txt`

**Dashboard loads but form doesn't work:**
→ Expected! API not deployed. Demo modes work fine.

**Slow loading:**
→ First load is slow, caching helps after that

**Need API working:**
→ Deploy FastAPI separately (Railway, Render, etc.)

---

## ✅ Success Criteria

Your app is working if you can:
1. ✅ See the ShieldBank header
2. ✅ Click "Start Live Monitoring" and see transactions
3. ✅ View heatmap and charts
4. ✅ Navigate between tabs

You're live! 🎉
