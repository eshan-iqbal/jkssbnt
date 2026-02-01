#!/usr/bin/env python3
"""
JKSSB Notification Monitor
Monitors JKSSB website for new notifications and sends alerts
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set
import time

# Import notification handlers
from notifiers.telegram import TelegramNotifier
from notifiers.email import EmailNotifier

# Configuration
URL = "https://jkssb.nic.in/Whatsnew.html"
DATA_DIR = Path("data")
LOG_DIR = Path("logs")
DATA_FILE = DATA_DIR / "notifications.json"
LOG_FILE = LOG_DIR / "monitor.log"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class JKSSBMonitor:
    """Main monitoring class for JKSSB notifications"""
    
    def __init__(self):
        self.url = URL
        self.data_file = DATA_FILE
        self.notifiers = []
        
        # Initialize notifiers
        self._init_notifiers()
        
    def _init_notifiers(self):
        """Initialize all enabled notification channels"""
        # Telegram
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if telegram_token and telegram_chat_id:
            self.notifiers.append(
                TelegramNotifier(telegram_token, telegram_chat_id)
            )
            logger.info("Telegram notifier initialized")
        
        # Email
        if os.getenv('EMAIL_ENABLED', 'false').lower() == 'true':
            email_notifier = EmailNotifier()
            if email_notifier.is_configured():
                self.notifiers.append(email_notifier)
                logger.info("Email notifier initialized")
        
        if not self.notifiers:
            logger.warning("No notifiers configured! Please set up at least one notification channel.")
    
    def fetch_notifications(self) -> List[Dict[str, str]]:
        """
        Fetch current notifications from JKSSB website
        
        Returns:
            List of notification dictionaries with 'title', 'date', and 'link'
        """
        try:
            logger.info(f"Fetching notifications from {self.url}")
            
            # Add headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(self.url, timeout=20, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            notifications = []
            
            # Find all notification links with class 'linkText'
            link_elements = soup.find_all('a', class_='linkText')
            
            if not link_elements:
                logger.warning("Could not find notification links on page")
                return []
            
            for link_tag in link_elements:
                # Extract title
                title = link_tag.text.strip()
                
                # Extract link
                href = link_tag.get('href', '')
                link = ""
                if href:
                    # Make absolute URL if relative
                    if href.startswith('http'):
                        link = href
                    else:
                        base_url = "https://jkssb.nic.in/"
                        link = base_url + href.lstrip('../').lstrip('/')
                
                # Extract date from PDF filename (format: _DDMMYYYY.pdf)
                date = ""
                if href:
                    import re
                    # Look for date pattern in filename: _DDMMYYYY.pdf
                    date_match = re.search(r'_(\d{2})(\d{2})(\d{4})\.pdf', href)
                    if date_match:
                        day, month, year = date_match.groups()
                        date = f"{day}-{month}-{year}"
                
                if title:  # Only add if we have a title
                    notifications.append({
                        'title': title,
                        'date': date,
                        'link': link,
                        'fetched_at': datetime.now().isoformat()
                    })
            
            logger.info(f"Successfully fetched {len(notifications)} notifications")
            return notifications
            
        except requests.RequestException as e:
            logger.error(f"Error fetching notifications: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while fetching notifications: {e}")
            return []
    
    def load_old_notifications(self) -> List[Dict[str, str]]:
        """Load previously saved notifications from file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data)} old notifications")
                    return data
            except Exception as e:
                logger.error(f"Error loading old notifications: {e}")
                return []
        else:
            logger.info("No previous notification data found")
            return []
    
    def save_notifications(self, notifications: List[Dict[str, str]]):
        """Save notifications to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(notifications, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(notifications)} notifications to file")
        except Exception as e:
            logger.error(f"Error saving notifications: {e}")
    
    def find_new_notifications(
        self, 
        current: List[Dict[str, str]], 
        old: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Find notifications that are in current but not in old
        
        Args:
            current: Current notifications from website
            old: Previously saved notifications
            
        Returns:
            List of new notifications
        """
        # Create sets of titles for comparison
        old_titles = {notif['title'] for notif in old}
        
        # Find new notifications
        new_notifications = [
            notif for notif in current 
            if notif['title'] not in old_titles
        ]
        
        return new_notifications
    
    def send_notifications(self, new_notifications: List[Dict[str, str]]):
        """Send notifications through all configured channels"""
        if not new_notifications:
            logger.info("No new notifications to send")
            return
        
        logger.info(f"Sending {len(new_notifications)} new notifications")
        
        for notifier in self.notifiers:
            try:
                notifier.send(new_notifications)
            except Exception as e:
                logger.error(f"Error sending notification via {notifier.__class__.__name__}: {e}")
    
    def run(self):
        """Main monitoring logic - single check"""
        logger.info("=" * 50)
        logger.info("Starting JKSSB notification check")
        logger.info("=" * 50)
        
        # Fetch current notifications
        current_notifications = self.fetch_notifications()
        
        if not current_notifications:
            logger.warning("No notifications fetched. Skipping this check.")
            return
        
        # Load old notifications
        old_notifications = self.load_old_notifications()
        
        # Find new notifications
        new_notifications = self.find_new_notifications(
            current_notifications, 
            old_notifications
        )
        
        if new_notifications:
            logger.info(f"Found {len(new_notifications)} new notification(s)!")
            
            # Send notifications
            self.send_notifications(new_notifications)
            
            # Save updated notifications
            self.save_notifications(current_notifications)
            
            logger.info("Notification check completed successfully")
        else:
            logger.info("No new notifications found")
            
            # Still update the file to track fetch time
            if current_notifications != old_notifications:
                self.save_notifications(current_notifications)
    
    def run_continuous(self, interval: int = 1800):
        """
        Run monitoring continuously with specified interval
        
        Args:
            interval: Seconds between checks (default: 1800 = 30 minutes)
        """
        logger.info(f"Starting continuous monitoring (interval: {interval}s)")
        
        while True:
            try:
                self.run()
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            logger.info(f"Waiting {interval} seconds until next check...")
            time.sleep(interval)


def load_config():
    """Load configuration from config.env file"""
    config_file = Path("config.env")
    
    if config_file.exists():
        logger.info("Loading configuration from config.env")
        with open(config_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    else:
        logger.warning("config.env not found. Using environment variables only.")


def main():
    """Main entry point"""
    # Load configuration
    load_config()
    
    # Create monitor instance
    monitor = JKSSBMonitor()
    
    # Check if continuous mode is requested
    continuous = os.getenv('CONTINUOUS_MODE', 'false').lower() == 'true'
    interval = int(os.getenv('CHECK_INTERVAL', '1800'))
    
    if continuous:
        monitor.run_continuous(interval)
    else:
        # Single run (for cron jobs)
        monitor.run()


if __name__ == "__main__":
    main()
