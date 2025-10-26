# 🤖 Enable AI Planning for ANY City

## What This Does

With AI planning enabled, you can plan trips to **ANY city in the world**:
- ✅ San Diego
- ✅ Prague
- ✅ Rome
- ✅ Dubai
- ✅ Amsterdam
- ✅ Literally any city!

The AI will research the city and create a custom itinerary on the fly.

---

## Step 1: Get Your Claude API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Click "API Keys" in the left menu
4. Click "Create Key"
5. Copy your API key (it starts with `sk-ant-api03-...`)

**Important:** Keep this key secret! Don't share it or commit it to git.

---

## Step 2: Create .env File

In the project root directory (where you see `agent.py`, `planner.py`, etc.), create a file named `.env`:

```bash
# Method 1: Using terminal
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Method 2: Using text editor
nano .env
# Then type: ANTHROPIC_API_KEY=your-key-here
# Save: Ctrl+X, Y, Enter
```

**Replace `your-key-here` with your actual API key!**

Example `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Step 3: Restart the Backend

The backend needs to restart to load the new API key:

```bash
# Kill the old backend
pkill -f "python.*app.py"

# Start the new backend
python3 web_app/backend/app.py
```

You should see:
```
🚀 Starting Trip Planner Agent API Server...
✅ LLM Integration: ENABLED
🌍 Capability: Can plan trips to ANY city worldwide!
📍 API available at: http://localhost:5000
```

**Look for "LLM Integration: ENABLED" - that's the key!**

---

## Step 4: Test with San Diego

Now refresh your web browser and try:

```
Plan a 3-day trip to San Diego
```

You should get a full itinerary with:
- ✅ Real San Diego attractions
- ✅ Neighborhoods (Gaslamp Quarter, La Jolla, etc.)
- ✅ Activities (beaches, zoo, museums)
- ✅ Restaurants and local spots

**This will take 5-10 seconds** as the AI researches San Diego and creates your itinerary.

---

## Step 5: Try Other Cities!

Now you can try ANY city:

```
Weekend in Prague
Dubai for 5 days
Amsterdam highlights
Rome food tour
Tokyo off the beaten path
```

All of these will work! 🎉

---

## Troubleshooting

### "LLM Integration: DISABLED" after restart

**Check:**
1. `.env` file is in the project root (same folder as `agent.py`)
2. File is named exactly `.env` (not `.env.txt`)
3. API key format is correct: `ANTHROPIC_API_KEY=sk-ant-api03-...`
4. No spaces around the `=`

**Verify:**
```bash
# Check if .env exists
cat .env

# Should show: ANTHROPIC_API_KEY=sk-ant-api03-...

# Test if Python can read it
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Key found:', bool(os.getenv('ANTHROPIC_API_KEY')))"
```

### "Invalid API key" error

- Double-check your API key is correct
- Make sure you copied the entire key
- Check you have credits/quota available at https://console.anthropic.com/

### Still using static database

- Make sure you restarted the backend AFTER creating .env
- Check backend startup message says "LLM Integration: ENABLED"
- If not, the .env file isn't being loaded

---

## How It Works

### Without API Key (Current):
```
You: "Plan trip to San Diego"
Backend: Checks static database
Backend: "San Diego not found"
Backend: Returns error ❌
```

### With API Key (After Setup):
```
You: "Plan trip to San Diego"
Backend: Checks static database
Backend: "San Diego not found, using AI"
Backend: Calls Claude API
Claude: Researches San Diego
Claude: Generates custom itinerary
Backend: Returns personalized plan ✅
```

---

## Cost Information

Claude API pricing (as of 2024):
- Model: `claude-3-haiku-20240307` (fast and cheap)
- Cost: ~$0.01-0.02 per trip itinerary
- Very affordable for personal use!

For 100 trip plans = ~$1-2 in API costs.

---

## Security

The `.env` file is already in `.gitignore`, so your API key won't be committed to git. ✅

Never share your API key or commit it to public repositories!

---

## Quick Reference

**Enable AI:**
```bash
echo "ANTHROPIC_API_KEY=your-key-here" > .env
pkill -f "python.*app.py"
python3 web_app/backend/app.py
```

**Disable AI:**
```bash
rm .env
pkill -f "python.*app.py"
python3 web_app/backend/app.py
```

**Check Status:**
```bash
# Backend should show one of these:
# ✅ LLM Integration: ENABLED   (AI on)
# ⚠️  LLM Integration: DISABLED  (AI off)
```

---

## What You Get

### Static Database (No API Key):
- ✅ 6 cities: Tokyo, Barcelona, Singapore, Paris, New York, London
- ✅ Pre-curated POIs
- ✅ Instant response
- ❌ Limited to these 6 cities

### AI Planning (With API Key):
- ✅ **ANY city worldwide**
- ✅ AI-researched POIs
- ✅ Personalized recommendations
- ✅ Up-to-date information
- ⏱️ Takes 5-10 seconds per request

---

## Ready to Enable?

1. Get API key: https://console.anthropic.com/
2. Create `.env`: `echo "ANTHROPIC_API_KEY=your-key" > .env`
3. Restart backend: `pkill -f app.py && python3 web_app/backend/app.py`
4. Try San Diego! 🏖️

---

**You're about to unlock trip planning for ANY city in the world!** 🌍✨
