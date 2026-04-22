# 🚀 Quick Start Guide

Get up and running with RJTVentures Crypto Tracker in 5 minutes!

## Step 1: Installation (2 minutes)

### Download
```bash
git clone https://github.com/yourusername/rjtventures-crypto-tracker.git
cd rjtventures-crypto-tracker
```

### Install
```bash
chmod +x install.sh
./install.sh
```

## Step 2: Start the Server (30 seconds)

```bash
python3 server_coingecko.py
```

You should see:
```
✅ Server started on http://localhost:8080
✅ Automatic price updates every 5 minutes
```

## Step 3: Open in Browser (10 seconds)

Navigate to:
```
http://localhost:8080
```

## Step 4: Add Your First Coin (1 minute)

### Method 1: Add to Holdings
1. Find the "Add Holding" section
2. Enter coin name: `bitcoin` or symbol: `BTC`
3. Enter amount: `0.001`
4. Select source: `Hardware Wallet`
5. Click **"Add to Portfolio"**

Done! You'll see:
- Current price
- Your holding value
- 24h change

### Method 2: Add to Watchlist
1. Scroll to "Watchlist" section
2. Click **"+ Add to Watchlist"**
3. Enter: `ethereum` or `ETH`
4. Add note: "Watching for dip"
5. Click **"Add to Watchlist"**

Price history starts building immediately!

## Step 5: Explore Features (1 minute)

### View Your Portfolio
- Check total value (top of page)
- See 24h performance
- View holdings table

### Check Price Charts
- Click any coin name
- View price history
- See statistics

### Backup Your Data
- Click **"💾 Backup to Server"** (top right)
- Backup saved automatically
- Kept for 30 days

## Common First-Time Questions

### Q: How do I add more coins?
**A:** Just click "Add Holding" or "Add to Watchlist" - supports 10,000+ coins!

### Q: Where is my data stored?
**A:** 
- Holdings: Your browser (localStorage)
- Prices: Local database (price_history.db)
- Backups: backups/ folder

### Q: Is my data private?
**A:** Yes! Everything stays on YOUR computer. No external servers (except CoinGecko for prices).

### Q: How often do prices update?
**A:** Every 5 minutes automatically.

### Q: Can I use symbols instead of full names?
**A:** Yes! Use BTC, ETH, ADA, etc. The tracker will find the right coin.

### Q: What if I misspell a coin name?
**A:** The tracker will search and suggest the correct name.

## What to Do Next

### Essential Setup
1. ✅ Add all your holdings
2. ✅ Set up watchlist for coins you're researching
3. ✅ Create your first backup

### Recommended
1. Record existing transactions (for accurate profit/loss)
2. Customize portfolio name
3. Export a JSON backup

### Optional
1. Browse price history charts
2. Check transaction history
3. Explore different view modes

## Tips for Best Experience

### Daily Use
- Check portfolio summary at top
- Monitor watchlist for entry points
- Review 24h change percentages

### Weekly Tasks
- Export JSON backup (safekeeping)
- Review transaction history
- Check price charts for trends

### Monthly Review
- Analyze performance charts
- Review watchlist decisions
- Clean up old transactions

## Keyboard Shortcuts

- **Shift + Command + R** - Hard refresh (clears cache)
- **Command + R** - Regular refresh
- **F12** - Open browser console (for debugging)

## Next Steps

- Read the full [README.md](README.md) for detailed features
- Check [CHANGELOG.md](CHANGELOG.md) for version history
- See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to help improve the tracker

## Need Help?

1. **Troubleshooting:** See README.md → Troubleshooting section
2. **Features:** See README.md → Usage Guide
3. **Issues:** Open an issue on GitHub

---

**That's it! You're ready to track your crypto portfolio! 🎉**

Happy tracking! 📊
