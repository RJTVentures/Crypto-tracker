[QUICKSTART.md](https://github.com/user-attachments/files/27228771/QUICKSTART.md)
# Quick Start Guide

Get up and running with RJTVentures Crypto Tracker in 5 minutes!

## ⚡ Quick Install

### 1. Download
```bash
git clone https://github.com/yourusername/rjtventures-crypto-tracker.git
cd rjtventures-crypto-tracker
```

### 2. Install Python Dependencies
```bash
pip3 install requests --break-system-packages
```

(SQLite3 is included with Python)

### 3. Start Server
```bash
python3 server_coingecko.py
```

You should see:
```
🚀 SERVER STARTED
   Port: 2816
   CoinGecko API: Active
   Update Interval: 600 seconds
   
🔄 Fetching initial prices...
✅ Price cache loaded: XX coins
```

### 4. Open Tracker
Open `tracker-v2.0-COMPLETE.html` in your browser, or navigate to:
```
http://localhost:2816/tracker-v2.0-COMPLETE.html
```

## 🎯 First Steps

### Add Your First Crypto
1. Click **+ Add Crypto**
2. Search for "Bitcoin" (or your coin)
3. Enter amount: `0.05`
4. Select source: `Hardware Wallet`
5. Click **Add to Portfolio**

### Record a Transaction
1. Find your holding
2. Click **Buy More** button
3. Enter:
   - Amount: `0.01`
   - Price paid: `145000`
   - Fee: `5.00`
4. Click **Confirm Buy**

### Add to Watchlist
1. Click **Watchlist** tab
2. Click **+ Add to Watchlist**
3. Search for coin (e.g., "Ethereum")
4. Add optional notes
5. Click **Add to Watchlist**

### Set Up Budget
1. Click **Budget** tab
2. Click **+ Add Income**
3. Fill in:
   - Category: Salary
   - Description: Monthly Pay
   - Frequency: Monthly
   - Amount: 5000
4. Click **Add Income**

## 🔧 Common Tasks

### Export Portfolio
Settings ⚙️ → Export Portfolio Data → Save JSON

### Import Portfolio
Settings ⚙️ → Import Portfolio Data → Select JSON file

### View Price History
Click 📈 Chart icon next to any crypto

### Browse Backups
Settings ⚙️ → Browse Backups → Select backup to restore

## ⚠️ Troubleshooting

### Server won't start
```bash
# Check Python version (need 3.8+)
python3 --version

# Check if port 2816 is in use
lsof -i :2816

# Try different port (edit server_coingecko.py)
PORT = 2817
```

### Prices show $0.00
1. Ensure server is running
2. Hard refresh: Ctrl+Shift+R (Cmd+Shift+R on Mac)
3. Check browser console for errors (F12)

### 429 Rate Limit Error
Edit `server_coingecko.py`:
```python
UPDATE_INTERVAL = 900  # Increase from 600 to 900 (15 minutes)
```

## 📚 Next Steps

- Read full [README.md](README.md) for detailed features
- Check [CHANGELOG.md](CHANGELOG.md) for version history
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## 💡 Pro Tips

1. **Backup regularly**: Settings → Export Portfolio Data
2. **Let server run**: Needs 24 hours for accurate 24h change calculations
3. **Use categories**: Helps visualize your portfolio breakdown
4. **Track fees**: Important for tax calculations
5. **Link liabilities**: Connect mortgages to properties for equity tracking

## 🆘 Need Help?

- Check [Issues](https://github.com/yourusername/rjtventures-crypto-tracker/issues)
- Read [FAQ](#) (coming soon)
- Email: [your-email@example.com]

Happy tracking! 📊
