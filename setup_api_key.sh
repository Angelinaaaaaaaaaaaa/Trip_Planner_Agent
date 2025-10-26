#!/bin/bash
# Quick setup script to enable AI planning

echo "🤖 AI Trip Planning Setup"
echo "========================="
echo ""

# Check if .env already exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    echo ""
    cat .env
    echo ""
    read -p "Do you want to replace it? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file."
        exit 0
    fi
fi

# Get API key from user
echo "Please enter your Anthropic API key:"
echo "(Get it from: https://console.anthropic.com/)"
echo ""
read -p "API Key (starts with sk-ant-api03-): " api_key

# Validate format
if [[ ! $api_key =~ ^sk-ant-api03- ]]; then
    echo ""
    echo "❌ Invalid API key format!"
    echo "API keys should start with: sk-ant-api03-"
    exit 1
fi

# Create .env file
echo "ANTHROPIC_API_KEY=$api_key" > .env
echo ""
echo "✅ .env file created!"
echo ""

# Test if it can be loaded
echo "Testing API key..."
python3 << EOF
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("ANTHROPIC_API_KEY")

if key:
    print(f"✅ API key loaded successfully!")
    print(f"   Key starts with: {key[:20]}...")
else:
    print("❌ Failed to load API key")
    exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Restart the backend:"
    echo "   pkill -f 'python.*app.py'"
    echo "   python3 web_app/backend/app.py"
    echo ""
    echo "2. Look for this message:"
    echo "   ✅ LLM Integration: ENABLED"
    echo "   🌍 Capability: Can plan trips to ANY city worldwide!"
    echo ""
    echo "3. Try planning a trip to San Diego!"
    echo ""
    echo "Now you can plan trips to ANY city in the world! 🌍"
else
    echo ""
    echo "❌ Setup failed. Please check your Python environment."
    exit 1
fi
