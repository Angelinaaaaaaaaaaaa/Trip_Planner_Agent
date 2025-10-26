# 🚀 Quick Start Guide

Get your Trip Planner Agent up and running locally in 5 minutes!

## 🎯 Choose Your Path

**Option A: [Web Application](#option-a-web-application-easiest)** (Easiest - Beautiful UI, works in browser)
**Option B: [uAgents + ASI:One](#option-b-uagents--asione)** (For Fetch.ai integration)
**Option C: [Python Scripts](#option-c-python-scripts-testing)** (For testing/development)

---

# Option A: Web Application (Easiest)

The fastest way to try the Trip Planner with a beautiful web interface!

## Step 1: Install Dependencies (2 minutes)

```bash
# Make sure you're in the project directory
cd /path/to/Trip_Planner_Agent

# Install all required packages (no virtual env needed if using system Python)
pip3 install anthropic flask flask-cors python-dotenv uagents

# OR if you want to use a virtual environment:
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install anthropic flask flask-cors python-dotenv uagents
```

**What gets installed:**
- `anthropic` - Claude AI API client
- `flask` - Web server framework
- `flask-cors` - Enable cross-origin requests
- `python-dotenv` - Load environment variables
- `uagents` - Fetch.ai agent framework

## Step 2: Configure API Key (OPTIONAL - 1 minute)

**⚠️ IMPORTANT:** The API key is **OPTIONAL**!

### Without API Key (Static Database):
- ✅ Works with 6 cities: **Tokyo, Barcelona, Singapore, Paris, New York, London**
- ✅ Instant responses
- ✅ Perfect for testing
- ❌ Limited to these 6 cities

### With API Key (AI Planning):
- ✅ **ANY city in the world** (San Diego, Prague, Rome, Dubai, etc.)
- ✅ AI-researched itineraries
- ✅ Personalized recommendations
- ⏱️ Takes 5-10 seconds per request

**To enable AI planning:**

1. Get your Claude API key from https://console.anthropic.com/
2. Create `.env` file in project root:
   ```bash
   echo "ANTHROPIC_API_KEY=sk-ant-api03-your-key-here" > .env
   ```
   Replace `your-key-here` with your actual API key!

3. Or use the interactive setup:
   ```bash
   ./setup_api_key.sh
   ```

**Skip this step if you just want to try the 6 built-in cities first!**

## Step 3: Start the Web App

### Method 1: Auto Start Script (Recommended)

```bash
./start_web_app.sh
```

The script will:
- ✅ Check dependencies
- ✅ Start backend API (port 5000 or 5001)
- ✅ Start frontend web server (port 8080)
- ✅ Auto-detect available ports
- ✅ Show startup status

### Method 2: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
# From project root
python3 web_app/backend/app.py
```

You should see:
```
🚀 Starting Trip Planner Agent API Server...
⚠️  LLM Integration: DISABLED (no ANTHROPIC_API_KEY)
📍 Capability: Limited to 6 pre-configured cities
📍 API available at: http://localhost:5000

OR (if you added API key):

✅ LLM Integration: ENABLED
🌍 Capability: Can plan trips to ANY city worldwide!
```

**Terminal 2 - Frontend:**
```bash
# From project root
cd web_app/frontend/public
python3 -m http.server 8080
```

You should see:
```
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

## Step 4: Access the Web Interface

**Open your browser:** http://localhost:8080

You should see:
- 🎨 Modern dark theme web interface
- 📋 Example trip prompts (click to use them!)
- 🌍 List of supported cities
- 💬 Chat-like input box
- ⚠️ Status indicator showing AI availability

**Status Indicators:**
- **"Limited to Enhanced Cities"** = Static database (6 cities)
- **"Global AI Planning ENABLED"** = AI mode (any city)

## Step 5: Plan Your First Trip!

### Test with Built-in Cities (Works Immediately!)

Try these prompts:

```
Plan a 3-day trip to Tokyo for food and culture
Show me Paris highlights for 3 days
Barcelona for 2 days
new york
london trip
Singapore family vacation
```

**These work WITHOUT an API key!** ✅

### If You Have API Key (Any City Works!)

```
Plan a 3-day trip to San Diego
Weekend in Prague
Dubai for 5 days
Amsterdam highlights
Rome food tour
```

### What You'll See

1. ⏳ Loading spinner while processing
2. 📋 Trip details (destination, days, preferences)
3. 🗓️ Day-by-day itinerary with:
   - Activity times (09:00, 12:00, 15:00, 18:00)
   - POI names and locations
   - Google Maps links
   - Activity categories (food, culture, etc.)
4. 📅 Download Calendar button (creates .ics file)

## ✅ Verify It's Working

### Quick Test Checklist

1. **Backend running?**
   ```bash
   curl http://localhost:5000/api/health
   # or
   curl http://localhost:5001/api/health
   ```
   Expected: `{"status": "healthy", ...}`

2. **Frontend loading?**
   - Go to http://localhost:8080
   - See example prompts? ✅
   - See city list? ✅

3. **API connected?**
   - Browser console (F12) should show:
   - `✅ Backend detected on port 5001` ✅

4. **Can plan trips?**
   - Try: "Plan a 3-day trip to Tokyo"
   - Get itinerary? ✅

### Expected Behavior

**✅ Working correctly:**
- Tokyo, Paris, Barcelona → Get full itinerary
- San Diego (without API key) → Error "not supported"
- San Diego (with API key) → Get full itinerary

**❌ Something's wrong:**
- "Connection refused" → Backend not running
- "is_city_supported is not defined" → Old backend, restart it
- Nothing happens → Check browser console (F12) for errors

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

### "CORS error" in browser console

**If you see CORS errors for port 5000, this is NORMAL!**

Example error:
```
Access to fetch at 'http://localhost:5000/api/health' from origin 'http://localhost:8080'
has been blocked by CORS policy
```

**What's happening:**
- Port 5000 is often used by macOS AirPlay Receiver
- Frontend auto-detects this and switches to port 5001
- You'll see: "✅ Backend detected on port 5001"
- **This is expected behavior - everything is working!**

**Other CORS issues:**
- ✅ Backend has CORS enabled by default
- ✅ Make sure you're accessing via `http://localhost:8080` not `file://`
- ✅ If issues persist, restart both backend and frontend

### "name 'is_city_supported' is not defined" error

**This is a common error if you started the backend before installing dependencies.**

**Solution:**
```bash
# Kill all old backend processes
pkill -9 -f "python.*app.py"

# Make sure dependencies are installed
pip3 install anthropic flask flask-cors python-dotenv

# Start fresh backend from project root
cd /path/to/Trip_Planner_Agent
python3 web_app/backend/app.py
```

**Verify it's fixed:**
- Backend should start without errors
- Try planning a trip to Tokyo
- Check browser console (F12) - should NOT see this error

### "City 'San Diego' (or Prague, Rome, etc.) is not supported"

**This is CORRECT behavior if you don't have an API key configured!**

The static database only includes 6 cities:
- Tokyo, Barcelona, Singapore, Paris, New York, London

**To enable ANY city worldwide:**

1. Get API key from https://console.anthropic.com/
2. Create `.env` file in project root:
   ```bash
   echo "ANTHROPIC_API_KEY=sk-ant-api03-your-key-here" > .env
   ```
3. Restart backend:
   ```bash
   pkill -f "python.*app.py"
   python3 web_app/backend/app.py
   ```
4. You should see: "✅ LLM Integration: ENABLED"
5. Now San Diego, Prague, Rome, Dubai, etc. will all work!

## General Issues

### "Module not found" error
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip3 install anthropic flask flask-cors python-dotenv uagents
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

### Run the test suite to verify everything works

**Before reporting an issue, run the test suite:**

```bash
# Test core functionality (no API key needed)
python3 test_core_functionality.py
```

**Expected output:**
```
🎉 ALL TESTS PASSED! System is fully functional.

TOTAL: 28/28 tests passed

City Validation:      10/10 passed ✅
POI Fetching:         6/6 passed ✅
Intent Parsing:       6/6 passed ✅
Web App Examples:     6/6 passed ✅
```

**If all tests pass, your system is working correctly!**

The issue is likely with how you're using it:
- Make sure you're testing with the 6 supported cities (without API key)
- Or make sure API key is properly configured (for other cities)

## Getting Help

- 📚 Read the full [README.md](README.md)
- 🐛 Report issues on GitHub
- 💬 Join Fetch.ai Discord

---

**Built for CalHacks 12.0 | Powered by Fetch.ai & Claude AI** 🚀
