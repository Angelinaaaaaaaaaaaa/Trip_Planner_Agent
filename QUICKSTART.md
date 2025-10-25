# 🚀 Quick Start Guide

Get your Trip Planner Agent up and running in 5 minutes!

## 🎯 Choose Your Path

**Option A: [Web Application](#option-a-web-application-easiest)** (Easiest - Beautiful UI, works in browser)
**Option B: [uAgents + ASI:One](#option-b-uagents--asione)** (For Fetch.ai integration)
**Option C: [Python Scripts](#option-c-python-scripts-testing)** (For testing/development)

---

# Option A: Web Application (Easiest)

The fastest way to try the Trip Planner with a beautiful web interface!

## Step 1: Install Dependencies (2 minutes)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Key (1 minute)

1. Get your Claude API key from [https://console.anthropic.com/](https://console.anthropic.com/)

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Edit `.env` and add your key:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

## Step 3: Start the Web App (30 seconds)

**Quick Method: Use the Start Script**

```bash
./start_web_app.sh
```

The script will:
- ✅ Start the backend API server
- ✅ Start the frontend web server
- ✅ Open your browser automatically
- ✅ Auto-detect available ports

**Manual Method: Two Terminals**

Terminal 1 - Backend:
```bash
python web_app/backend/app.py
```

Terminal 2 - Frontend:
```bash
cd web_app/frontend/public
python3 -m http.server 8080
```

## Step 4: Access the Web Interface

Open your browser and go to:

**🌐 Frontend:** http://localhost:8080

You should see a beautiful web interface with:
- 🎨 Modern dark theme
- 📋 Example trip prompts
- 🌍 List of supported cities
- 💬 Chat-like interface

## Step 5: Plan Your First Trip! (30 seconds)

1. **Click an example** or type your own prompt:
   ```
   Plan a 3-day trip to Tokyo for food and culture
   ```

2. **Click "Plan My Trip"**

3. **See your itinerary** with:
   - Day-by-day schedule
   - Activity times (09:00, 12:00, etc.)
   - Google Maps links
   - Activity categories

4. **Download calendar** (optional):
   - Click "Download Calendar" button
   - Import the `.ics` file to Google Calendar or Apple Calendar

## ✨ Example Prompts to Try

```
"Plan a 2-day trip to Barcelona for architecture"
"Family trip to Singapore for 4 days, kid-friendly"
"Show me Paris highlights for 3 days"
"Tokyo nightlife and food, 2 days"
"Quick 1-day tour of London"
"Week-long New York adventure"
```

---

# Option B: uAgents + ASI:One

Run the agent with Fetch.ai's uAgents framework for ASI:One integration.

## Step 1-2: Same as Above

Follow Steps 1-2 from Option A to install dependencies and configure API key.

## Step 3: Run the uAgent (1 minute)

```bash
python agent.py
```

You should see:
```
INFO:     [trip_coordinator]: Trip Planner Agent started!
INFO:     [trip_coordinator]: Agent address: agent1q...
INFO:     [trip_coordinator]: Agent port: 8000
INFO:     [trip_coordinator]: Chat Protocol enabled
```

## Step 4: Deploy to Agentverse

1. Go to [https://agentverse.ai](https://agentverse.ai)
2. Create new agent
3. Upload your code
4. Set `ANTHROPIC_API_KEY` environment variable
5. Enable Chat Protocol
6. Publish to ASI:One

---

# Option C: Python Scripts (Testing)

Test the core functionality without the web UI or agent framework.

## Step 1-2: Same as Above

Follow Steps 1-2 from Option A.

## Step 3: Run Test Script

```bash
python test_local.py
```

You should see:
- ✅ Supported cities list
- ✅ Intent parsing examples
- ✅ Generated itinerary for Tokyo
- ✅ Calendar file created

---

# 🌟 What's Next?

## 🌐 Deploy Web App Online

Make your Trip Planner accessible to everyone on the internet!

**Recommended Platforms:**
- **[Railway](https://railway.app)** - Easiest, free tier, auto HTTPS
- **[Render](https://render.com)** - Free tier, GitHub integration
- **[Vercel](https://vercel.com)** - Great for frontend

**📚 Complete Guide:** See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) for step-by-step instructions!

## 🎨 Customize Your Trip Planner

### Add More Cities
Edit `data_sources.py` to add new destinations like Rome, Amsterdam, Dubai, etc.

### Change Colors
Edit `web_app/frontend/public/styles.css` CSS variables:
```css
:root {
    --primary-color: #6366f1;  /* Change this */
    --secondary-color: #ec4899; /* And this */
}
```

### Add Your Branding
Edit `web_app/frontend/public/index.html` header section.

## 🧪 Advanced Features

### Test Core Components
```python
# Test intent parsing
from intent import parse_intent
intent = parse_intent("Plan a 3-day trip to Tokyo for food")
print(intent)

# Test itinerary generation
from planner import build_itinerary
itinerary = build_itinerary(intent)
print(itinerary.items)
```

### Add User Analytics
Add Google Analytics to `index.html` to track usage.

### Implement User Accounts
Add Flask-Login for saving trips per user.

---

# 🛠️ Troubleshooting

## Web Application Issues

### Backend won't start
```bash
# Check if port is in use (common on macOS with AirPlay)
lsof -i :5000

# Use a different port
PORT=5001 python web_app/backend/app.py
```

### Frontend can't connect to backend
- ✅ The frontend auto-detects ports 5000, 5001, 5002
- ✅ Check browser console (F12) for connection errors
- ✅ Make sure backend is running before opening frontend

### "CORS error" in browser
- ✅ Backend has CORS enabled by default
- ✅ Make sure you're accessing via `http://localhost:8080` not `file://`

## General Issues

### "Module not found" error
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Invalid API key" error
```bash
# Check .env file exists
cat .env

# Verify it's loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key:', os.getenv('ANTHROPIC_API_KEY')[:20])"

# If still not working, make sure .env is in project root directory
pwd  # Should show /path/to/Trip_Planner_Agent
```

### Port already in use (for uAgent)
```bash
# Change port in .env
AGENT_PORT=8001
```

### Web page loads but buttons don't work
- ✅ Open browser console (F12) and check for JavaScript errors
- ✅ Make sure all three files exist: index.html, styles.css, app.js
- ✅ Verify backend is running and accessible

## Getting Help

- 📚 Read the full [README.md](README.md)
- 🐛 Report issues on GitHub
- 💬 Join Fetch.ai Discord

---

**Built for CalHacks 12.0 | Powered by Fetch.ai & Claude AI** 🚀
