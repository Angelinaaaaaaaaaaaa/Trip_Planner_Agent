# Model Context Protocol (MCP) Setup Guide

## 🎯 What is MCP?

**Model Context Protocol (MCP)** is Anthropic's open standard that enables secure, two-way connections between AI systems and external data sources. For Trip Planner Agent, MCP enables:

- 📝 **Save trip plans to Notion** - Automatically create beautifully formatted Notion pages
- 📅 **Export to calendars** - Generate iCal files for your itineraries
- 📄 **Create PDF documents** - Professional trip plan PDFs
- 🔗 **Share trip plans** - Generate shareable links

## ⭐ Why This Makes Your Hackathon Submission Better

Adding MCP integration demonstrates:
1. **Cutting-edge technology** - Using Anthropic's newest protocol (2024-2025)
2. **Real-world utility** - Actual data persistence and sharing
3. **Production readiness** - Integration with popular tools (Notion)
4. **Advanced integration** - Beyond basic LLM usage
5. **Ecosystem adoption** - Following industry standards

## 🚀 Quick Setup (Notion Integration)

### Step 1: Create Notion Integration

1. Go to https://www.notion.so/profile/integrations
2. Click **"+ New integration"**
3. Name it: `Trip Planner Agent`
4. Select your workspace
5. Click **"Submit"**
6. Copy the **Integration Token** (starts with `secret_`)

### Step 2: Create Notion Database

1. Create a new Notion page for your trips
2. Create a database with these properties:
   - **Title** (Title)
   - **Destination** (Text)
   - **Duration** (Number)
   - **Start Date** (Date)
   - **End Date** (Date)
   - **Status** (Select: Planning, Confirmed, In Progress, Completed)
   - **Budget** (Number)
   - **Trip Type** (Select: Business, Leisure, Adventure, Family, Solo)

3. Click the **"..."** menu → **"Copy link to view"**
4. Extract the database ID from the URL:
   ```
   https://notion.so/workspace/[DATABASE_ID]?v=...
                              ^^^^^^^^^^^^^^^^
   ```

### Step 3: Share Database with Integration

1. Click **"Share"** on your database
2. Click **"Invite"**
3. Select your **Trip Planner Agent** integration
4. Click **"Invite"**

### Step 4: Configure Environment

Add to your `.env` file:

```env
# MCP - Notion Integration
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
MCP_ENABLED=true
MCP_NOTION_ENABLED=true
```

### Step 5: Install MCP Notion Server (Optional)

For full MCP functionality with Claude Desktop:

```bash
# Using npm
npm install -g @makenotion/notion-mcp-server

# Or using npx (no installation needed)
# The system will use npx automatically
```

### Step 6: Test Integration

```python
from utils.mcp_integration import get_notion_integration

# Create integration instance
notion = get_notion_integration()

# Test saving a trip plan
result = await notion.save_trip_plan_to_notion({
    "destination": "Tokyo, Japan",
    "duration": 7,
    "start_date": "2025-11-15",
    "budget": 3000,
    "preferences": {
        "budget": "moderate",
        "interests": ["culture", "food", "technology"]
    }
})

print(result)
```

## 📋 MCP Configuration File

The `mcp_config.json` file controls MCP features:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@makenotion/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "${NOTION_API_KEY}"
      },
      "enabled": true
    }
  }
}
```

## 🔧 Advanced Configuration

### Claude Desktop Integration

To use MCP with Claude Desktop app:

1. **Locate Claude config file**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add MCP server configuration**:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@makenotion/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "secret_your_key_here"
      }
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Test**: Ask Claude to "Save this to Notion"

### Using MCP in Trip Coordinator Agent

Update `agents/trip_coordinator.py` to include MCP functionality:

```python
from utils.mcp_integration import get_notion_integration, get_mcp_tool_registry

# In your message handler
notion = get_notion_integration()

if "save to notion" in message.lower():
    # Save current trip plan to Notion
    result = await notion.save_trip_plan_to_notion(trip_plan)

    if result["success"]:
        response = f"✅ Trip plan saved to Notion! {result.get('notion_url', '')}"
    else:
        response = f"⚠️ {result.get('message', 'Could not save to Notion')}"
```

## 🎨 Notion Page Template

When you save a trip plan, it creates a beautifully formatted Notion page:

```
📍 Trip to Tokyo, Japan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🗓️ Duration: 7 days
📅 Start Date: Nov 15, 2025
💰 Budget: $3,000
👥 Travelers: 2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Trip Overview

## Preferences
• Budget: Moderate
• Interests: Culture, Food, Technology
• Travel Style: Balanced

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Itinerary

## Day 1: Arrival & Shibuya Exploration
Morning: ...
Afternoon: ...
Evening: ...

