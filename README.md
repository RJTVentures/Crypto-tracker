[README.md](https://github.com/user-attachments/files/27228756/README.md)
# RJTVentures Crypto Tracker v2.0

A comprehensive, self-hosted cryptocurrency portfolio tracker with support for traditional assets, liabilities, budget management, and automated backups.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Features

### Portfolio Management
- **Multi-Source Holdings**: Track crypto across hardware wallets, exchanges (CoinSpot, etc.)
- **Traditional Assets**: Manage property, superannuation, and other investments
- **Liabilities Tracking**: Monitor mortgages, loans, and debts with interest calculations
- **Metals Support**: Track gold and silver holdings
- **Real-Time Pricing**: Live price updates from CoinGecko API
- **24h Change Tracking**: Historical price change calculated from local database

### Transaction Management
- **Complete History**: Buy, Sell, Swap, Transfer, Send transactions
- **Fee Tracking**: Capture and analyze transaction fees across all operations
- **Staking Rewards**: Track rewards with automatic portfolio integration
- **CSV Export**: Export transaction history for accounting/tax purposes

### Budget & Planning
- **Income/Expense Tracking**: Categorized with frequency (weekly, fortnightly, monthly, yearly)
- **Asset Assignment**: Link income/expenses to specific investments
- **Custom Categories**: Create your own budget categories
- **Filter Views**: Show all, income only, or expenses only

### Analytics & Visualization
- **Portfolio Charts**: Distribution across crypto, metals, and traditional assets
- **Category Breakdowns**: Visualize holdings by investment category
- **Performance Tracking**: Historical portfolio value over time
- **Profit/Loss Analysis**: Track gains/losses across all holdings

### Data Management
- **Automatic Backups**: Daily automated backups to server
- **Manual Backups**: Export/import portfolio data as JSON
- **Price History Database**: Local SQLite database stores price data every 5 minutes
- **Browse Backups**: View and restore from previous backups

### Watchlist
- **Coin Monitoring**: Track coins you don't own yet
- **Quick Buy**: Convert watchlist items to holdings with one click
- **Custom Notes**: Add notes to watchlist items

## 📋 Requirements

### Frontend
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- LocalStorage support

### Backend (Server)
- Python 3.8+
- Required packages:
  ```bash
  pip install requests sqlite3 --break-system-packages
  ```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/rjtventures-crypto-tracker.git
cd rjtventures-crypto-tracker
```

### 2. Start the Server
```bash
python3 server_coingecko.py
```

The server will:
- Start on `http://localhost:2816`
- Create `price_history.db` for historical price data
- Create `backups/` directory for automatic backups
- Begin fetching prices every 10 minutes (configurable)

### 3. Open the Tracker
Open `tracker-v2.0-COMPLETE.html` in your web browser, or navigate to:
```
http://localhost:2816/tracker-v2.0-COMPLETE.html
```

## ⚙️ Configuration

### Server Settings
Edit `server_coingecko.py`:

```python
PORT = 2816  # Change server port
UPDATE_INTERVAL = 600  # Price update frequency (seconds)
```

### Tracker Settings
Click the ⚙️ Settings icon to configure:
- Portfolio name
- Default view modes
- Sort preferences

## 📊 Usage

### Adding Holdings
1. Click **+ Add Crypto** button
2. Enter coin name/symbol
3. Specify amount and source (wallet/exchange)
4. Optionally add purchase details for cost basis tracking

### Recording Transactions
Use the dedicated buttons for each transaction type:
- **Buy More**: Add to existing holdings
- **Sell**: Record sales
- **Swap**: Exchange one coin for another
- **Transfer**: Move between sources
- **Send**: Send to external address

### Managing Traditional Assets
1. Navigate to **Investments** tab
2. Click **+ Add Asset** in Traditional Assets section
3. Enter property details (name, value, source)
4. Link to liabilities if applicable (mortgages, etc.)

### Budget Tracking
1. Go to **Budget** tab
2. Add income sources with frequency
3. Add expenses with frequency
4. Optionally assign to specific assets (rental income, etc.)
5. Use filters to view income only or expenses only

### Viewing Price History
Click the 📈 Chart icon next to any crypto holding to see:
- 7 days / 30 days / 90 days / 1 year / Max timeframes
- Current price, highest, lowest, average
- Percentage change over period
- Data points collected

## 🔄 Backup & Restore

### Automatic Backups
- Run automatically every 24 hours
- Stored in `backups/` directory on server
- Filename format: `auto-backup-YYYY-MM-DDTHH-MM-SS.json`

### Manual Backups
1. Click **⚙️ Settings**
2. Click **💾 Export Portfolio Data**
3. Save JSON file locally

### Restore from Backup
1. Click **⚙️ Settings**
2. Click **📂 Browse Backups** (server) or **📥 Import Portfolio Data** (local file)
3. Select backup to restore
4. Confirm restoration

## 🗂️ File Structure

```
rjtventures-crypto-tracker/
├── tracker-v2.0-COMPLETE.html    # Main tracker application
├── server_coingecko.py           # Backend server
├── price_history.db              # SQLite price database (auto-created)
├── backups/                      # Automatic backups (auto-created)
└── README.md                     # This file
```

## 🔐 Data Storage

### LocalStorage (Browser)
- Holdings, transactions, watchlist
- Budget data, staking positions, liabilities
- Custom prices, user preferences
- Portfolio name, view modes

### SQLite Database (Server)
- Price history (every 5 minutes)
- Coin metadata
- Used for 24h change calculations

### Server Backups
- Complete portfolio snapshots
- Includes all holdings, transactions, budget data
- JSON format for easy import/export

## 🛠️ Troubleshooting

### Server Won't Start
- Check if port 2816 is already in use
- Verify Python 3.8+ is installed: `python3 --version`
- Install required packages

### 429 Rate Limit Errors
- CoinGecko free API has rate limits (10-30 calls/minute)
- Increase `UPDATE_INTERVAL` in server to 900+ seconds (15+ minutes)
- Reduce number of tracked coins

### Prices Showing $0.00
- Ensure server is running
- Check browser console for errors
- Hard refresh page (Ctrl+Shift+R)
- Clear browser cache

### 24h Change Shows 0.00%
- Requires 24+ hours of price history data
- Server must run continuously to collect data
- Check `price_history.db` has data: `sqlite3 price_history.db "SELECT COUNT(*) FROM price_history;"`

## 🔮 Future Enhancements

- [ ] Multi-currency support (USD, EUR, etc.)
- [ ] Tax reporting exports
- [ ] Mobile app (iOS/Android)
- [ ] Price alerts/notifications
- [ ] DCA (Dollar Cost Averaging) calculator
- [ ] API key support for exchanges
- [ ] Multi-user support
- [ ] Cloud sync option

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚠️ Disclaimer

This software is for personal portfolio tracking only. It is not financial advice. Cryptocurrency investments are volatile and risky. Always do your own research and never invest more than you can afford to lose.

## 📧 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Email: [your-email@example.com]

## 🙏 Acknowledgments

- Price data provided by [CoinGecko](https://www.coingecko.com/)
- Chart visualization using [Chart.js](https://www.chartjs.org/)
- Built in Perth, Western Australia 🇦🇺

---

**Made with ❤️ by Rob | RJTVentures**
