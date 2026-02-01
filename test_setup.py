#!/usr/bin/env python3
"""
Quick test script to verify your setup
"""

import os
import sys

def check_config():
    """Check if configuration is set up"""
    print("🔍 Checking configuration...\n")
    
    # Check if config.env exists
    if not os.path.exists('config.env'):
        print("❌ config.env not found!")
        print("   Run: cp config.example.env config.env")
        return False
    
    # Load config
    from pathlib import Path
    config_file = Path("config.env")
    config = {}
    
    with open(config_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    # Check Telegram config
    telegram_token = config.get('TELEGRAM_BOT_TOKEN', '')
    telegram_chat = config.get('TELEGRAM_CHAT_ID', '')
    
    if telegram_token == 'your_bot_token_here' or not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN not configured")
        print("   Get your token from @BotFather on Telegram")
        return False
    else:
        print(f"✅ Telegram bot token: {telegram_token[:10]}...")
    
    if telegram_chat == 'your_chat_id_here' or not telegram_chat:
        print("❌ TELEGRAM_CHAT_ID not configured")
        print("   Get your chat ID from Telegram API")
        return False
    else:
        print(f"✅ Telegram chat ID: {telegram_chat}")
    
    return True

def test_telegram():
    """Test Telegram connection"""
    print("\n📱 Testing Telegram connection...\n")
    
    try:
        from notifiers.telegram import TelegramNotifier
        
        # Load config
        from pathlib import Path
        config_file = Path("config.env")
        
        with open(config_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        notifier = TelegramNotifier(token, chat_id)
        
        if notifier.test_connection():
            print("✅ Telegram bot is working!")
            
            # Send test message
            print("\n📤 Sending test notification...")
            test_notif = [{
                'title': 'Test Notification - JKSSB Monitor is Working!',
                'date': '2026-02-01',
                'link': 'https://jkssb.nic.in',
                'fetched_at': '2026-02-01T20:00:00'
            }]
            
            notifier.send(test_notif)
            print("✅ Test notification sent! Check your Telegram.")
            return True
        else:
            print("❌ Telegram connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_scraping():
    """Test website scraping"""
    print("\n🌐 Testing JKSSB website scraping...\n")
    
    try:
        from monitor import JKSSBMonitor
        
        monitor = JKSSBMonitor()
        notifications = monitor.fetch_notifications()
        
        if notifications:
            print(f"✅ Successfully fetched {len(notifications)} notifications")
            print("\nFirst notification:")
            print(f"   Title: {notifications[0]['title'][:60]}...")
            if notifications[0].get('date'):
                print(f"   Date: {notifications[0]['date']}")
            return True
        else:
            print("❌ No notifications fetched")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🚨 JKSSB Monitor - Configuration Test")
    print("=" * 60)
    print()
    
    # Check dependencies
    try:
        import requests
        import bs4
        print("✅ Dependencies installed\n")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check configuration
    if not check_config():
        print("\n❌ Configuration incomplete")
        print("\nPlease edit config.env with your credentials")
        sys.exit(1)
    
    # Test scraping
    if not test_scraping():
        print("\n⚠️  Website scraping failed - check your internet connection")
    
    # Test Telegram
    if not test_telegram():
        print("\n❌ Telegram test failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Your monitor is ready to use.")
    print("=" * 60)
    print("\nTo start monitoring:")
    print("  python monitor.py")
    print("\nFor continuous monitoring:")
    print("  Set CONTINUOUS_MODE=true in config.env")
    print()

if __name__ == "__main__":
    main()
