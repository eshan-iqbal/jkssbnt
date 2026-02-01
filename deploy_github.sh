#!/bin/bash

# Quick Deploy to GitHub Actions
# This script automates the entire setup process

set -e  # Exit on error

echo "🚀 JKSSB Monitor - GitHub Actions Deployment"
echo "============================================"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Installing..."
    sudo apt update
    sudo apt install gh -y
fi

# Check if logged in to GitHub
if ! gh auth status &> /dev/null; then
    echo "🔐 Please login to GitHub..."
    gh auth login
fi

echo "✅ GitHub CLI ready"
echo ""

# Initialize git if needed
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: JKSSB Monitor"
fi

# Create GitHub repository
echo "📤 Creating GitHub repository..."
if gh repo create jkssb-monitor --public --source=. --push; then
    echo "✅ Repository created and pushed"
else
    echo "⚠️  Repository might already exist. Pushing changes..."
    git push -u origin main || git push -u origin master
fi

echo ""
echo "🔑 Adding secrets to GitHub..."

# Add secrets
gh secret set TELEGRAM_BOT_TOKEN --body "8585238092:AAF1RbQmPT87phek0HvDVTwp0ESFSo7mTbA"
echo "✅ TELEGRAM_BOT_TOKEN added"

gh secret set TELEGRAM_CHAT_ID --body "1084763055"
echo "✅ TELEGRAM_CHAT_ID added"

echo ""
echo "🎯 Triggering first workflow run..."
gh workflow run monitor.yml

echo ""
echo "============================================"
echo "✅ Deployment Complete!"
echo "============================================"
echo ""
echo "📊 Your monitor is now set up on GitHub Actions!"
echo ""
echo "📅 Schedule: Runs at 9 AM and 9 PM IST daily"
echo "📱 Notifications: Sent to your Telegram"
echo "💰 Cost: FREE (2000 minutes/month included)"
echo ""
echo "🔍 View your workflows:"
echo "   https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/actions"
echo ""
echo "📝 View logs:"
echo "   gh run list"
echo "   gh run view --log"
echo ""
echo "🎉 You're all set! Check your Telegram for notifications."
echo ""
