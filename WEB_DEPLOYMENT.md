# 🌐 Web Application Deployment Guide

Complete guide to deploy your Trip Planner Agent as a web application that anyone can access!

## 📋 Table of Contents
- [Quick Start (Local Testing)](#quick-start-local-testing)
- [Deployment Option 1: Railway (Recommended)](#deployment-option-1-railway-recommended)
- [Deployment Option 2: Render](#deployment-option-2-render)
- [Deployment Option 3: Vercel + Backend](#deployment-option-3-vercel--backend)
- [Environment Variables](#environment-variables)
- [Custom Domain Setup](#custom-domain-setup)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start (Local Testing)

### Step 1: Install Dependencies

```bash
# Make sure you're in the project directory
cd Trip_Planner_Agent

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install/update dependencies (including Flask)
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Make sure your `.env` file exists with your API key:
```bash
# .env file
ANTHROPIC_API_KEY=your_claude_api_key_here
```

### Step 3: Start the Backend Server

```bash
# Start Flask backend
python web_app/backend/app.py
```

You should see:
```
🚀 Starting Trip Planner Agent API Server...
📍 API available at: http://localhost:5000
```

### Step 4: Open the Frontend

Open a new terminal and run:

```bash
# Serve the frontend (multiple options)

# Option 1: Using Python's built-in server
cd web_app/frontend/public
python3 -m http.server 8080

# Option 2: Using Node.js http-server (if you have it)
cd web_app/frontend/public
npx http-server -p 8080

# Option 3: Just open the HTML file directly in your browser
open web_app/frontend/public/index.html  # macOS
# or double-click index.html on Windows
```

### Step 5: Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000

Try planning a trip! Enter: "Plan a 3-day trip to Tokyo for food and culture"

---

## 🚂 Deployment Option 1: Railway (Recommended)

Railway offers the simplest deployment with free tier and automatic HTTPS.

### Prerequisites
- GitHub account
- Railway account (sign up at https://railway.app)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub** (if not already):
```bash
git add .
git commit -m "Add web application"
git push origin main
```

2. **Create `railway.json`** in project root:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python web_app/backend/app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

3. **Create `Procfile`** in project root:
```
web: python web_app/backend/app.py
```

4. **Update `app.py`** to use environment port:

Edit `web_app/backend/app.py` line 232:
```python
if __name__ == '__main__':
    print("🚀 Starting Trip Planner Agent API Server...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Step 2: Deploy to Railway

1. Go to https://railway.app
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `Trip_Planner_Agent` repository
4. Railway will automatically detect Python and start building

### Step 3: Configure Environment Variables

1. In Railway dashboard, click your project
2. Go to **"Variables"** tab
3. Add:
   ```
   ANTHROPIC_API_KEY=your_claude_api_key_here
   PORT=5000
   ```

### Step 4: Update Frontend API URL

After deployment, Railway gives you a URL like: `https://trip-planner-production.up.railway.app`

**Option A: Deploy Frontend to Railway Too**

Create a second Railway service for the frontend:
1. Create `web_app/frontend/railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd public && python3 -m http.server $PORT"
  }
}
```

2. Update `app.js` line 2:
```javascript
const API_BASE_URL = 'https://your-backend-url.railway.app/api';
```

**Option B: Use Netlify/Vercel for Frontend (Free)**

See Option 3 below.

### Step 5: Test Your Deployment

Visit your Railway URL and test the trip planner!

---

## 🎨 Deployment Option 2: Render

Render offers free tier with auto-deploy from GitHub.

### Step 1: Prepare Files

1. **Create `render.yaml`** in project root:
```yaml
services:
  - type: web
    name: trip-planner-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python web_app/backend/app.py
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: PORT
        value: 10000
```

2. **Update `app.py`** (same as Railway step above)

### Step 2: Deploy to Render

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Add your `ANTHROPIC_API_KEY` in Environment Variables
6. Click **"Create Web Service"**

### Step 3: Deploy Frontend

Same as Railway - deploy to Netlify/Vercel (see Option 3).

---

## ⚡ Deployment Option 3: Vercel + Backend

Split deployment: Frontend on Vercel (fast), Backend on Railway/Render.

### Deploy Frontend to Vercel

1. **Install Vercel CLI** (optional):
```bash
npm i -g vercel
```

2. **Create `vercel.json`** in `web_app/frontend/`:
```json
{
  "version": 2,
  "public": true,
  "builds": [
    {
      "src": "public/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/public/$1"
    }
  ]
}
```

3. **Deploy**:
```bash
cd web_app/frontend
vercel --prod
```

OR use Vercel website:
1. Go to https://vercel.com
2. Import your GitHub repository
3. Set root directory to `web_app/frontend/public`
4. Deploy!

4. **Update API URL** in `app.js`:
```javascript
const API_BASE_URL = 'https://your-backend-url.railway.app/api';
```

### Deploy Backend

Use Railway or Render (see options above).

---

## 🔐 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Claude API key | `sk-ant-api03-...` |
| `PORT` | Server port (auto-set by host) | `5000` or `10000` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `CORS_ORIGINS` | Allowed origins for CORS | `*` |

### Setting Environment Variables

**Railway**: Project → Variables tab

**Render**: Dashboard → Environment section

**Vercel**: Project Settings → Environment Variables

**Local**: `.env` file in project root

---

## 🌍 Custom Domain Setup

### Railway

1. Go to your service → Settings
2. Click **"Generate Domain"** for free subdomain
3. Or add custom domain:
   - Click **"Custom Domain"**
   - Add your domain (e.g., `trip-planner.yourdomain.com`)
   - Update DNS records as shown

### Render

1. Go to your service → Settings
2. Scroll to **"Custom Domains"**
3. Add your domain and follow DNS instructions

### Vercel

1. Go to your project → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

---

## 🔧 Troubleshooting

### Frontend Can't Connect to Backend

**Problem**: CORS errors or "Failed to fetch"

**Solutions**:

1. **Check CORS is enabled** in `app.py`:
```python
from flask_cors import CORS
CORS(app)  # This should be present
```

2. **Update API URL** in `app.js`:
```javascript
// Make sure this matches your backend URL
const API_BASE_URL = 'https://your-actual-backend-url.com/api';
```

3. **For production**, restrict CORS:
```python
CORS(app, origins=['https://your-frontend-url.com'])
```

### Backend Crashes on Startup

**Problem**: "Module not found" or import errors

**Solution**:

1. Check `requirements.txt` has all dependencies
2. Ensure build command installs dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### "Invalid API Key" Errors

**Problem**: Claude API returns 401 errors

**Solution**:

1. Verify environment variable is set correctly
2. Check for extra spaces: `ANTHROPIC_API_KEY=sk-ant-api03-...` (no spaces)
3. Regenerate API key if needed: https://console.anthropic.com/

### Itinerary Not Showing

**Problem**: Trip plans but nothing displays

**Solution**:

1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify backend returns correct JSON:
   ```bash
   curl -X POST http://your-backend/api/plan \
     -H "Content-Type: application/json" \
     -d '{"message": "Plan a 3-day trip to Tokyo"}'
   ```

### Deployment Build Fails

**Problem**: Railway/Render build fails

**Solutions**:

1. **Check Python version** (add `runtime.txt`):
   ```
   python-3.10.13
   ```

2. **Verify requirements.txt** is in root directory

3. **Check build logs** for specific errors

4. **Common fixes**:
   ```bash
   # If psycopg2 fails, use binary version
   pip install psycopg2-binary

   # If numpy fails, add to requirements
   pip install numpy
   ```

---

## 📊 Monitoring & Analytics

### Add Basic Analytics

Add to `index.html` before `</head>`:

```html
<!-- Google Analytics (optional) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

### Check Backend Health

Add health check endpoint (already included in `app.py`):
```bash
curl https://your-backend-url.com/api/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "Trip Planner Agent API",
  "version": "1.0.0"
}
```

---

## 🎯 Next Steps

### Enhancements

1. **Add User Accounts** - Save trips per user
2. **Social Sharing** - Share itineraries with friends
3. **PDF Export** - Generate PDF itineraries
4. **Multi-language** - Support multiple languages
5. **Mobile App** - Create React Native version
6. **Payment Integration** - Add booking capabilities

### Scaling

1. **Database** - Add PostgreSQL for storing trips
2. **Caching** - Add Redis for faster responses
3. **CDN** - Use Cloudflare for global delivery
4. **Load Balancer** - Handle more traffic

---

## 💡 Tips for Production

### Security

1. **Never commit** `.env` file or API keys
2. **Use HTTPS** (automatic on Railway/Render/Vercel)
3. **Restrict CORS** to your frontend domain only
4. **Rate limit** API endpoints to prevent abuse

### Performance

1. **Minify** CSS/JS files for production
2. **Enable caching** for static assets
3. **Use CDN** for images and assets
4. **Compress** API responses (gzip)

### Cost Optimization

1. **Monitor API usage** - Claude API costs money per request
2. **Cache results** - Same request = same itinerary
3. **Set limits** - Max requests per user per day
4. **Use free tiers** - Railway/Render/Vercel have generous free plans

---

## 📞 Support

- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Flask Docs**: https://flask.palletsprojects.com

---

**Happy Deploying! 🚀**

Your Trip Planner Agent will be live and accessible to users worldwide!
