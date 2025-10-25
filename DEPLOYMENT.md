# 🌐 Agentverse Deployment Guide

Complete guide to deploying your Trip Planner Agent to Agentverse and making it discoverable via ASI:One.

## Prerequisites

- ✅ Completed local setup and testing
- ✅ Anthropic Claude API key
- ✅ Fetch.ai account on Agentverse

## Step-by-Step Deployment

### 1. Prepare Your Code

**Verify everything works locally:**
```bash
# Test the agent
python test_local.py

# Make sure all tests pass
```

**Create a clean repository:**
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Trip Planner Agent for CalHacks 12.0"

# Push to GitHub (optional but recommended)
git remote add origin https://github.com/yourusername/Trip_Planner_Agent.git
git push -u origin main
```

### 2. Register on Agentverse

1. **Go to Agentverse**
   - Navigate to [https://agentverse.ai](https://agentverse.ai)
   - Sign in with your Fetch.ai wallet

2. **Create New Agent**
   - Click **"Create Agent"** or **"New Agent"**
   - Choose **"Code Agent"** (not drag-and-drop)

### 3. Configure Agent Settings

**Basic Information:**

```yaml
Name: trip_planner_agent
Display Name: Trip Planner
Description: |
  AI-powered trip planning assistant using Claude AI.
  Provides personalized travel recommendations, detailed
  day-by-day itineraries, and smart scheduling for popular
  destinations worldwide. Supports Tokyo, Barcelona, Singapore,
  Paris, New York, and London.

Agent Type: Service Agent
Category: Travel & Tourism
```

**Agent Configuration:**

```yaml
Runtime: Python 3.10+
Entry Point: agent.py
Port: 8000
```

### 4. Upload Code

**Option A: Upload Files**
1. Zip your project (exclude `.venv/`, `.git/`, `*.ics`)
2. Upload via Agentverse UI
3. Agentverse will extract and install dependencies

**Option B: GitHub Integration**
1. Connect your GitHub account in Agentverse
2. Select your repository
3. Choose branch (usually `main`)
4. Agentverse will auto-deploy on commits

### 5. Set Environment Variables

In Agentverse agent settings, add:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here

# Optional (defaults are fine)
AGENT_SEED=trip_planner_production_2024
AGENT_NAME=trip_coordinator
AGENT_PORT=8000
```

⚠️ **Security Note**: Never commit `.env` file to Git!

### 6. Enable Chat Protocol

This is crucial for ASI:One discoverability!

1. **Go to Protocols Tab**
   - In your agent settings, find "Protocols"
   - Click **"Enable Chat Protocol"**

2. **Configure Discovery Metadata:**

```yaml
Protocol: Chat
Enabled: Yes

Discovery Settings:
  Title: "Trip Planner"

  Short Description: "Plan your perfect trip with AI"

  Full Description: |
    Plan personalized trips with AI-powered recommendations!
    Just tell me:
    - Where you want to go
    - How many days
    - Your interests (food, culture, architecture, etc.)

    I'll create a detailed day-by-day itinerary with:
    ✓ Smart activity scheduling
    ✓ Geographic clustering (minimize travel)
    ✓ Opening hours optimization
    ✓ Google Maps links for each spot
    ✓ Calendar export (.ics file)

  Keywords: |
    travel, trip planning, itinerary, vacation planning,
    tourism, travel agent, ai travel, trip advisor,
    travel recommendations, vacation planner

  Example Prompts:
    - "Plan a 3-day trip to Tokyo for food and culture"
    - "I want to visit Barcelona for 2 days, architecture focus"
    - "Family trip to Singapore, kid-friendly, 4 days"
```

### 7. Test on Agentverse

1. **Use Built-in Test Console**
   - Go to "Test" tab in Agentverse
   - Send test message: `"Plan a 3-day trip to Tokyo"`
   - Verify response looks correct

2. **Check Logs**
   - Go to "Logs" tab
   - Look for startup messages
   - Verify no errors

3. **Test Chat Protocol**
   - Use "Test Chat" feature
   - Ensure proper acknowledgements

### 8. Publish to ASI:One

1. **Click "Publish"**
   - In Agentverse, click the **"Publish"** button
   - Confirm you want to make it discoverable

