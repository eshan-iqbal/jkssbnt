"""WhatsApp notification handler (via Twilio)"""

import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class WhatsAppNotifier:
    """Send notifications via WhatsApp using Twilio API"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_WHATSAPP_FROM')  # Format: whatsapp:+14155238886
        self.to_number = os.getenv('TWILIO_WHATSAPP_TO')      # Format: whatsapp:+919876543210
        
        # Only import twilio if credentials are provided
        if self.is_configured():
            try:
                from twilio.rest import Client
                self.client = Client(self.account_sid, self.auth_token)
            except ImportError:
                logger.error("Twilio library not installed. Run: pip install twilio")
                self.client = None
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        """Check if WhatsApp/Twilio is properly configured"""
        return all([
            self.account_sid,
            self.auth_token,
            self.from_number,
            self.to_number
        ])
    
    def send(self, notifications: List[Dict[str, str]]):
        """
        Send notifications via WhatsApp
        
        Args:
            notifications: List of notification dictionaries
        """
        if not notifications:
            return
        
        if not self.is_configured():
            logger.warning("WhatsApp not properly configured. Skipping WhatsApp notification.")
            return
        
        if not self.client:
            logger.error("Twilio client not initialized")
            return
        
        # Build message
        message = "🚨 *New JKSSB Notification(s)*\n\n"
        
        for i, notif in enumerate(notifications, 1):
            message += f"*{i}. {notif['title']}*\n"
            
            if notif.get('date'):
                message += f"📅 Date: {notif['date']}\n"
            
            if notif.get('link'):
                message += f"🔗 {notif['link']}\n"
            
            message += "\n"
        
        message += f"⏰ Checked at: {notifications[0].get('fetched_at', 'N/A')}\n"
        message += "\n_Stay updated with JKSSB notifications!_"
        
        # Send message
        try:
            message_obj = self.client.messages.create(
                from_=self.from_number,
                body=message,
                to=self.to_number
            )
            
            logger.info(f"Successfully sent WhatsApp notification. SID: {message_obj.sid}")
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp notification: {e}")
            raise


# Note: To use WhatsApp notifications, you need:
# 1. Twilio account (free trial available)
# 2. Install twilio: pip install twilio
# 3. Set environment variables:
#    - TWILIO_ACCOUNT_SID
#    - TWILIO_AUTH_TOKEN
#    - TWILIO_WHATSAPP_FROM (e.g., whatsapp:+14155238886)
#    - TWILIO_WHATSAPP_TO (e.g., whatsapp:+919876543210)
