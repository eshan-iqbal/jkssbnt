# 🚀 GitHub Actions Setup Guide

## Quick Setup (5 Minutes)

### Step 1: Install GitHub CLI (if not installed)

```bash
# Check if already installed
gh --version

# If not installed:
sudo apt update
sudo apt install gh -y

# Login to GitHub
gh auth login
```

### Step 2: Create GitHub Repository

```bash
cd /home/eshan/Desktop/Agent/jkssb-monitor

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: JKSSB Monitor"

# Create GitHub repository and push
gh repo create jkssb-monitor --public --source=. --push
```

### Step 3: Add Secrets to GitHub

**Option A: Using GitHub CLI (Easiest)**

```bash
# Add Telegram bot token
gh secret set TELEGRAM_BOT_TOKEN --body "8585238092:AAF1RbQmPT87phek0HvDVTwp0ESFSo7mTbA"

# Add Telegram chat ID
gh secret set TELEGRAM_CHAT_ID --body "1084763055"
```

**Option B: Using GitHub Web UI**

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add:
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: `8585238092:AAF1RbQmPT87phek0HvDVTwp0ESFSo7mTbA`
5. Click **Add secret**
6. Repeat for:
   - Name: `TELEGRAM_CHAT_ID`
   - Value: `1084763055`

### Step 4: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. If prompted, click **I understand my workflows, go ahead and enable them**

### Step 5: Test the Workflow

**Option A: Manual Trigger (Test Now)**

```bash
gh workflow run monitor.yml
```

Or on GitHub:
1. Go to **Actions** tab
2. Click **JKSSB Monitor** workflow
3. Click **Run workflow** → **Run workflow**

**Option B: Wait for Scheduled Run**

The workflow will automatically run at:
- **9:00 AM IST** (3:30 AM UTC)
- **9:00 PM IST** (3:30 PM UTC)

### Step 6: View Logs

```bash
# View recent workflow runs
gh run list

# View logs of latest run
gh run view --log
```

Or on GitHub:
1. Go to **Actions** tab
2. Click on a workflow run
3. Click on the **monitor** job
4. View the logs

---

## ✅ What Happens Now

1. **Automatic Execution**: GitHub Actions runs your monitor 2x daily
2. **Notification Check**: Fetches JKSSB notifications
3. **Smart Detection**: Compares with previous data
4. **Telegram Alert**: Sends you new notifications
5. **Data Persistence**: Saves state back to repository

---

## 📊 Monitor Your Workflow

### View Workflow Status

```bash
# List recent runs
gh run list --workflow=monitor.yml

# Watch a run in real-time
gh run watch
```

### Check Logs

```bash
# View latest run logs
gh run view --log

# View specific run
gh run view <run-id> --log
```

### On GitHub Web

1. Go to repository
2. Click **Actions** tab
3. See all runs with status (✅ success, ❌ failed)

---

## 🔧 Customization

### Change Schedule

Edit `.github/workflows/monitor.yml`:

```yaml
schedule:
  # Every 6 hours
  - cron: '0 */6 * * *'
  
  # Every hour
  - cron: '0 * * * *'
  
  # 3 times a day (9 AM, 3 PM, 9 PM IST)
  - cron: '30 3,9,15 * * *'
```

**Cron Format**: `minute hour day month weekday`

**Common Schedules**:
- Every 30 minutes: `*/30 * * * *`
- Every hour: `0 * * * *`
- Every 6 hours: `0 */6 * * *`
- Twice daily (9 AM, 9 PM IST): `30 3,15 * * *`
- Once daily (9 AM IST): `30 3 * * *`

### Add Email Notifications

Add to secrets:
```bash
gh secret set EMAIL_ENABLED --body "true"
gh secret set SMTP_USERNAME --body "your_email@gmail.com"
gh secret set SMTP_PASSWORD --body "your_app_password"
gh secret set EMAIL_TO --body "recipient@example.com"
```

Update workflow to include email env vars.

---

## 🐛 Troubleshooting

### Workflow Not Running?

1. **Check if Actions are enabled**:
   - Repository → Settings → Actions → Allow all actions

2. **Check secrets are set**:
   ```bash
   gh secret list
   ```

3. **Manually trigger**:
   ```bash
   gh workflow run monitor.yml
   ```

### Workflow Failing?

1. **View logs**:
   ```bash
   gh run view --log
   ```

2. **Common issues**:
   - Missing secrets → Add them
   - Invalid bot token → Check token
   - Network issues → GitHub will retry

### Not Receiving Notifications?

1. **Check workflow ran successfully** (green ✅)
2. **Check logs** for "Successfully sent Telegram notification"
3. **Test bot manually**:
   ```bash
   python test_setup.py
   ```

---

## 💰 Cost & Limits

### GitHub Actions Free Tier

- **2,000 minutes/month** for public repos
- **500 MB storage** for artifacts
- **Unlimited** for public repos

### Your Usage

- **Per run**: ~1 minute
- **2 runs/day**: 60 runs/month
- **Total usage**: ~60 minutes/month
- **Remaining**: 1,940 minutes/month

**Verdict**: You'll use only **3%** of your free quota! 🎉

---

## 🎯 Next Steps

1. ✅ Repository created
2. ✅ Secrets added
3. ✅ Workflow configured
4. ✅ Actions enabled
5. ⏳ Wait for first scheduled run OR trigger manually

**You're all set!** Your monitor will now run automatically twice daily, completely free! 🚀

---

## 📱 What You'll Receive

At 9 AM and 9 PM IST daily, if there are new JKSSB notifications, you'll get:

```
🚨 New JKSSB Notification(s)

1. [New Notification Title]
📅 Date: 01-02-2026
🔗 View Details

⏰ Checked at: 2026-02-01T09:00:00
📊 Total: 1 notification(s)

🔔 Stay updated with JKSSB notifications!
```

**Never miss another JKSSB update!** 🎊
