# 🚨 JKSSB Notification Monitor

An automated notification agent that monitors the JKSSB (Jammu & Kashmir Services Selection Board) website and sends instant alerts when new notifications are published.

## 🌟 Features

- ✅ **Real-time Monitoring**: Checks JKSSB website for new notifications
- ✅ **Multiple Alert Channels**: Telegram, Email, WhatsApp, SMS
- ✅ **Smart Detection**: Only alerts on genuinely new notifications
- ✅ **Error Handling**: Robust error handling and logging
- ✅ **Easy Deployment**: Run locally, on VPS, or AWS Lambda
- ✅ **Docker Support**: Containerized deployment option
- ✅ **Configurable**: Easy configuration via environment variables

## 🎯 What It Monitors

**Website**: [https://jkssb.nic.in/Whatsnew.html](https://jkssb.nic.in/Whatsnew.html)

The agent scrapes the "What's New" page and detects:
- New job notifications
- Advertisement notifications
- Result announcements
- Important updates

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Internet connection
- Telegram account (for Telegram notifications)

### Installation

1. **Clone or download this repository**

```bash
cd jkssb-monitor
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure your settings**

Copy the example config and edit it:

```bash
cp config.example.env config.env
```

Edit `config.env` with your credentials:

```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Email Configuration (optional)
EMAIL_ENABLED=false
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_TO=recipient@example.com
```

4. **Run the monitor**

```bash
python monitor.py
```

## 📱 Setting Up Telegram Bot

### Step 1: Create Bot

1. Open Telegram and search for `@BotFather`
2. Send `/start`
3. Send `/newbot`
4. Follow prompts to name your bot
5. Copy the **BOT TOKEN** (looks like: `1234567890:AAHsdjsjdjsjdjsjdj`)

### Step 2: Get Your Chat ID

1. Send a message to your bot
2. Visit this URL in your browser (replace `<YOUR_TOKEN>`):
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
3. Look for `"chat":{"id":123456789}` and copy the ID

### Step 3: Update Config

Add these to your `config.env`:
```env
TELEGRAM_BOT_TOKEN=1234567890:AAHsdjsjdjsjdjsjdj
TELEGRAM_CHAT_ID=123456789
```

## ⏰ Automated Monitoring

### Linux/Mac (Cron)

Edit crontab:
```bash
crontab -e
```

Add this line to check every 30 minutes:
```bash
*/30 * * * * cd /path/to/jkssb-monitor && /usr/bin/python3 monitor.py >> logs/cron.log 2>&1
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., every 30 minutes)
4. Set action: Run `python.exe` with argument `C:\path\to\monitor.py`

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t jkssb-monitor .

# Run container
docker run -d --name jkssb-monitor \
  --env-file config.env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  jkssb-monitor
```

### Docker Compose

```bash
docker-compose up -d
```

## ☁️ AWS Lambda Deployment

See [AWS_LAMBDA.md](AWS_LAMBDA.md) for detailed instructions on deploying to AWS Lambda with EventBridge scheduling.

## 📊 Project Structure

```
jkssb-monitor/
├── monitor.py              # Main monitoring script
├── notifiers/
│   ├── telegram.py         # Telegram notification handler
│   ├── email.py            # Email notification handler
│   └── whatsapp.py         # WhatsApp notification handler
├── config.example.env      # Example configuration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── data/                   # Stored notification data
├── logs/                   # Application logs
└── README.md               # This file
```

## 🔧 Configuration Options

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather | Yes (for Telegram) |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | Yes (for Telegram) |
| `EMAIL_ENABLED` | Enable email notifications | No |
| `SMTP_SERVER` | SMTP server address | No |
| `SMTP_PORT` | SMTP server port | No |
| `SMTP_USERNAME` | SMTP username | No |
| `SMTP_PASSWORD` | SMTP password | No |
| `EMAIL_TO` | Recipient email address | No |
| `CHECK_INTERVAL` | Seconds between checks (for continuous mode) | No |

## 📝 Logs

Logs are stored in the `logs/` directory:
- `monitor.log` - Main application log
- `cron.log` - Cron job output (if using cron)

## 🛠️ Troubleshooting

### No notifications received

1. Check logs in `logs/monitor.log`
2. Verify your bot token and chat ID
3. Ensure you've sent at least one message to your bot
4. Test manually: `python monitor.py`

### Script errors

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version: `python --version` (should be 3.9+)
3. Verify internet connection
4. Check if JKSSB website is accessible

## 🎯 Roadmap

- [ ] WhatsApp integration (via Twilio)
- [ ] SMS notifications
- [ ] Web dashboard
- [ ] Multiple website monitoring
- [ ] AI-powered notification summarization
- [ ] Mobile app
- [ ] PDF download automation

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool is for educational purposes. Please respect the JKSSB website's terms of service and don't overload their servers with too frequent requests.

---

**Made with ❤️ for job seekers**
