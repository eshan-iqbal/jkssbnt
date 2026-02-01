# 🚀 Quick Start Guide

Get your JKSSB notification monitor running in 5 minutes!

## Step 1: Get Telegram Bot Credentials

### Create Your Bot

1. Open Telegram and search for **@BotFather**
2. Send `/start`
3. Send `/newbot`
4. Follow the prompts:
   - Choose a name (e.g., "JKSSB Alert")
   - Choose a username (e.g., "jkssb_alert_bot")
5. **Copy the bot token** (looks like: `1234567890:AAHsdjsjdjsjdjsjdj`)

### Get Your Chat ID

1. Send a message to your bot (any message)
2. Open this URL in your browser (replace `<YOUR_TOKEN>` with your bot token):
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
3. Look for `"chat":{"id":123456789}` in the response
4. **Copy the chat ID** (the number)

## Step 2: Configure the Monitor

1. **Copy the example config:**
   ```bash
   cp config.example.env config.env
   ```

2. **Edit config.env:**
   ```bash
   nano config.env
   # or use any text editor
   ```

3. **Add your credentials:**
   ```env
   TELEGRAM_BOT_TOKEN=1234567890:AAHsdjsjdjsjdjsjdj
   TELEGRAM_CHAT_ID=123456789
   ```

4. **Save the file**

## Step 3: Test Your Setup

Run the test script:

```bash
source venv/bin/activate
python test_setup.py
```

You should see:
- ✅ Dependencies installed
- ✅ Configuration verified
- ✅ Website scraping working
- ✅ Telegram bot connected
- 📱 Test notification sent to your Telegram

## Step 4: Run the Monitor

### Single Check (for testing)

```bash
python monitor.py
```

This will:
1. Check JKSSB website
2. Compare with previous data
3. Send notification if new items found
4. Save current data

### Continuous Monitoring

Edit `config.env`:
```env
CONTINUOUS_MODE=true
CHECK_INTERVAL=1800  # 30 minutes
```

Then run:
```bash
python monitor.py
```

The monitor will keep running and check every 30 minutes.

## Step 5: Automate with Cron (Recommended)

For production use, set up a cron job:

1. **Edit crontab:**
   ```bash
   crontab -e
   ```

2. **Add this line** (check every 30 minutes):
   ```bash
   */30 * * * * cd /home/eshan/Desktop/Agent/jkssb-monitor && /home/eshan/Desktop/Agent/jkssb-monitor/venv/bin/python monitor.py >> logs/cron.log 2>&1
   ```

3. **Save and exit**

Now the monitor will run automatically every 30 minutes!

## 📱 What You'll Receive

When a new notification appears on JKSSB, you'll get a Telegram message like:

```
🚨 New JKSSB Notification(s)

1. Advertisement Notification No. 03 of 2026
📅 Date: 01-02-2026
🔗 View Details

⏰ Checked at: 2026-02-01T20:00:00

🔔 Stay updated with JKSSB notifications!
```

## 🔧 Troubleshooting

### Not receiving notifications?

1. **Check logs:**
   ```bash
   tail -f logs/monitor.log
   ```

2. **Verify bot token and chat ID:**
   ```bash
   python test_setup.py
   ```

3. **Make sure you sent a message to your bot first**

### Script errors?

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.9+
   ```

2. **Reinstall dependencies:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Check internet connection**

## 🎯 Next Steps

### Add Email Notifications

Edit `config.env`:
```env
EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_TO=recipient@example.com
```

For Gmail, create an [App Password](https://support.google.com/accounts/answer/185833).

### Deploy to Cloud

- **Docker**: See `docker-compose.yml`
- **AWS Lambda**: See `AWS_LAMBDA.md`
- **VPS**: Use systemd service (see below)

### Create Systemd Service (Linux)

Create `/etc/systemd/system/jkssb-monitor.service`:

```ini
[Unit]
Description=JKSSB Notification Monitor
After=network.target

[Service]
Type=simple
User=eshan
WorkingDirectory=/home/eshan/Desktop/Agent/jkssb-monitor
Environment="CONTINUOUS_MODE=true"
Environment="CHECK_INTERVAL=1800"
ExecStart=/home/eshan/Desktop/Agent/jkssb-monitor/venv/bin/python monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable jkssb-monitor
sudo systemctl start jkssb-monitor
sudo systemctl status jkssb-monitor
```

## 📊 Monitoring

View logs in real-time:
```bash
tail -f logs/monitor.log
```

Check stored notifications:
```bash
cat data/notifications.json | python -m json.tool
```

## 🎉 You're All Set!

Your personal JKSSB notification agent is now running. You'll be notified instantly whenever new notifications appear on the website.

**Questions?** Check the main [README.md](README.md) for detailed documentation.
