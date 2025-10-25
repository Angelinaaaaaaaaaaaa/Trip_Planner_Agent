# 🚀 Quick Start Guide

Get your Trip Planner Agent up and running in 5 minutes!

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

## Step 3: Test Locally (1 minute)

```bash
python test_local.py
```

You should see:
- ✅ Supported cities list
- ✅ Intent parsing examples
- ✅ Generated itinerary for Tokyo
- ✅ Calendar file created

## Step 4: Run the Agent (1 minute)

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

## What's Next?

### 🌐 Deploy to Agentverse

1. Go to [https://agentverse.ai](https://agentverse.ai)
2. Create new agent
3. Upload your code
4. Set `ANTHROPIC_API_KEY` environment variable
5. Enable Chat Protocol
6. Publish to ASI:One

### 🧪 Test More Features

Try different prompts:
```python
# Different cities
"Plan a 2-day trip to Barcelona for architecture"
"Show me Paris highlights for 4 days"

# Different preferences
"Family-friendly Singapore for 3 days"
"Tokyo nightlife and food, 2 days"

# Various durations
"Quick 1-day tour of London"
"Week-long New York adventure"
```

### 📅 Import Calendar

The agent creates `.ics` files you can import:
1. Open Google Calendar
2. Click Settings → Import & Export
3. Import the `.ics` file
4. See your trip schedule!

## Troubleshooting

### "Module not found" error
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
```

### "Invalid API key" error
```bash
# Check .env file
cat .env

# Verify it's loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key:', os.getenv('ANTHROPIC_API_KEY')[:20])"
```

### Port already in use
```bash
# Change port in .env
AGENT_PORT=8001
```

## Getting Help

- 📚 Read the full [README.md](README.md)
- 🐛 Report issues on GitHub
- 💬 Join Fetch.ai Discord

---

**Built for CalHacks 12.0 | Powered by Fetch.ai & Claude AI** 🚀
