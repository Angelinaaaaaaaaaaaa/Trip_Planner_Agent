# Setup Guide for Trip Planner Agent

## Prerequisites Check

Before starting, ensure you have:

```bash
# Check Python version (need 3.8+)
python --version

# Check pip
pip --version

# Check git
git --version
```

## Step-by-Step Setup

### 1. Get API Keys

#### Anthropic Claude API Key (Required)
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and save it securely

#### OpenWeatherMap API Key (Optional)
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to API keys
4. Copy your default API key

### 2. Install Dependencies

```bash
# Navigate to project directory
cd Trip_Planner_Agent

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file and add your API keys
# Use your preferred text editor:
notepad .env     # Windows
nano .env        # macOS/Linux
code .env        # VSCode
```

Add your keys:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
OPENWEATHER_API_KEY=xxxxxxxxxxxxxx  # Optional
AGENT_SEED_PHRASE=my_unique_seed_phrase_123
```

### 4. Verify Installation

```bash
# Test imports
python -c "import uagents; import anthropic; print('All imports successful!')"
```

### 5. Run Your First Agent

```bash
# Start single agent
python run_single_agent.py
```

You should see:
```
============================================================
🌍 Trip Planner Agent - Single Instance
============================================================

Agent Name: TripCoordinator
Agent Address: agent1q...
Endpoint: http://localhost:8001/submit

This agent is ready for Agentverse registration!
============================================================
```

### 6. Run Full System

In a new terminal:
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run all agents
python main.py
```

## Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Error: "ANTHROPIC_API_KEY not found"
- Make sure `.env` file exists in project root
- Check that the key starts with `sk-ant-`
- Ensure no spaces around the `=` sign

### Error: "Port already in use"
```bash
# Kill processes using the ports (Windows)
netstat -ano | findstr :8001
taskkill /PID <process_id> /F

# Kill processes using the ports (macOS/Linux)
lsof -ti:8001 | xargs kill -9
```

### Error: "anthropic module error"
```bash
pip uninstall anthropic
pip install anthropic>=0.39.0
```

## Verifying Everything Works

1. **Check agents are running**: You should see startup messages for each agent
2. **Check addresses are printed**: Each agent will print its address
3. **No error messages**: Look for any red error text

## Next Steps

- Read the main [README.md](README.md) for usage examples
- See [DEPLOYMENT.md](DEPLOYMENT.md) for Agentverse deployment
- Try the example queries in the README

## Getting Help

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review Fetch.ai docs: https://fetch.ai/docs
3. Review uAgents docs: https://uagents.fetch.ai/docs
4. Check Anthropic docs: https://docs.anthropic.com

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] API keys configured in `.env`
- [ ] Single agent runs successfully
- [ ] Agent address is displayed
- [ ] No error messages in console

You're ready to start using Trip Planner Agent! 🎉
