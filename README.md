# 🏦 RJTVentures Crypto Tracker

A self-hosted cryptocurrency portfolio tracker. Track your crypto holdings, monitor prices in real-time, maintain a watchlist, and keep complete transaction history - all running locally on your own machine.

![Version](https://img.shields.io/badge/version-1.3-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)

## ✨ Features

### 📊 Portfolio Tracking
- Track holdings across multiple wallets and exchanges
- Real-time price updates every 5 minutes
- 24-hour price change tracking
- Portfolio performance charts
- Cost basis and profit/loss calculations

### 👀 Watchlist
- Track coins before buying
- Personal notes for each coin
- Live price updates
- Quick conversion to holdings

### 📈 Price History
- Automatic 5-minute price snapshots
- Historical price charts
- 365-day retention
- SQLite database storage

### 💾 Backup & Restore
- Server-side backups
- Export/Import as JSON
- 30-day backup retention
- Browse and restore previous backups

### 🎨 Professional Design
- Banker green/gold color scheme
- Clean, modern interface
- Responsive design
- Smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- macOS, Linux, or Windows

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/rjtventures-crypto-tracker.git
cd rjtventures-crypto-tracker
```

2. **Run the installation script**
```bash
chmod +x install.sh
./install.sh
```

Or manually:

3. **Start the server**
```bash
python3 server_coingecko.py
```

4. **Open your browser**
```
http://localhost:8080
```

That's it! 🎉

## 📖 Usage Guide

### Adding Your First Holding

1. Click the **"Add Holding"** button in the Holdings section
2. Enter the cryptocurrency name or symbol (e.g., "bitcoin" or "BTC")
3. Enter the amount you own
4. Select the source (Hardware Wallet, CoinSpot, etc.)
5. Click **"Add to Portfolio"**

The tracker will automatically fetch the current price and calculate your holding value.

### Using the Watchlist

1. Navigate to the **Watchlist** section
2. Click **"+ Add to Watchlist"**
3. Enter the coin name or symbol
4. Optionally add notes (e.g., "Waiting for dip below $0.80")
5. Price history starts building immediately!

When you're ready to buy, click **"💰 Buy This"** to move it to your holdings.

### Recording Transactions

All transactions are automatically logged when you:
- Add a holding (Buy)
- Sell a holding (Sell)
- Swap between coins (Swap)
- Add staking rewards (Staking Reward)

View complete history in the **Transaction History** section.

### Backup Your Data

**Server Backup:**
1. Click **"💾 Backup to Server"** (top right)
2. Backups saved to `backups/` folder
3. Kept for 30 days automatically

**Export JSON:**
1. Click **"📥 Export Data"**
2. Save the JSON file securely
3. Import later with **"📤 Import Data"**

## 🏗️ Architecture

### Components

**Frontend (`tracker.html`)**
- Single-page application
- Pure HTML/CSS/JavaScript
- Chart.js for visualizations
- LocalStorage for data persistence

**Backend (`server_coingecko.py`)**
- Python HTTP server
- CoinGecko API integration
- SQLite price history database
- Automatic backup management

### Data Storage

**Browser (localStorage):**
- Holdings
- Transactions
- Watchlist
- Settings
- Price cache

**Server (files):**
- `price_history.db` - Price snapshots (SQLite)
- `tracked_coins.json` - Coin tracking list
- `backups/` - Portfolio backups

## 🔧 Configuration

### Changing the Server Port

Edit `server_coingecko.py`:
```python
PORT = 8080  # Change to your preferred port
```

### Price Update Interval

Default: 5 minutes. To change:
```python
UPDATE_INTERVAL = 300  # Seconds (5 minutes)
```

### Backup Retention

Default: 30 days. To change:
```python
KEEP_BACKUPS_DAYS = 30  # Days
```

## 🌐 Supported Cryptocurrencies

### Currently Tracking (24 coins):
- Bitcoin (BTC)
- Ethereum (ETH)
- Cardano (ADA)
- Ripple (XRP)
- Solana (SOL)
- Dogecoin (DOGE)
- Litecoin (LTC)
- Tron (TRX)
- Stellar (XLM)
- EOS
- Polygon (POL/MATIC)
- Aave (AAVE)
- Chainlink (LINK)
- The Graph (GRT)
- Hedera (HBAR)
- Fetch.ai (FET)
- And more...

### Adding More Coins

The tracker automatically supports **10,000+ coins** from CoinGecko!

**To add a coin to tracking:**
1. Add it to your watchlist OR
2. Add it as a holding

The server will automatically start tracking prices.

## 🔐 Privacy & Security

### Your Data is Private

✅ **All data stays on YOUR computer**
- Holdings stored in browser
- Price database stored locally
- Backups stored on your machine
- No data sent to external servers (except CoinGecko for prices)

### No Account Required

- No registration
- No login
- No email
- No tracking
- 100% self-hosted

### Backup Recommendations

1. **Regular Exports:** Export JSON weekly
2. **Server Backups:** Automatic (kept 30 days)
3. **Database Backup:** Copy `price_history.db` periodically
4. **Source Control:** Keep `tracked_coins.json` backed up

## 🛠️ Troubleshooting

### Server Won't Start

**Error:** `Port 8080 already in use`
```bash
# Find what's using the port
lsof -i :8080
# Kill it or change PORT in server_coingecko.py
```

### Prices Not Loading

1. Check server is running
2. Hard refresh browser (Shift + Command + R)
3. Check server terminal for errors
4. Verify internet connection

### Watchlist Shows "Loading..."

1. Verify server is running
2. Wait for next price update (every 5 min)
3. Check coin ID is correct in `tracked_coins.json`
4. Restart server: `Ctrl+C` then `python3 server_coingecko.py`

### Missing Price History

Price history builds over time:
- **Minimum:** 2-3 days for meaningful charts
- **Optimal:** 7+ days
- **Note:** History only starts when coin is added

## 📊 API Information

### CoinGecko API

**Free Tier Limits:**
- 50 calls/minute
- No API key required
- 10,000+ coins supported

**This tracker uses:**
- ~1 call every 5 minutes
- Well within free limits
- No rate limiting issues

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/rjtventures-crypto-tracker.git
cd rjtventures-crypto-tracker

# Make changes
# Test thoroughly
# Submit PR
```

## 📝 Changelog

### [1.3.0] - 2026-04-22
#### Fixed
- Polygon coin ID updated to `polygon-ecosystem-token`
- Watchlist price loading issues resolved
- Backup browse endpoint added
- All 404 errors fixed

### [1.2.0] - 2026-04-22
#### Fixed
- Watchlist prices now update correctly
- Fixed price fetching to include watchlist coins

### [1.1.0] - 2026-04-22
#### Fixed
- Removed loading message from watchlist modal
- Cache busting meta tags added

### [1.0.0] - 2026-04-20
#### Added
- Initial release
- Banker green theme
- Watchlist feature
- Complete portfolio tracking
- Price history charts
- Server backups

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 💬 Support

Having issues? Check:
1. [Troubleshooting Guide](#-troubleshooting)
2. [Installation Guide](#-quick-start)
3. Open an issue on GitHub

## 🎯 Roadmap

### Planned Features (v2.0)
- [ ] Tabbed interface for cleaner UX
- [ ] Price alerts
- [ ] Portfolio comparison
- [ ] Multi-currency support (USD, EUR, etc.)
- [ ] Mobile app version
- [ ] Docker containerization

### Under Consideration
- [ ] Tax reporting
- [ ] DeFi protocol integration
- [ ] NFT tracking
- [ ] Hardware wallet direct integration

## 🙏 Acknowledgments

- **CoinGecko** - For the free crypto API
- **Chart.js** - For beautiful charts
- **Open Source Community** - For inspiration and tools

---

**Made with 💚 by RJTVentures**

*Self-hosted. Private. Powerful.*
