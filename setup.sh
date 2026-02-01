#!/bin/bash

# JKSSB Monitor Setup Script
# This script helps you set up the notification monitor

echo "🚨 JKSSB Notification Monitor - Setup"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create config file if it doesn't exist
if [ ! -f "config.env" ]; then
    echo ""
    echo "⚙️  Creating configuration file..."
    cp config.example.env config.env
    echo "✅ Created config.env"
    echo ""
    echo "⚠️  IMPORTANT: Please edit config.env and add your credentials:"
    echo "   - TELEGRAM_BOT_TOKEN (from @BotFather)"
    echo "   - TELEGRAM_CHAT_ID (from Telegram API)"
    echo ""
    echo "📖 See README.md for detailed setup instructions"
else
    echo "✅ config.env already exists"
fi

# Create data and logs directories
mkdir -p data logs

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.env with your Telegram credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python monitor.py"
echo ""
echo "For automated monitoring, see README.md for cron setup"
