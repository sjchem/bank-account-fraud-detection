# 🚀 Quick Deployment Reference

## 🏠 LOCAL DEVELOPMENT

```bash
# 1. Install dependencies
make install_local

# 2. In Terminal 1: Start API
make run_api

# 3. In Terminal 2: Start Dashboard
make run_streamlit

# 4. Access
# Dashboard: http://localhost:8501
# API Docs:  http://localhost:8000/docs
```

✅ **All 3 tabs working**
✅ **Fast development**
✅ **No cost**

---

## ☁️ CLOUD DEPLOYMENT

### Step 1: Deploy Dashboard to Streamlit Cloud

```bash
# Push code
git add .
git commit -m "Deploy ShieldBank"
git push origin main

# Then:
# 1. Go to https://share.streamlit.io
# 2. New app → Select repo → Deploy
# 3. Wait 2-3 minutes
```

✅ **Tabs 1 & 3 working** (Executive Summary, Model Performance)
❌ **Tab 2 needs API** (Fraud Deep Dive predictions)

---

### Step 2: Deploy API to Railway (Recommended)

```bash
# 1. Go to https://railway.app
# 2. Sign in with GitHub
# 3. New Project → Deploy from GitHub repo
# 4. Select: bank-account-fraud-detection
# 5. Railway auto-detects railway.json
# 6. Click Deploy

# 7. After deployment:
#    Settings → Domains → Generate domain
#    Copy URL: https://your-app.railway.app
```

---

### Step 3: Connect Dashboard to API

```bash
# Edit streamlit_app/app.py line 12:
API_URL = "https://your-app.railway.app/predict"

# Push changes
git add streamlit_app/app.py
git commit -m "Connect to Railway API"
git push origin main

# Streamlit Cloud auto-redeploys in ~1 minute
```

✅ **All 3 tabs now fully functional!**

---

## 🔀 ALTERNATIVE API PLATFORMS

### Render (100% Free)
```bash
# 1. Go to https://render.com
# 2. New → Web Service → Connect repo
# 3. Configure:
#    - Build: pip install -r requirements-api.txt
#    - Start: uvicorn api.fastapi:app --host 0.0.0.0 --port $PORT
# 4. Deploy
```

⚠️ **Free tier spins down after 15 min** (30s cold start)

### Heroku (Requires $5/month)
```bash
# Install CLI
brew install heroku/brew/heroku

# Deploy
heroku login
heroku create shieldbank-api
git push heroku main
```

---

## 📊 QUICK COMPARISON

| Setup | Dashboard | API | Cost | All Tabs? |
|-------|-----------|-----|------|-----------|
| **Local** | ✅ | ✅ | $0 | ✅ |
| **Streamlit Only** | ✅ | ❌ | $0 | ❌ (Tab 2 broken) |
| **Streamlit + Railway** | ✅ | ✅ | ~$0* | ✅ |
| **Streamlit + Render** | ✅ | ✅ | $0 | ✅ |

*Railway: $5 free credit/month (~500 hours)

---

## 🎯 RECOMMENDED WORKFLOWS

### For Development
```bash
make install_local
make run_api    # Terminal 1
make run_streamlit  # Terminal 2
```

### For Portfolio/Demo
```bash
# Dashboard: Streamlit Cloud (free)
# API: Railway (free $5 credit)
# = Full functionality, zero cost
```

### For Production
```bash
# Dashboard: Streamlit Cloud
# API: Railway/Render (paid tier)
# Add: Authentication, monitoring, alerts
```

---

## 🛠️ TROUBLESHOOTING

### Dashboard works but Tab 2 shows error?
```bash
# Check API is running
curl https://your-api-url.com/

# Should return: {"status": "ok", "message": "ShieldBank API"}
```

### Railway deployment failed?
```bash
# Check logs in Railway dashboard
# Verify railway.json exists
# Ensure requirements-api.txt has all packages
```

### Streamlit Cloud stuck on "Installing dependencies"?
```bash
# Check requirements.txt has:
# numpy>=1.23.0,<2.0.0  (NOT numpy==2.x)
```

---

## 📖 FULL DOCUMENTATION

- **Detailed Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Dashboard Features**: [SHIELDBANK_GUIDE.md](SHIELDBANK_GUIDE.md)
- **API Docs**: http://localhost:8000/docs (when running locally)

---

**Last Updated**: February 2026
