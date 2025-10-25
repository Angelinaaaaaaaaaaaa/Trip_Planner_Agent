# Agentverse Deployment Guide

This guide walks you through deploying your Trip Planner Agent to Fetch.ai's Agentverse platform.

## Prerequisites

- [ ] Trip Planner Agent running locally without errors
- [ ] Fetch.ai account (create at https://agentverse.ai/)
- [ ] Agent address from local testing
- [ ] This GitHub repository URL

## Deployment Options

### Option 1: Local Agent with Agentverse Registration (Recommended for Hackathon)

This keeps your agent running locally but makes it discoverable on Agentverse.

#### Step 1: Get Your Agent Address

```bash
python run_single_agent.py
```

Copy the agent address shown (starts with `agent1q...`)

#### Step 2: Register on Agentverse

1. Go to https://agentverse.ai/
2. Log in or create account
3. Click "Create Agent" or "My Agents" → "New Agent"

#### Step 3: Configure Agent Details

**Basic Information:**
- **Name**: `TripCoordinator`
- **Description**:
  ```
  Intelligent AI travel assistant powered by Claude that helps users plan personalized vacations.
  Provides destination recommendations, detailed itineraries, budget optimization, weather
  insights, and cultural tips through natural conversation.
  ```
- **Agent Type**: Local Agent
- **Agent Address**: Paste your agent address from Step 1

**Function Configuration:**
- **Function Name**: `trip_planning`
- **Function Description**:
  ```
  Plan your perfect trip with AI-powered personalization. Get destination recommendations
  based on your budget and interests, create detailed day-by-day itineraries, optimize
  your travel budget, and receive local insights and cultural tips.
  ```

**Keywords** (important for discovery):
```
travel, trip planning, vacation, itinerary, destination, budget, tourism,
adventure, recommendations, planning assistant
```

**Field Descriptions for DeltaV:**

1. **Destination Preferences**
   - Type: Text
   - Description: "Tell me about your travel preferences (budget, interests, duration, travel style)"
   - Required: No

2. **Destination**
   - Type: Text
   - Description: "Which destination are you interested in?"
   - Required: No

3. **Trip Duration**
   - Type: Number
   - Description: "How many days is your trip?"
   - Required: No

#### Step 4: Enable Chat Protocol

- Toggle "Enable Chat Protocol": **ON** ✓
- This is crucial for conversational interaction

#### Step 5: Set Endpoint

- **Endpoint URL**: `http://localhost:8001/submit`
- Or if using ngrok: `https://your-ngrok-url.ngrok.io/submit`

#### Step 6: Test in DeltaV

1. Click "Test in DeltaV" button
2. Try queries like:
   - "I want to plan a 7-day trip to Japan"
   - "Recommend a beach destination for a couple on moderate budget"
   - "Create an itinerary for 5 days in Paris"

### Option 2: Hosted Agent on Agentverse

For full cloud deployment:

#### Step 1: Prepare Code for Upload

Create a single-file version combining all agents:

```bash
# Your main agent file should be self-contained
# Use run_single_agent.py as the base
```

#### Step 2: Upload to Agentverse

1. In Agentverse, select "Hosted Agent"
2. Upload your `run_single_agent.py`
3. Upload `utils/` folder
4. Add dependencies from `requirements.txt`

#### Step 3: Configure Environment Variables

In Agentverse settings, add:
```
ANTHROPIC_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
```

#### Step 4: Deploy and Test

1. Click "Deploy"
2. Wait for agent to start
3. Test in DeltaV

## Making Your Agent Discoverable

### Optimize for DeltaV Search

Your agent's discoverability depends on:

1. **Good Description**: Clear, keyword-rich description
2. **Relevant Keywords**: Include all related terms
3. **Function Details**: Well-defined function parameters
4. **Testing**: Regular testing improves ranking

### Recommended Description Template

```
I'm an AI-powered trip planning assistant that helps you create perfect vacations!

✨ What I can do:
• Recommend destinations based on your budget, interests, and travel style
• Create detailed day-by-day itineraries with activities and restaurants
• Optimize your travel budget and find cost-saving opportunities
• Provide weather forecasts and local cultural insights
• Answer travel questions and give practical tips

🌟 Powered by Claude AI for intelligent, personalized recommendations

Just tell me what kind of trip you're dreaming about!
```

## Exposing Local Agent to Internet (Development)

### Using ngrok

```bash
# Install ngrok
# Download from https://ngrok.com/

# Expose your local agent
ngrok http 8001

# Copy the https URL (e.g., https://abc123.ngrok.io)
# Use this as your endpoint in Agentverse
```

### Using localtunnel

```bash
# Install localtunnel
npm install -g localtunnel

# Expose port 8001
lt --port 8001

# Use the provided URL as your endpoint
```

## Monitoring Your Agent

### View Agent Activity

In Agentverse dashboard:
1. Go to "My Agents"
2. Click on your agent
3. View "Activity" tab for:
   - Request logs
   - Error messages
   - Usage statistics

### Check Agent Health

```bash
# Locally, monitor console output
python run_single_agent.py

# Watch for:
# - Startup messages
# - Incoming requests
# - Claude API calls
# - Errors or warnings
```

## Updating Your Agent

### Update Local Agent

```bash
# Make changes to code
git add .
git commit -m "Update agent features"

# Restart agent
python run_single_agent.py
```

### Update Agentverse Registration

1. Go to agent settings in Agentverse
2. Update description, keywords, or configuration
3. Click "Save"
4. Changes take effect immediately

## Troubleshooting Deployment

### Agent Not Appearing in DeltaV

- Check chat protocol is enabled
- Verify agent is running and accessible
- Ensure description has good keywords
- Try more specific search terms

### Connection Errors

- Verify endpoint URL is correct and accessible
- Check firewall settings allow incoming connections
- If using ngrok/localtunnel, ensure tunnel is active
- Test endpoint with curl:
  ```bash
  curl -X POST http://localhost:8001/submit
  ```

### Authentication Errors

- Verify ANTHROPIC_API_KEY is set correctly
- Check API key has sufficient credits
- Test API key locally first

## Production Checklist

Before final submission:

- [ ] Agent runs without errors
- [ ] Chat protocol enabled and tested
- [ ] Agent registered on Agentverse
- [ ] Tested in DeltaV successfully
- [ ] GitHub repository is public
- [ ] README has agent addresses
- [ ] Demo video recorded
- [ ] All documentation complete

## Agent Information for Submission

After deployment, update these in your README:

```markdown
## 🤖 Agent Addresses

- **Trip Coordinator**: agent1q[your_address]
- **Agentverse Profile**: https://agentverse.ai/agents/[your_agent_id]
- **DeltaV Function**: trip_planning
```

## Support Resources

- **Agentverse Docs**: https://fetch.ai/docs/concepts/agent-services/agentverse-intro
- **Function Registration**: https://fetch.ai/docs/guides/agentverse/agentverse-functions/registering-agent-services
- **DeltaV Integration**: https://fetch.ai/docs/guides/agentverse/agentverse-functions/field-descriptions-for-deltav
- **Fetch.ai Discord**: Join for real-time help

## Success Criteria

Your agent is successfully deployed when:

✅ Agent appears in Agentverse dashboard
✅ Agent can be found in DeltaV search
✅ Test conversations work end-to-end
✅ Claude AI responses are generated
✅ No errors in agent logs
✅ Agent address is documented

Congratulations! Your Trip Planner Agent is live! 🎉
