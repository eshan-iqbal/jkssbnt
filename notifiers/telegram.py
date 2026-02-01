"""Telegram notification handler"""

import requests
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Send notifications via Telegram bot"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send(self, notifications: List[Dict[str, str]]):
        """
        Send notifications to Telegram
        
        Args:
            notifications: List of notification dictionaries
        """
        if not notifications:
            return
        
        # Limit to top 10 most recent notifications
        MAX_NOTIFICATIONS = 10
        notifications_to_show = notifications[:MAX_NOTIFICATIONS]
        remaining_count = len(notifications) - MAX_NOTIFICATIONS
        
        # Build message
        message = "🚨 <b>New JKSSB Notification(s)</b>\n\n"
        
        for i, notif in enumerate(notifications_to_show, 1):
            message += f"<b>{i}. {notif['title'][:100]}</b>\n"
            
            if notif.get('date'):
                message += f"📅 Date: {notif['date']}\n"
            
            if notif.get('link'):
                message += f"🔗 <a href=\"{notif['link']}\">View Details</a>\n"
            
            message += "\n"
        
        # Add summary for remaining notifications
        if remaining_count > 0:
            message += f"<i>... and {remaining_count} more notification(s)</i>\n\n"
        
        message += f"⏰ Checked at: {notifications[0].get('fetched_at', 'N/A')}\n"
        message += f"📊 Total: {len(notifications)} notification(s)\n"
        message += "\n🔔 <i>Stay updated with JKSSB notifications!</i>"
        
        # Send message
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
            
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Successfully sent Telegram notification for {len(notifications)} notification(s)")
            
        except requests.RequestException as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test if bot token and chat ID are valid"""
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            bot_info = response.json()
            if bot_info.get('ok'):
                logger.info(f"Telegram bot connected: @{bot_info['result']['username']}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Telegram connection test failed: {e}")
            return False
