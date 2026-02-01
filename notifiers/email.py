"""Email notification handler"""

import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Send notifications via email"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.username = os.getenv('SMTP_USERNAME')
        self.password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('SMTP_FROM', self.username)
        self.to_email = os.getenv('EMAIL_TO')
    
    def is_configured(self) -> bool:
        """Check if email is properly configured"""
        return all([
            self.smtp_server,
            self.smtp_port,
            self.username,
            self.password,
            self.to_email
        ])
    
    def send(self, notifications: List[Dict[str, str]]):
        """
        Send notifications via email
        
        Args:
            notifications: List of notification dictionaries
        """
        if not notifications:
            return
        
        if not self.is_configured():
            logger.warning("Email not properly configured. Skipping email notification.")
            return
        
        # Build email content
        subject = f"🚨 {len(notifications)} New JKSSB Notification(s)"
        
        # HTML body
        html_body = self._build_html_body(notifications)
        
        # Plain text body (fallback)
        text_body = self._build_text_body(notifications)
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Successfully sent email notification for {len(notifications)} notification(s)")
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            raise
    
    def _build_html_body(self, notifications: List[Dict[str, str]]) -> str:
        """Build HTML email body"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 20px; border-radius: 10px 10px 0 0; }
                .notification { background: #f8f9fa; padding: 15px; margin: 10px 0; 
                               border-left: 4px solid #667eea; border-radius: 5px; }
                .notification h3 { margin: 0 0 10px 0; color: #667eea; }
                .notification p { margin: 5px 0; }
                .link { display: inline-block; margin-top: 10px; padding: 8px 15px; 
                       background: #667eea; color: white; text-decoration: none; 
                       border-radius: 5px; }
                .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 New JKSSB Notifications</h1>
                    <p>You have new notifications from JKSSB website</p>
                </div>
        """
        
        for i, notif in enumerate(notifications, 1):
            html += f"""
                <div class="notification">
                    <h3>{i}. {notif['title']}</h3>
            """
            
            if notif.get('date'):
                html += f"<p>📅 <strong>Date:</strong> {notif['date']}</p>"
            
            if notif.get('link'):
                html += f'<p><a href="{notif["link"]}" class="link">View Details →</a></p>'
            
            html += "</div>"
        
        html += f"""
                <div class="footer">
                    <p>⏰ Checked at: {notifications[0].get('fetched_at', 'N/A')}</p>
                    <p>This is an automated notification from JKSSB Monitor</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _build_text_body(self, notifications: List[Dict[str, str]]) -> str:
        """Build plain text email body"""
        text = "🚨 NEW JKSSB NOTIFICATIONS\n"
        text += "=" * 50 + "\n\n"
        
        for i, notif in enumerate(notifications, 1):
            text += f"{i}. {notif['title']}\n"
            
            if notif.get('date'):
                text += f"   Date: {notif['date']}\n"
            
            if notif.get('link'):
                text += f"   Link: {notif['link']}\n"
            
            text += "\n"
        
        text += f"Checked at: {notifications[0].get('fetched_at', 'N/A')}\n"
        text += "\n---\nThis is an automated notification from JKSSB Monitor"
        
        return text
