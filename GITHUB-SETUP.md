# 🚀 GitHub Setup Guide

Complete step-by-step instructions for putting your tracker on GitHub.

## 📋 What You'll Need

- GitHub account (free at github.com)
- Git installed on your computer
- Terminal access

---

## Step 1: Create GitHub Account (if needed)

1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration process
4. Verify your email

---

## Step 2: Create a New Repository

1. Click the **"+"** icon (top right)
2. Select **"New repository"**
3. Fill in details:
   - **Name:** `rjtventures-crypto-tracker`
   - **Description:** "Self-hosted cryptocurrency portfolio tracker with watchlist and price history"
   - **Visibility:** **Public** (so others can use it) or **Private** (just for you)
   - **DO NOT** check "Initialize with README" (we already have one)
4. Click **"Create repository"**

---

## Step 3: Install Git (if needed)

### macOS
```bash
# Check if Git is installed
git --version

# If not installed
brew install git
# OR download from https://git-scm.com/
```

### Linux
```bash
sudo apt install git  # Ubuntu/Debian
sudo yum install git  # CentOS/RHEL
```

### Windows
Download from https://git-scm.com/download/win

---

## Step 4: Configure Git (first time only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 5: Upload Your Project

### Navigate to your project folder
```bash
cd ~/Downloads/rjtventures-crypto-tracker
```

### Initialize Git
```bash
git init
```

### Add all files
```bash
git add .
```

### Create first commit
```bash
git commit -m "Initial release v1.3 - Full crypto tracker with watchlist"
```

### Connect to GitHub
Replace `YOUR-USERNAME` with your actual GitHub username:
```bash
git remote add origin https://github.com/YOUR-USERNAME/rjtventures-crypto-tracker.git
```

### Push to GitHub
```bash
git branch -M main
git push -u origin main
```

---

## Step 6: Verify Upload

1. Go to your repository on GitHub
2. You should see all files:
   - README.md
   - LICENSE
   - CHANGELOG.md
   - tracker.html
   - server_coingecko.py
   - install.sh
   - etc.

---

## Step 7: Add a Description

1. Click **"About"** (⚙️ icon, top right of repo)
2. Add description: "Self-hosted crypto portfolio tracker with watchlist and price history"
3. Add topics: `cryptocurrency`, `portfolio`, `tracker`, `python`, `coingecko`
4. Save changes

---

## Step 8: Verify .gitignore Works

Check that these files are NOT on GitHub:
- ❌ price_history.db
- ❌ tracked_coins.json
- ❌ backups/

If you see them, something went wrong! They contain your personal data.

**To fix:**
```bash
git rm --cached price_history.db
git rm --cached tracked_coins.json
git rm --cached -r backups/
git commit -m "Remove personal data files"
git push
```

---

## 🎉 Success!

Your tracker is now on GitHub! Others can:
- View the code
- Download and use it
- Report issues
- Contribute improvements

**Your personal data is safe** - it's NOT on GitHub, only on your computer.

---

## Making Updates Later

When you make changes:

```bash
# 1. Add changed files
git add .

# 2. Commit with a message
git commit -m "Description of what you changed"

# 3. Push to GitHub
git push
```

---

## Common Issues

### "Permission denied"
You need to authenticate with GitHub. Options:
- Use HTTPS with a Personal Access Token
- Set up SSH keys

See: https://docs.github.com/en/authentication

### "Repository not found"
Check:
- Repository name is correct
- You're pushing to YOUR username's repo
- Repository exists on GitHub

### "Files won't upload"
Check:
- Files aren't too large (GitHub has 100MB limit)
- .gitignore isn't blocking them
- You ran `git add .` before committing

---

## Next Steps

### Add GitHub Topics
Make your repo discoverable:
1. Go to repo settings
2. Add topics: `crypto`, `portfolio-tracker`, `python`, `javascript`, `coingecko`, `self-hosted`

### Enable Issues
Allow people to report bugs:
1. Settings → General
2. Check "Issues"

### Add Release
Create v1.3 release:
1. Click "Releases"
2. "Create a new release"
3. Tag: v1.3
4. Title: "v1.3 - Watchlist & Price Tracking"
5. Description: Copy from CHANGELOG.md

---

## Questions?

- **GitHub Docs:** https://docs.github.com
- **Git Tutorial:** https://git-scm.com/docs/gittutorial
- **GitHub Learning Lab:** https://lab.github.com/

---

**Congratulations! Your tracker is now open source!** 🎉
