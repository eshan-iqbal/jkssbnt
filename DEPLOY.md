# 🚀 Simple Deployment Guide

## Option 1: One-Command Deploy (Automated)

If you have GitHub CLI installed:

```bash
./deploy_github.sh
```

This will automatically:
- Install GitHub CLI (if needed)
- Create repository
- Add secrets
- Deploy to GitHub Actions

---

## Option 2: Manual Setup (5 Minutes)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `jkssb-monitor`
3. Make it **Public**
4. Click **Create repository**

### Step 2: Push Code to GitHub

```bash
cd /home/eshan/Desktop/Agent/jkssb-monitor

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/jkssb-monitor.git

# Push
git branch -M main
git push -u origin main
```

### Step 3: Add Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these two secrets:

**Secret 1:**
- Name: `TELEGRAM_BOT_TOKEN`
- Value: `8585238092:AAF1RbQmPT87phek0HvDVTwp0ESFSo7mTbA`

**Secret 2:**
- Name: `TELEGRAM_CHAT_ID`
- Value: `1084763055`

### Step 4: Enable Actions

1. Go to **Actions** tab
2. Click **I understand my workflows, go ahead and enable them**

### Step 5: Test Run

1. Go to **Actions** tab
2. Click **JKSSB Monitor** workflow
3. Click **Run workflow** → **Run workflow**

**Done!** ✅

---

## Option 3: Local Cron Job (No GitHub)

If you want to run it on your local machine:

### Set Up Cron Job

```bash
# Open crontab editor
crontab -e

# Add this line (runs at 9 AM and 9 PM daily)
0 9,21 * * * cd /home/eshan/Desktop/Agent/jkssb-monitor && /home/eshan/Desktop/Agent/jkssb-monitor/venv/bin/python monitor.py >> logs/cron.log 2>&1

# Save and exit
```

**Schedule Explanation:**
- `0 9,21 * * *` = At 9:00 and 21:00 (9 PM) every day
- `0 */6 * * *` = Every 6 hours
- `*/30 * * * *` = Every 30 minutes

### View Cron Logs

```bash
tail -f logs/cron.log
```

**Limitation**: Your computer must be ON at scheduled times.

---

## 🎯 Recommended: GitHub Actions

**Why?**
- ✅ Runs even when your computer is off
- ✅ Completely free
- ✅ No maintenance
- ✅ Reliable

**Local Cron is good if:**
- Your computer is always on
- You don't want to use GitHub
- You want more control

---

## 📊 Quick Comparison

| Method | Cost | Reliability | Computer Must Be On? |
|--------|------|-------------|---------------------|
| **GitHub Actions** | Free | ⭐⭐⭐⭐⭐ | ❌ No |
| **Local Cron** | Free | ⭐⭐⭐ | ✅ Yes |

---

## 🆘 Need Help?

**GitHub Actions Setup**: See `GITHUB_ACTIONS_SETUP.md`  
**Free Hosting Options**: See `FREE_HOSTING.md`  
**Local Cron**: Use Option 3 above

Choose the method that works best for you! 🚀