2. **Get Your Agent Address**
   - Copy your agent address (e.g., `agent1q2w3e4r5t6y7u8i9o0p...`)
   - Save it for your documentation

3. **Verify on ASI:One**
   - Go to ASI:One interface
   - Search for "trip planner" or your agent name
   - Your agent should appear in results!

### 9. Monitor and Maintain

**Check Agent Health:**
```bash
# In Agentverse dashboard
- Status: Should show "Running" (green)
- Uptime: Should be 99%+
- Response time: Should be < 2s
```

**Monitor Logs:**
- Check for errors regularly
- Look for failed requests
- Monitor API usage (Claude credits)

**Update Agent:**
```bash
# If using GitHub integration
git commit -am "Update feature"
git push

# Agentverse will auto-deploy
```

## Troubleshooting Deployment

### Agent Won't Start

**Check logs for errors:**
- Missing environment variable
- Invalid API key
- Port conflict
- Import errors

**Solution:**
```bash
# Verify requirements.txt is complete
# Check ANTHROPIC_API_KEY is set correctly
# Try running locally first to debug
```

### Chat Protocol Not Working

**Symptoms:**
- Agent not discoverable in ASI:One
- Messages not being received

**Solutions:**
1. Verify Chat Protocol is enabled in settings
2. Check `chat_proto` is included: `agent.include(chat_proto, publish_manifest=True)`
3. Restart agent after changes
4. Check manifest is published (look for log message)

### API Rate Limits

**Claude API limits:**
- Free tier: Limited requests/month
- Paid tier: Higher limits

**Solutions:**
1. Monitor usage in Anthropic console
2. Implement caching (future enhancement)
3. Add fallback to rule-based parsing

### Performance Issues

**If responses are slow:**

1. **Check Claude API latency**
   - Test locally first
   - Claude typically responds in 1-2s

2. **Optimize code**
   - Cache frequently requested cities
   - Pre-compute popular itineraries

3. **Monitor Agentverse resources**
   - Check CPU/memory usage
   - Upgrade plan if needed

## Production Checklist

Before going live:

- [ ] All tests pass locally
- [ ] Environment variables set correctly
- [ ] Chat Protocol enabled and tested
- [ ] Agent published to ASI:One
- [ ] Discovery metadata optimized
- [ ] Example prompts work correctly
- [ ] Error handling tested
- [ ] Logging configured
- [ ] API usage monitored
- [ ] Documentation updated with agent address

## Post-Deployment

### Share Your Agent

**Agent Address:**
```
agent1q... (your actual address from Agentverse)
```

**ASI:One Link:**
```
https://agentverse.ai/agents/agent1q...
```

**Demo Prompts:**
```
1. "Plan a 3-day trip to Tokyo for food and culture"
2. "I'll be in Barcelona for 2 days, architecture focus"
3. "Family vacation in Singapore, 4 days, kid-friendly"
```

### Promote Your Agent

1. **Update README** with live agent address
2. **Create demo video** showing it in action
3. **Share on social media** with hashtags:
   - #CalHacks12
   - #FetchAI
   - #ClaudeAI
   - #AIAgents

### Get Feedback

1. Monitor user interactions in logs
2. Track popular queries
3. Identify missing cities/features
4. Iterate and improve!

## Support Resources

- **Agentverse Docs**: [https://docs.fetch.ai/](https://docs.fetch.ai/)
- **uAgents Guide**: [https://fetch.ai/docs/guides/agents](https://fetch.ai/docs/guides/agents)
- **Discord**: [Fetch.ai Discord Community](https://discord.gg/fetchai)
- **GitHub Issues**: Report bugs in your repo

## Next Steps

After successful deployment:

1. **Add More Cities** - Expand to 20+ destinations
2. **Real APIs** - Integrate Google Places, weather data
3. **User Accounts** - Save preferences and past trips
4. **Multi-language** - Support Spanish, French, Japanese
5. **Mobile App** - Build native iOS/Android apps

---

**Congratulations!** 🎉 Your Trip Planner Agent is now live on Agentverse and discoverable via ASI:One!

Built for CalHacks 12.0 | Powered by Fetch.ai & Claude AI
