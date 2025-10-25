# 🌐 Trip Planner Web Application

A beautiful, user-friendly web interface for the AI Trip Planner Agent.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# From the project root directory
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
# From the project root directory
python web_app/backend/app.py
```

Backend will run on: `http://localhost:5000`

### 3. Start the Frontend

**Option A: Simple Python Server**
```bash
cd web_app/frontend/public
python3 -m http.server 8080
```

**Option B: Open Directly in Browser**
```bash
# macOS
open web_app/frontend/public/index.html

# Linux
xdg-open web_app/frontend/public/index.html

# Windows
start web_app/frontend/public/index.html
```

**Option C: Using Node.js http-server**
```bash
cd web_app/frontend/public
npx http-server -p 8080
```

### 4. Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000/api/health

## 📁 Structure

```
web_app/
├── backend/
│   └── app.py              # Flask REST API server
└── frontend/
    └── public/
        ├── index.html      # Main HTML page
        ├── styles.css      # Styling
        └── app.js          # Frontend JavaScript logic
```

## 🎨 Features

- **Beautiful Dark Theme UI** - Modern, responsive design
- **Example Prompts** - Click to try pre-made trip ideas
- **Supported Cities Display** - See all available destinations
- **Real-time Planning** - Watch your itinerary generate
- **Calendar Export** - Download .ics files for your calendar
- **Mobile Responsive** - Works on all devices
- **Error Handling** - Clear error messages and validation

## 🔌 API Endpoints

### GET /api/health
Health check endpoint
```bash
curl http://localhost:5000/api/health
```

### GET /api/cities
Get list of supported cities
```bash
curl http://localhost:5000/api/cities
```

### POST /api/plan
Plan a trip
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan a 3-day trip to Tokyo for food and culture"}'
```

### GET /api/download/:id
Download calendar file for an itinerary
```bash
curl http://localhost:5000/api/download/YOUR-ITINERARY-ID \
  --output trip.ics
```

### GET /api/examples
Get example prompts
```bash
curl http://localhost:5000/api/examples
```

## 🌍 Deployment

See [WEB_DEPLOYMENT.md](../WEB_DEPLOYMENT.md) for comprehensive deployment guides:

- **Railway** (Recommended - Free tier, easiest)
- **Render** (Free tier, auto-deploy)
- **Vercel** (Frontend only, very fast)
- **Heroku** (Classic option)

## 🛠️ Development

### Update API URL for Production

When deploying, update `frontend/public/app.js` line 2:

```javascript
// Development
const API_BASE_URL = 'http://localhost:5000/api';

// Production
const API_BASE_URL = 'https://your-backend-url.com/api';
```

### Enable CORS for Specific Origins

In `backend/app.py`, restrict CORS to your frontend:

```python
# Allow all origins (development)
CORS(app)

# Restrict to specific origin (production)
CORS(app, origins=['https://your-frontend-url.com'])
```

### Add Environment Variables

Create `.env` file in project root:
```bash
ANTHROPIC_API_KEY=your_claude_api_key_here
PORT=5000
FLASK_ENV=development  # or 'production'
```

## 🎯 Usage Tips

### Example Prompts to Try

1. "Plan a 3-day trip to Tokyo for food and culture"
2. "I want to visit Barcelona for 2 days, focus on architecture"
3. "Family trip to Singapore for 4 days, kid-friendly"
4. "Show me Paris highlights for 3 days"
5. "Plan a 5-day trip to New York"
6. "London trip for 3 days, museums and history"

### Supported Cities

- Tokyo 🇯🇵
- Barcelona 🇪🇸
- Singapore 🇸🇬
- Paris 🇫🇷
- New York 🇺🇸
- London 🇬🇧

## 🐛 Troubleshooting

### Backend won't start
- Check `.env` file has `ANTHROPIC_API_KEY`
- Ensure Flask is installed: `pip install flask flask-cors`
- Check port 5000 is not in use

### Frontend can't connect to backend
- Verify backend is running on port 5000
- Check browser console for CORS errors
- Make sure `API_BASE_URL` in `app.js` is correct

### "Invalid API key" errors
- Verify your Anthropic API key is correct
- Check `.env` file is in project root
- Ensure `python-dotenv` loads the `.env` file

### Calendar download fails
- Check the itinerary was created successfully
- Verify backend has write permissions
- Check browser console for errors

## 📊 Adding Features

### Add New Cities

Edit `data_sources.py` to add more destinations.

### Customize UI

Edit `styles.css` to change colors, fonts, layout.

### Add Analytics

Add Google Analytics or other tracking to `index.html`.

### Add Authentication

Implement user accounts with Flask-Login or JWT tokens.

## 🔒 Security Notes

- Never commit `.env` file or API keys to Git
- Use HTTPS in production (automatic on Railway/Render)
- Restrict CORS to your frontend domain only
- Consider rate limiting for API endpoints
- Validate all user inputs on backend

## 📝 License

MIT License - see [LICENSE](../LICENSE) file for details

---

**Built with ❤️ for CalHacks 12.0 | Powered by Fetch.ai & Claude AI**
