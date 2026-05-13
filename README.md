# RJTVentures Crypto Tracker + Scanner

A self-hosted cryptocurrency portfolio tracker and market scanner, running entirely on your local network from an old iMac. No subscription, no cloud, no third-party account required beyond a free CoinGecko API key.

All prices are in **AUD** via the CoinGecko API.

---

## What's Included

| File | Description |
|------|-------------|
| `server_coingecko.py` | Local Python HTTP server — the shared data layer |
| `tracker.html` | Portfolio tracker — holdings, DCA plans, tax tools, budget |
| `crypto-scanner.html` | Market scanner — top 250 coins, watchlist, news, Fear & Greed |

---

## Features

### Tracker (`tracker.html`)
- Portfolio holdings with live AUD prices
- Price history charts (local SQLite DB, 5-min snapshots)
- DCA calculator and active plan tracking with next-purchase reminders
- Tax reporting (CGT estimates)
- Budget / income / expense tracker
- Staking positions and traditional assets
- Automatic server-side backups (30-day retention)
- Multi-device sync via backup download/import

### Scanner (`crypto-scanner.html`)
- Top 250 coins by market cap — gainers, losers, all coins table
- 1H / 24H / 7D / 30D % change columns
- Watchlist synced with tracker via server
- Opportunities and trending coins panel
- Coin sector categories
- Fear & Greed Index in header
- Crypto news feed (CoinDesk + Cointelegraph RSS)
- DCA reminder panel (reads active plans from tracker backup)

### Server (`server_coingecko.py`)
- Single Python file, no external dependencies beyond stdlib
- Serves both HTML files, handles all API calls
- Caches market data in memory (2-min refresh)
- Price history stored in SQLite (`price_history.db`)
- Shared watchlist persisted to `shared_watchlist.json`
- Fear & Greed proxied from `api.alternative.me`
- News RSS proxied from CoinDesk and Cointelegraph
- CORS headers on all responses (works from any device on your LAN)

---

## Setup

### Requirements
- Python 3.8+ (pre-installed on macOS)
- No pip installs required — stdlib only

### First Run

```bash
cd ~/Desktop/crypto-server
python3 server_coingecko.py
```

Open your browser to `http://localhost:8080`.

### Optional: CoinGecko API Key

Create a file called `coingecko_key.txt` in the same folder as the server, containing just your Demo API key on one line:

```
CG-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Get a free key at [coingecko.com/en/developers](https://www.coingecko.com/en/developers). This increases your rate limits and is recommended if you use the scanner heavily.

### Auto-Start on Boot (macOS LaunchAgent)

Create `~/Library/LaunchAgents/com.rjtventures.cryptotracker.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.rjtventures.cryptotracker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/Desktop/crypto-server/server_coingecko.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/Desktop/crypto-server</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/Desktop/crypto-server/server.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/Desktop/crypto-server/server.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.rjtventures.cryptotracker.plist
```

Restart it after updating files:
```bash
launchctl unload ~/Library/LaunchAgents/com.rjtventures.cryptotracker.plist
launchctl load  ~/Library/LaunchAgents/com.rjtventures.cryptotracker.plist
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve tracker.html |
| GET | `/scanner` | Serve crypto-scanner.html |
| GET | `/api/prices` | Portfolio prices with 24h change |
| GET | `/api/price-history/<id>` | Price history for one coin (`?days=30`) |
| GET | `/api/status` | Server health and cache status |
| GET | `/api/markets` | Top-250 market data for scanner |
| GET | `/api/global` | Global market cap, BTC dominance, DeFi |
| GET | `/api/trending` | Trending coins |
| GET | `/api/categories` | Coin sector categories |
| GET | `/api/portfolio` | Portfolio coin IDs from latest backup |
| GET | `/api/watchlist` | Shared watchlist (read) |
| GET | `/api/chart/<id>` | Chart data from local DB |
| GET | `/api/feargreed` | Fear & Greed Index |
| GET | `/api/news` | News feed (`?filter=bitcoin\|markets\|altcoins\|defi`) |
| GET | `/api/dca_plans` | DCA plans from latest backup |
| GET | `/api/backup/list` | List backup files |
| GET | `/api/backup/download/<fn>` | Download a backup file |
| POST | `/api/prices` | Fetch prices for specific coins |
| POST | `/api/coins/add` | Add a coin to tracked list |
| POST | `/api/backup/save` | Save portfolio backup |
| POST | `/api/watchlist` | Update shared watchlist |

---

## File Structure

```
crypto-server/
├── server_coingecko.py      # Main server
├── tracker.html             # Portfolio tracker
├── crypto-scanner.html      # Market scanner
├── coingecko_key.txt        # API key (not committed)
├── tracked_coins.json       # Auto-generated — tracked coin list
├── shared_watchlist.json    # Auto-generated — shared watchlist
├── price_history.db         # Auto-generated — SQLite price history
└── backups/                 # Auto-generated — portfolio backups
    └── portfolio-backup-YYYY-MM-DD_HH-MM-SS.json
```

---

## Version History

| Version | Changes |
|---------|---------|
| v3.1 | Fear & Greed Index, news RSS panel (CoinDesk + Cointelegraph), DCA reminder panel in scanner, shared watchlist sync |
| v3.0 | Scanner integration, `/api/markets`, `/api/global`, `/api/trending`, `/api/categories`, shared watchlist |
| v2.0 | Switched from CoinSpot to CoinGecko, price history DB, multi-device backup sync |
| v1.0 | Initial release — basic portfolio price tracker |

---

## Notes

- The server runs locally and is only accessible on your home network. It is not intended to be exposed to the internet.
- `coingecko_key.txt` is excluded from version control via `.gitignore`.
- Backup files and the SQLite database are also excluded — they contain personal financial data.