## Day 2: Traditional Tokyo
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Budget Breakdown
[Detailed budget analysis]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Local Insights & Tips
[Cultural tips, customs, practical advice]
```

## 🛠️ Available MCP Tools

The Trip Planner Agent supports these MCP tools:

### 1. save_to_notion
Save complete trip plan to Notion workspace

**Usage:**
```
User: Save this trip plan to Notion
Agent: ✅ Trip plan saved to Notion! You can view it at [link]
```

### 2. export_to_calendar
Export itinerary to iCal format for Google Calendar, Apple Calendar, etc.

**Usage:**
```
User: Export this itinerary to my calendar
Agent: ✅ Calendar file ready for download: tokyo_trip.ics
```

### 3. create_pdf
Generate professional PDF document of trip plan

**Usage:**
```
User: Create a PDF of my trip plan
Agent: ✅ PDF generated: trip_plan_tokyo_2025.pdf
```

### 4. share_trip
Generate shareable link for trip plan

**Usage:**
```
User: Create a shareable link for this trip
Agent: ✅ Share your trip: https://tripplanner.ai/share/abc123
```

## 🔐 Security Best Practices

1. **Never commit API keys** - Use `.env` file (already in `.gitignore`)
2. **Read-only access** - For demo, use read-only Notion integration
3. **Scope permissions** - Only grant access to specific Notion pages
4. **Rotate keys** - Change API keys after hackathon demo
5. **Environment separation** - Use different keys for dev/prod

## 🧪 Testing MCP Integration

### Test Script

Create `test_mcp.py`:

```python
import asyncio
from utils.mcp_integration import get_notion_integration

async def test_notion():
    notion = get_notion_integration()

    # Sample trip plan
    trip_plan = {
        "destination": "Paris, France",
        "duration": 5,
        "start_date": "2025-12-01",
        "budget": 2500,
        "preferences": {
            "budget": "moderate",
            "interests": ["art", "food", "history"]
        },
        "itinerary": {
            "days": [
                {
                    "day_number": 1,
                    "theme": "Arrival & Eiffel Tower",
                    "morning": "Arrive at CDG, check into hotel",
                    "afternoon": "Visit Eiffel Tower",
                    "evening": "Seine River cruise"
                }
            ]
        }
    }

    result = await notion.save_trip_plan_to_notion(trip_plan)
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test_notion())
```

Run test:
```bash
python test_mcp.py
```

## 📊 Hackathon Demo Tips

### In Your Demo Video

1. **Show MCP in action** (30 seconds):
   - "Watch as I save this trip plan to Notion..."
   - Show the command
   - Show the Notion page being created in real-time

2. **Highlight innovation** (15 seconds):
   - "Using Anthropic's Model Context Protocol..."
   - "Industry-standard integration..."
   - "Production-ready data persistence..."

3. **Show the Notion page** (15 seconds):
   - Beautiful formatting
   - All trip details preserved
   - Easy to share and collaborate

### Talking Points

- "We're using Anthropic's **Model Context Protocol**, the latest standard for AI tool integration"
- "Trip plans are automatically saved to Notion with beautiful formatting"
- "This demonstrates **real-world utility** beyond just conversation"
- "MCP support means easy integration with other tools in the future"

## 🚀 Production Deployment

For production use:

1. **Use Notion's hosted MCP server** (recommended)
2. **Set up proper authentication**
3. **Implement rate limiting**
4. **Add error logging**
5. **Monitor API usage**

## 📚 Additional Resources

- **MCP Documentation**: https://docs.anthropic.com/en/docs/agents-and-tools/mcp
- **Notion MCP Server**: https://github.com/makenotion/notion-mcp-server
- **Notion API Docs**: https://developers.notion.com/
- **MCP GitHub**: https://github.com/modelcontextprotocol

## 🎯 Why This Wins

**Before MCP**: "Our agent can plan trips and have conversations"

**After MCP**: "Our agent can plan trips, save them to Notion for collaboration, export to calendars, generate PDFs, and use cutting-edge MCP protocol for future integrations"

The MCP integration shows:
- ✅ Advanced technical skills
- ✅ Following industry standards
- ✅ Production-ready thinking
- ✅ Real-world utility
- ✅ Future-proof architecture

## 💡 Quick Win for Hackathon

**Minimum viable MCP demo:**

1. Configure Notion API key (5 min)
2. Update `.env` file (1 min)
3. Show formatted trip plan structure (already done!)
4. In demo video, show "MCP-ready" badge (1 min)

**Even without full MCP setup**, showing the code and architecture demonstrates:
- Knowledge of cutting-edge technology
- Production-ready thinking
- Extensible architecture

## ⚡ Fast Track (No Notion Setup)

If you don't have time to set up Notion:

1. The MCP integration code is already there
2. It gracefully handles missing API keys
3. Show the formatted Notion page structure in demo
4. Mention: "MCP-ready for production deployment"

This still demonstrates advanced integration capabilities!

---

**MCP = Hackathon Advantage** 🏆

Adding MCP support takes your submission from "good chatbot" to "production-ready AI system with real-world integrations."
