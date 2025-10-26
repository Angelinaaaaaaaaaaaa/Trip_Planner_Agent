# Quick Reference Card

## ✅ System Status: WORKING

---

## 🚀 Quick Start (3 Steps)

```bash
# 1. Install dependencies
pip3 install anthropic flask flask-cors python-dotenv uagents

# 2. Start backend
python3 web_app/backend/app.py

# 3. Start frontend (new terminal)
cd web_app/frontend/public && python3 -m http.server 8080
```

**Open:** http://localhost:8080

---

## ✅ Test Prompts (These Work!)

```
Plan a 3-day trip to Tokyo
Show me Paris highlights
Barcelona for 2 days
new york
london
Singapore trip
```

---

## ❌ These Will Fail (Not in Static DB)

```
Prague
Rome
Dubai
```

**Error:** "City X is not supported"
**Fix:** Add `ANTHROPIC_API_KEY` to `.env` file

---

## 🔑 Enable AI for ALL Cities

```bash
# Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-api03-your-key-here" > .env

# Restart backend
pkill -f "python.*app.py"
python3 web_app/backend/app.py
```

Now **ANY city** works (Prague, Rome, Dubai, etc.)!

---

## 🐛 Quick Debug

### Backend not working?
```bash
# Kill old processes
pkill -9 -f "python.*app.py"

# Reinstall dependencies
pip3 install anthropic flask flask-cors

# Start fresh
python3 web_app/backend/app.py
```

### Frontend shows errors?
- Check browser console (F12)
- Should see: "✅ Backend detected on port XXXX"
- Should NOT see: "is_city_supported is not defined"

### CORS errors?
- Use `http://localhost:8080` (NOT `file://`)
- Verify backend running: `curl http://localhost:5001/api/health`

---

## ✅ Verify It Works

```bash
# Run tests
python3 test_core_functionality.py

# Expected output:
# 🎉 ALL TESTS PASSED! (28/28)
```

---

## 📋 Supported Cities (No API Key Needed)

1. Tokyo
2. Barcelona
3. Singapore
4. Paris
5. New York
6. London

**All these work:** tokyo, TOKYO, Tokyo, tokyo., new york, NEW YORK ✅

---

## ⚡ Your Error Explained

```
Error: City "Prague" is not supported yet.
```

**This is CORRECT!** ✅

Prague is not in the static database. Either:
1. Use Tokyo/Paris/Barcelona/etc. (works now)
2. Add API key (then Prague will work)

---

## 🎯 Success Checklist

- [ ] Installed: `pip3 install anthropic flask flask-cors`
- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:8080
- [ ] Can see example prompts
- [ ] **Can plan trip to Tokyo** ✅
- [ ] Prague rejected (correct!)

---

## 📚 Full Docs

- **Getting Started:** `FINAL_WORKING_GUIDE.md`
- **Setup:** `QUICKSTART_UPDATED.md`
- **Tests:** `python3 test_core_functionality.py`

---

**The system works! Just use Tokyo/Paris/Barcelona and you're good to go!** 🎉
