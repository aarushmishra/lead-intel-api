# ☁️ Cloud Deployment Guide

## 🚀 Quick Deploy Options

### **Option 1: Railway (Recommended - Easiest)**

1. **Sign up**: Go to [railway.app](https://railway.app) and create account
2. **Connect GitHub**: Link your GitHub repository
3. **Deploy**: Click "Deploy from GitHub repo"
4. **Get URL**: Railway will give you a public URL like `https://lead-intel-api-production.up.railway.app`

**Commands:**
```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy
railway up
```

### **Option 2: Render (Free Tier)**

1. **Sign up**: Go to [render.com](https://render.com) and create account
2. **New Web Service**: Click "New Web Service"
3. **Connect GitHub**: Link your repository
4. **Configure**:
   - **Name**: `lead-intel-api`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Deploy**: Click "Create Web Service"

### **Option 3: Heroku**

1. **Sign up**: Go to [heroku.com](https://heroku.com) and create account
2. **Install CLI**: `brew install heroku/brew/heroku`
3. **Login**: `heroku login`
4. **Create app**: `heroku create lead-intel-api`
5. **Deploy**: `git push heroku main`

## 📋 Pre-Deployment Checklist

- [ ] All tests passing: `python -m pytest tests/ -v`
- [ ] Docker build works: `docker build -t lead-intel-api .`
- [ ] Local API works: `curl http://localhost:8000/health`
- [ ] Code committed to GitHub
- [ ] Environment variables configured

## 🔧 Environment Variables

Set these in your cloud platform:

```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
PORT=8000  # Usually auto-set by platform
```

## 🌐 Post-Deployment Testing

Once deployed, test your API:

### **Health Check**
```bash
curl https://your-app-url.railway.app/health
```

### **Test Lead Enrichment**
```bash
curl -X POST "https://your-app-url.railway.app/enrich_lead" \
  -H "Content-Type: application/json" \
  -d '{
    "college": "ADYPU",
    "city": "Pune",
    "state": "Maharashtra",
    "course": "BBA",
    "language": "Hindi"
  }'
```

## 📊 Monitoring Your Deployment

### **Railway Dashboard**
- View logs in real-time
- Monitor resource usage
- Set up alerts

### **Render Dashboard**
- Automatic health checks
- Log streaming
- Performance metrics

### **Heroku Dashboard**
- Dyno metrics
- Log streams
- Add-ons for monitoring

## 🔄 Continuous Deployment

### **GitHub Actions (Optional)**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
```

## 🚨 Troubleshooting

### **Common Issues**

1. **Port Issues**
   ```bash
   # Make sure your app uses $PORT environment variable
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Dependencies**
   ```bash
   # Check requirements.txt is up to date
   pip freeze > requirements.txt
   ```

3. **Health Check Failing**
   ```bash
   # Ensure /health endpoint returns 200
   curl https://your-app-url/health
   ```

### **Debug Commands**

```bash
# Check logs
railway logs  # Railway
render logs   # Render
heroku logs   # Heroku

# SSH into container (if supported)
railway shell
```

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans | Ease of Use |
|----------|-----------|------------|-------------|
| Railway  | $5/month credit | Pay-as-you-use | ⭐⭐⭐⭐⭐ |
| Render   | 750 hours/month | $7/month+ | ⭐⭐⭐⭐ |
| Heroku   | 550-1000 hours/month | $7/month+ | ⭐⭐⭐ |
| AWS      | 12 months free | Pay-as-you-use | ⭐⭐ |

## 🎯 Recommended Approach

1. **Start with Railway** (easiest, good free tier)
2. **Test thoroughly** with the provided cURL commands
3. **Monitor performance** and usage
4. **Scale up** if needed (Railway → Render → AWS)

## 📞 Support

- **Railway**: [Discord](https://discord.gg/railway)
- **Render**: [Documentation](https://render.com/docs)
- **Heroku**: [Support](https://help.heroku.com)

---

**🚀 Your Lead Intel API will be live and accessible from anywhere!** 