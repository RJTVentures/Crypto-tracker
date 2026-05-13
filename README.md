## 🚀 RJTVentures Crypto Tracker + Scanner — v3.1

> Major update adding live news, market sentiment, DCA reminders and watchlist sync across both apps.

---

### 🆕 New Features

**📰 Crypto News Feed**
Live headlines from CoinDesk and Cointelegraph, routed through your local server.
Filter by Bitcoin, Markets, Altcoins or DeFi. Available in both Tracker and Scanner.

**😨 Fear & Greed Index**
Real-time market sentiment score (0–100) in the header of both apps.
Sourced from alternative.me, proxied through your server, refreshes every 5 minutes.

**📅 DCA Reminder Panel**
New tab in the Scanner showing all active DCA plans from your tracker backup.
Sorted by next purchase date — cards go orange when due within 2 days, red when overdue.

**⭐ Shared Watchlist Sync**
Watchlist now syncs between Tracker and Scanner via your local server.
Add a coin in either app and it appears in both. Persisted to shared_watchlist.json.

---

### 🔧 What Changed

**server_coingecko.py**
- Added `/api/feargreed` — Fear & Greed Index proxy
- Added `/api/news` — CoinDesk + Cointelegraph RSS proxy (`?filter=bitcoin|markets|altcoins|defi`)
- Added `/api/dca_plans` — DCA plans from latest tracker backup
- Switched news source from CryptoPanic (Cloudflare blocked) to CoinDesk + Cointelegraph
- Full refactor — dead code removed, imports consolidated, functions renamed for clarity
- Handler class renamed `CryptoTrackerHandler` → `RJTVenturesHandler`
- All debug print statements removed

**tracker.html**
- Fear & Greed widget added to header
- New 📰 News tab added to navigation
- Watchlist pushes to server on load and on every change

**crypto-scanner.html**
- Fear & Greed added to header stat bar
- New 📰 News and 📅 DCA tabs added
- Watchlist syncs from server on load, pushes on every star toggle
- News filter updated: Bitcoin / Markets / Altcoins / DeFi

---

### 🔌 New API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feargreed` | Fear & Greed Index (alternative.me proxy) |
| GET | `/api/news` | RSS news feed (`?filter=bitcoin\|markets\|altcoins\|defi`) |
| GET | `/api/dca_plans` | DCA plans from latest tracker backup |
| POST | `/api/watchlist` | Now called by both Tracker and Scanner |

---

### 🚀 Installation

Replace these three files in `~/Desktop/crypto-server/`:
- `server_coingecko.py`
- `tracker.html`
- `crypto-scanner.html`

Then restart the server:
