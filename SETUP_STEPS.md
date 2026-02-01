# 🚀 Final Setup Steps

Your bot token is configured! Now follow these simple steps:

## Step 1: Find Your Bot on Telegram

1. **Open Telegram** (on your phone or desktop)

2. **Search for your bot**:
   - Click on the search icon
   - Type: `@` and then search for your bot name
   - OR click this link to open directly:
     ```
     https://t.me/YOUR_BOT_USERNAME
     ```

3. **Start a conversation**:
   - Click **START** button
   - OR send any message like "Hello" or "Hi"

## Step 2: Get Your Chat ID

Once you've sent a message to your bot, run:

```bash
source venv/bin/activate
python get_chat_id.py
```

This will show you your **Chat ID** (a number like `123456789`)

## Step 3: Update Configuration

The script will tell you your Chat ID. Then:

1. **Open config.env**:
   ```bash
   nano config.env
   # or use any text editor
   ```

2. **Find this line**:
   ```env
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

3. **Replace with your actual Chat ID**:
   ```env
   TELEGRAM_CHAT_ID=123456789
   ```

4. **Save the file**

## Step 4: Test Everything

Run the test script:

```bash
python test_setup.py
```

You should see:
- ✅ All checks passing
- 📱 A test notification sent to your Telegram

## Step 5: Start Monitoring!

Run the monitor:

```bash
python monitor.py
```

That's it! You'll now receive instant notifications whenever JKSSB posts something new.

---

## 🆘 Need Help?

### Can't find your bot?

Your bot token is: `8585238092:AAF1RbQmPT87phek0HvDVTwp0ESFSo7mTbA`

Get bot info:
```bash
curl https://api.telegram.org/bot8585238092:AAF1RbQmPT87phek0HvDVTwp0ESFSo7mTbA/getMe
```

### Alternative: Get Chat ID Manually

1. Send a message to your bot
2. Visit this URL in your browser:
   ```
   https://api.telegram.org/bot8585238092:AAF1RbQmPT87phek0HvDVTwp0ESFSo7mTbA/getUpdates
   ```
3. Look for `"chat":{"id":123456789}`
4. Copy the number after `"id":`

---

**Next**: Once configured, see `QUICKSTART.md` for automation options!
