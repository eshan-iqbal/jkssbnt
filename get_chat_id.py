#!/usr/bin/env python3
"""
Get your Telegram Chat ID
"""

import requests
import sys

BOT_TOKEN = "8585238092:AAF1RbQmPT87phek0HvDVTwp0ESFSo7mTbA"

def get_chat_id():
    """Get chat ID from Telegram bot"""
    print("🔍 Fetching your Telegram Chat ID...\n")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('ok'):
            print("❌ Error: Bot token might be invalid")
            return
        
        updates = data.get('result', [])
        
        if not updates:
            print("⚠️  No messages found!")
            print("\n📱 Please do the following:")
            print("1. Open Telegram")
            print("2. Search for your bot")
            print("3. Send any message to your bot (e.g., 'Hello')")
            print("4. Run this script again")
            return
        
        # Get the most recent chat
        latest_update = updates[-1]
        chat = latest_update.get('message', {}).get('chat', {})
        chat_id = chat.get('id')
        
        if chat_id:
            print("✅ Success! Your Chat ID is:\n")
            print(f"   {chat_id}")
            print("\n📝 Next steps:")
            print(f"1. Open config.env")
            print(f"2. Replace 'your_chat_id_here' with: {chat_id}")
            print(f"3. Save the file")
            print(f"4. Run: python test_setup.py")
            
            # Also show bot info
            bot_info = get_bot_info()
            if bot_info:
                print(f"\n🤖 Your bot: @{bot_info.get('username')}")
                print(f"   Name: {bot_info.get('first_name')}")
        else:
            print("❌ Could not find chat ID")
            
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        print("\nPlease check your internet connection")
    except Exception as e:
        print(f"❌ Error: {e}")

def get_bot_info():
    """Get bot information"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('ok'):
            return data.get('result')
    except:
        pass
    
    return None

if __name__ == "__main__":
    print("=" * 60)
    print("📱 Telegram Chat ID Finder")
    print("=" * 60)
    print()
    
    get_chat_id()
    print()
