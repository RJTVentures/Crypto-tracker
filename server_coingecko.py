#!/usr/bin/env python3
"""
RJTVentures Crypto Server  v3.1
================================
Local Python HTTP server for the RJTVentures Crypto Tracker + Scanner.
Runs on your iMac (port 8080) and acts as a shared data layer for both
the tracker (tracker.html) and scanner (crypto-scanner.html).

All prices are in AUD via CoinGecko. No exchange account required.

API ENDPOINTS
─────────────
GET  /                          → tracker.html
GET  /scanner                   → crypto-scanner.html

GET  /api/prices                → portfolio coin prices with 24h change (from local DB)
GET  /api/price-history/<id>    → full price history for one coin (?days=30)
GET  /api/status                → server health + cache status
GET  /api/markets               → top-250 coins for scanner (cached 2 min)
GET  /api/global                → global market cap, BTC dominance, DeFi cap
GET  /api/trending              → trending coins (live)
GET  /api/categories            → coin sector categories (live)
GET  /api/portfolio             → coin IDs from latest tracker backup
GET  /api/watchlist             → shared watchlist (read)
GET  /api/chart/<id>            → price chart data from local DB (?days=30)
GET  /api/feargreed             → Fear & Greed Index (proxied from alternative.me)
GET  /api/news                  → crypto news RSS (?filter=bitcoin|markets|altcoins|defi)
GET  /api/dca_plans             → DCA plans from latest tracker backup
GET  /api/backup/list           → list saved backup files
GET  /api/backup/download/<fn>  → download a specific backup file

POST /api/prices                → request fresh prices for a specific coin list
POST /api/coins/add             → add a coin to the tracked list
POST /api/backup/save           → save a portfolio backup from the tracker
POST /api/watchlist             → update the shared watchlist

CONFIGURATION FILES (place in same folder as this script)
──────────────────────────────────────────────────────────
coingecko_key.txt      Optional — your CoinGecko Demo API key on one line.
                       Increases rate limits. Get one free at coingecko.com/en/developers.
tracked_coins.json     Auto-created — CoinGecko IDs tracked for portfolio prices.
shared_watchlist.json  Auto-created — shared watchlist between tracker and scanner.
backups/               Auto-created — portfolio backup files (30-day retention).
price_history.db       Auto-created — SQLite database of 5-minute price snapshots.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import re
import socket
import sqlite3
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

PORT               = 8080
COINGECKO_BASE     = 'https://api.coingecko.com/api/v3'
PRICE_ENDPOINT     = f'{COINGECKO_BASE}/simple/price'
PRICE_INTERVAL     = 300    # seconds between tracker price refreshes (5 min)
MARKETS_INTERVAL   = 120    # seconds between scanner market refreshes (2 min)
BACKUP_DIR         = 'backups'
BACKUP_RETENTION   = 30     # days to keep backup files
PRICE_DB           = 'price_history.db'
PRICE_HISTORY_DAYS = 365    # days of price history to retain in DB
COINS_FILE         = 'tracked_coins.json'
WATCHLIST_FILE     = 'shared_watchlist.json'

# CoinGecko IDs tracked by default — covers the RJT portfolio
DEFAULT_COINS = [
    'bitcoin', 'ethereum', 'solana', 'ripple', 'chainlink', 'aave',
    'fetch-ai', 'hedera-hashgraph', 'stellar', 'the-graph', 'tron',
    'thorchain', 'cardano', 'dogecoin', 'litecoin', 'tether',
    'neo', 'gas', 'power-ledger', 'eos',
]

# RSS feed URLs keyed by the ?filter= query parameter value
NEWS_FEEDS = {
    '':         ['https://www.coindesk.com/arc/outboundfeeds/rss/',
                 'https://cointelegraph.com/rss'],
    'bitcoin':  ['https://www.coindesk.com/arc/outboundfeeds/rss/?taxonomy=category&term=markets',
                 'https://cointelegraph.com/rss/tag/bitcoin'],
    'markets':  ['https://www.coindesk.com/arc/outboundfeeds/rss/?taxonomy=category&term=markets',
                 'https://cointelegraph.com/rss/tag/markets'],
    'altcoins': ['https://cointelegraph.com/rss/tag/altcoin',
                 'https://www.coindesk.com/arc/outboundfeeds/rss/'],
    'defi':     ['https://cointelegraph.com/rss/tag/defi',
                 'https://www.coindesk.com/arc/outboundfeeds/rss/'],
}

# Browser-like headers for RSS requests (plain Python UA gets blocked by some feeds)
RSS_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'application/rss+xml, application/xml, text/xml, */*',
}

# Keywords for lightweight news headline sentiment scoring
BULLISH_KEYWORDS = ('surge', 'rally', 'bull', 'gain', 'rise', 'high', 'breakout', 'adoption', 'soar', 'jump')
BEARISH_KEYWORDS = ('crash', 'drop', 'bear', 'fall', 'plunge', 'hack', 'ban', 'fear', 'warning', 'sink', 'tumble')


# ─────────────────────────────────────────────────────────────────────────────
# IN-MEMORY CACHES
# ─────────────────────────────────────────────────────────────────────────────

price_cache           = {}    # coin_id → {aud, aud_24h_change}
price_cache_updated   = None  # datetime of last successful price fetch

markets_cache         = []    # list of CoinGecko /coins/markets objects (top 250)
markets_cache_updated = None

global_cache          = {}    # CoinGecko /global data dict
global_cache_updated  = None


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def log(msg):
    """Print a timestamped server log line."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def get_local_ip():
    """Return the iMac's LAN IP address, or 'localhost' on failure."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return 'localhost'


def coingecko_headers():
    """
    Build request headers for CoinGecko.
    Includes the Demo API key from coingecko_key.txt if the file exists.
    """
    headers = {'User-Agent': 'RJTVentures/3.1'}
    if os.path.exists('coingecko_key.txt'):
        try:
            key = open('coingecko_key.txt').read().strip()
            if key:
                headers['x-cg-demo-api-key'] = key
        except Exception:
            pass
    return headers


def send_json(handler, data, status=200):
    """Send a JSON response with CORS headers."""
    body = json.dumps(data).encode()
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.end_headers()
    handler.wfile.write(body)


def serve_html_file(handler, filename):
    """Serve a local HTML file, or return 404 if not found."""
    try:
        with open(filename, 'rb') as f:
            handler.send_response(200)
            handler.send_header('Content-Type', 'text/html')
            handler.end_headers()
            handler.wfile.write(f.read())
    except FileNotFoundError:
        handler.send_error(404, f'{filename} not found')


# ─────────────────────────────────────────────────────────────────────────────
# TRACKED COIN LIST
# ─────────────────────────────────────────────────────────────────────────────

def load_tracked_coins():
    """Load tracked coins from disk, falling back to DEFAULT_COINS."""
    if os.path.exists(COINS_FILE):
        try:
            coins = json.load(open(COINS_FILE))
            if isinstance(coins, list):
                return coins
        except Exception:
            pass
    save_tracked_coins(DEFAULT_COINS)
    return DEFAULT_COINS


def save_tracked_coins(coins):
    """Persist the tracked coin list to disk."""
    try:
        json.dump(coins, open(COINS_FILE, 'w'), indent=2)
        return True
    except Exception as e:
        log(f'⚠️  Error saving tracked coins: {e}')
        return False


def add_tracked_coin(coin_id):
    """
    Add a coin to the tracked list if not already present.
    Returns True if the coin was added, False if it was already tracked.
    """
    coin_id = coin_id.lower().strip()
    coins   = load_tracked_coins()
    if coin_id not in coins:
        coins.append(coin_id)
        if save_tracked_coins(coins):
            log(f'➕ Added {coin_id} to tracked coins ({len(coins)} total)')
            return True
    return False


# Loaded once at startup; dynamically extended via add_tracked_coin
TRACKED_COINS = load_tracked_coins()


# ─────────────────────────────────────────────────────────────────────────────
# PRICE HISTORY DATABASE  (SQLite)
# ─────────────────────────────────────────────────────────────────────────────

def init_price_db():
    """Create the price_history table and index if they don't already exist."""
    conn = sqlite3.connect(PRICE_DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            coin_id   TEXT NOT NULL,
            price     REAL NOT NULL,
            timestamp TEXT NOT NULL,
            PRIMARY KEY (coin_id, timestamp)
        )
    ''')
    conn.execute('''
        CREATE INDEX IF NOT EXISTS idx_coin_timestamp
        ON price_history (coin_id, timestamp)
    ''')
    conn.commit()
    conn.close()
    log('💾 Price history database ready')


def save_price_snapshot(coin_id, price):
    """Write a single price point to the SQLite database."""
    try:
        conn = sqlite3.connect(PRICE_DB)
        conn.execute(
            'INSERT OR REPLACE INTO price_history (coin_id, price, timestamp) VALUES (?, ?, ?)',
            (coin_id, price, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
    except Exception as e:
        log(f'⚠️  DB write error ({coin_id}): {e}')


def save_all_price_snapshots():
    """Snapshot every coin in price_cache to the database."""
    if not price_cache:
        return
    count = 0
    for coin_id, data in price_cache.items():
        price = data.get('aud', 0) if isinstance(data, dict) else data
        if price and price > 0:
            save_price_snapshot(coin_id, price)
            count += 1
    if count:
        log(f'💾 Saved {count} price snapshots')


def get_price_history(coin_id, days=30):
    """Return a list of {timestamp, price} dicts for the given coin and time window."""
    try:
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        conn   = sqlite3.connect(PRICE_DB)
        rows   = conn.execute(
            'SELECT timestamp, price FROM price_history '
            'WHERE coin_id = ? AND timestamp >= ? ORDER BY timestamp ASC',
            (coin_id, cutoff)
        ).fetchall()
        conn.close()
        return [{'timestamp': r[0], 'price': r[1]} for r in rows]
    except Exception as e:
        log(f'⚠️  DB read error ({coin_id}): {e}')
        return []


def calculate_24h_change(coin_id):
    """
    Calculate the 24-hour percentage price change for a coin using the local DB.
    Returns 0.0 if insufficient history exists.
    """
    try:
        conn        = sqlite3.connect(PRICE_DB)
        current_row = conn.execute(
            'SELECT price FROM price_history WHERE coin_id = ? ORDER BY timestamp DESC LIMIT 1',
            (coin_id,)
        ).fetchone()
        cutoff_24h  = (datetime.now() - timedelta(hours=24)).isoformat()
        previous_row = conn.execute(
            'SELECT price FROM price_history '
            'WHERE coin_id = ? AND timestamp <= ? ORDER BY timestamp DESC LIMIT 1',
            (coin_id, cutoff_24h)
        ).fetchone()
        conn.close()
        if current_row and previous_row and previous_row[0] > 0:
            return ((current_row[0] - previous_row[0]) / previous_row[0]) * 100
        return 0.0
    except Exception as e:
        log(f'⚠️  24h change error ({coin_id}): {e}')
        return 0.0


def purge_old_price_data(days=PRICE_HISTORY_DAYS):
    """Delete price records older than `days` to keep the DB size in check."""
    try:
        cutoff  = (datetime.now() - timedelta(days=days)).isoformat()
        conn    = sqlite3.connect(PRICE_DB)
        deleted = conn.execute(
            'DELETE FROM price_history WHERE timestamp < ?', (cutoff,)
        ).rowcount
        conn.commit()
        conn.close()
        if deleted:
            log(f'🗑️  Purged {deleted} old price records')
    except Exception as e:
        log(f'⚠️  Error purging old price data: {e}')


# ─────────────────────────────────────────────────────────────────────────────
# BACKUP FILE MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────

def ensure_backup_dir():
    """Create the backups/ directory if it doesn't exist."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        log('📁 Created backups directory')


def purge_old_backups():
    """Delete backup JSON files older than BACKUP_RETENTION days."""
    try:
        cutoff  = datetime.now() - timedelta(days=BACKUP_RETENTION)
        removed = 0
        for fn in os.listdir(BACKUP_DIR):
            if fn.endswith('.json'):
                fp = os.path.join(BACKUP_DIR, fn)
                if datetime.fromtimestamp(os.path.getmtime(fp)) < cutoff:
                    os.remove(fp)
                    removed += 1
        if removed:
            log(f'🗑️  Removed {removed} old backup files')
    except Exception as e:
        log(f'⚠️  Error purging old backups: {e}')


def get_latest_backup():
    """
    Parse and return the most recent portfolio backup file, or None.
    Handles both wrapped {data: {...}} and flat backup formats.
    """
    try:
        ensure_backup_dir()
        json_files = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.json')]
        if not json_files:
            return None
        newest = max(json_files, key=lambda f: os.path.getmtime(os.path.join(BACKUP_DIR, f)))
        raw    = json.load(open(os.path.join(BACKUP_DIR, newest)))
        return raw.get('data', raw)
    except Exception as e:
        log(f'⚠️  Error reading latest backup: {e}')
        return None


def get_portfolio_coin_ids():
    """
    Extract the list of tracked CoinGecko coin IDs from the latest backup.
    Skips custom and traditional (non-crypto) assets.
    """
    backup = get_latest_backup()
    if not backup:
        return []
    coin_ids = set()
    for holding in backup.get('holdings', []):
        if holding.get('isCustom') or holding.get('isTraditional'):
            continue
        cid = holding.get('coinId', '')
        if cid and not cid.startswith(('traditional_', 'custom_')):
            coin_ids.add(cid)
    return sorted(coin_ids)


# ─────────────────────────────────────────────────────────────────────────────
# SHARED WATCHLIST
# ─────────────────────────────────────────────────────────────────────────────

def load_watchlist():
    """Load the shared watchlist from disk. Returns a list of uppercase symbols."""
    if os.path.exists(WATCHLIST_FILE):
        try:
            return json.load(open(WATCHLIST_FILE))
        except Exception:
            pass
    return []


def save_watchlist(symbols):
    """
    Persist the shared watchlist to disk.
    `symbols` should be uppercase coin symbols e.g. ['BTC', 'ETH', 'SOL'].
    """
    try:
        json.dump(symbols, open(WATCHLIST_FILE, 'w'), indent=2)
        return True
    except Exception as e:
        log(f'⚠️  Error saving watchlist: {e}')
        return False


# ─────────────────────────────────────────────────────────────────────────────
# COINGECKO DATA FETCHERS
# ─────────────────────────────────────────────────────────────────────────────

def fetch_portfolio_prices(coin_ids=None):
    """
    Fetch AUD prices for tracked coins from CoinGecko /simple/price.
    If coin_ids is None, reloads the tracked coins list from disk.
    Updates price_cache in-place and writes a DB snapshot on success.
    """
    global price_cache, price_cache_updated, TRACKED_COINS
    try:
        if coin_ids is None:
            TRACKED_COINS = load_tracked_coins()
            coin_ids      = TRACKED_COINS
        log(f'Fetching prices for {len(coin_ids)} coins...')
        url = (
            f"{PRICE_ENDPOINT}"
            f"?ids={','.join(coin_ids)}"
            f"&vs_currencies=aud"
            f"&include_24hr_change=true"
        )
        req = urllib.request.Request(url, headers=coingecko_headers())
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        for coin_id, coin_data in data.items():
            if 'aud' in coin_data:
                price_cache[coin_id] = {
                    'aud':            coin_data['aud'],
                    'aud_24h_change': coin_data.get('aud_24h_change', 0),
                }
        price_cache_updated = datetime.now()
        log(f'✅ Updated {len(data)} prices')
        save_all_price_snapshots()
        return True
    except urllib.error.URLError as e:
        log(f'⚠️  Network error fetching prices: {e}')
        return False
    except Exception as e:
        log(f'⚠️  Error fetching prices: {e}')
        return False


def fetch_markets():
    """
    Fetch top-250 coins from CoinGecko /coins/markets for the scanner.
    Returns price, market cap, volume, and 1h/24h/7d/30d % changes.
    """
    global markets_cache, markets_cache_updated
    try:
        url = (
            f'{COINGECKO_BASE}/coins/markets'
            '?vs_currency=aud'
            '&order=market_cap_desc'
            '&per_page=250'
            '&page=1'
            '&sparkline=false'
            '&price_change_percentage=1h%2C24h%2C7d%2C30d'
        )
        req = urllib.request.Request(url, headers=coingecko_headers())
        with urllib.request.urlopen(req, timeout=15) as resp:
            markets_cache = json.loads(resp.read().decode())
        markets_cache_updated = datetime.now()
        log(f'📈 Markets updated ({len(markets_cache)} coins)')
        return True
    except urllib.error.HTTPError as e:
        log(f'⚠️  Markets HTTP {e.code}{"  — rate limited" if e.code == 429 else ""}')
        return False
    except Exception as e:
        log(f'⚠️  Markets fetch error: {e}')
        return False


def fetch_global_stats():
    """Fetch global market stats (total market cap, BTC dominance, DeFi cap) from CoinGecko."""
    global global_cache, global_cache_updated
    try:
        req = urllib.request.Request(f'{COINGECKO_BASE}/global', headers=coingecko_headers())
        with urllib.request.urlopen(req, timeout=10) as resp:
            global_cache = json.loads(resp.read().decode()).get('data', {})
        global_cache_updated = datetime.now()
        log('🌐 Global stats updated')
        return True
    except Exception as e:
        log(f'⚠️  Global stats error: {e}')
        return False


def fetch_trending_coins():
    """Fetch currently trending coins from CoinGecko /search/trending."""
    try:
        req = urllib.request.Request(f'{COINGECKO_BASE}/search/trending', headers=coingecko_headers())
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        log(f'⚠️  Trending fetch error: {e}')
        return None


def fetch_categories():
    """Fetch coin sector categories from CoinGecko, ordered by market cap."""
    try:
        url = f'{COINGECKO_BASE}/coins/categories?order=market_cap_desc'
        req = urllib.request.Request(url, headers=coingecko_headers())
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        log(f'⚠️  Categories fetch error: {e}')
        return None


# ─────────────────────────────────────────────────────────────────────────────
# NEWS RSS PARSER
# ─────────────────────────────────────────────────────────────────────────────

def parse_rss_feed(url):
    """
    Fetch and parse a single RSS feed URL.
    Returns a list of article dicts: title, url, published_at, source, sentiment scores.
    Handles feeds that contain unescaped & characters (common in news URLs/titles).
    """
    req = urllib.request.Request(url, headers=RSS_HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()

    # Sanitise bare & characters that break strict XML parsing
    text = raw.decode('utf-8', errors='replace')
    text = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', text)

    root    = ET.fromstring(text.encode('utf-8'))
    channel = root.find('channel')
    if channel is None:
        return []

    title_el    = channel.find('title')
    source_name = title_el.text.strip() if title_el is not None and title_el.text else ''

    articles = []
    for item in channel.findall('item')[:20]:

        def _text(tag):
            el = item.find(tag)
            return el.text.strip() if el is not None and el.text else ''

        title = _text('title')
        link  = _text('link') or _text('guid')
        pub   = _text('pubDate')

        try:
            pub_iso = parsedate_to_datetime(pub).isoformat()
        except Exception:
            pub_iso = pub

        title_lower   = title.lower()
        bullish_score = sum(1 for k in BULLISH_KEYWORDS if k in title_lower)
        bearish_score = sum(1 for k in BEARISH_KEYWORDS if k in title_lower)

        articles.append({
            'title':          title,
            'url':            link,
            'published_at':   pub_iso,
            'source':         {'title': source_name},
            'currencies':     [],
            'votes_positive': bullish_score,
            'votes_negative': bearish_score,
        })

    return articles


def fetch_news(filter_key=''):
    """
    Fetch news articles from the feeds matching filter_key.
    Merges results from all feeds, deduplicates by title, returns newest-first.
    """
    feed_urls    = NEWS_FEEDS.get(filter_key, NEWS_FEEDS[''])
    all_articles = []

    for url in feed_urls:
        try:
            all_articles.extend(parse_rss_feed(url))
        except Exception as e:
            log(f'⚠️  Feed error ({url}): {e}')

    seen   = set()
    unique = []
    for article in sorted(all_articles, key=lambda a: a['published_at'], reverse=True):
        if article['title'] and article['title'] not in seen:
            seen.add(article['title'])
            unique.append(article)

    return unique[:30]


# ─────────────────────────────────────────────────────────────────────────────
# BACKGROUND THREADS
# ─────────────────────────────────────────────────────────────────────────────

def _price_updater_loop():
    """Refresh portfolio prices every PRICE_INTERVAL seconds."""
    while True:
        time.sleep(PRICE_INTERVAL)
        fetch_portfolio_prices()


def _markets_updater_loop():
    """Refresh scanner market data + global stats every MARKETS_INTERVAL seconds."""
    while True:
        time.sleep(MARKETS_INTERVAL)
        fetch_markets()
        time.sleep(5)       # stagger to avoid consecutive rate-limit hits
        fetch_global_stats()


def _daily_cleanup_loop():
    """Run daily housekeeping: purge old backups and old DB records."""
    while True:
        time.sleep(86_400)  # 24 hours
        purge_old_backups()
        purge_old_price_data()


# ─────────────────────────────────────────────────────────────────────────────
# HTTP REQUEST HANDLER
# ─────────────────────────────────────────────────────────────────────────────

class RJTVenturesHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%d/%b/%Y %H:%M:%S')}] {fmt % args}")

    # ── OPTIONS — CORS preflight ─────────────────────────────────────────────

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    # ── GET ──────────────────────────────────────────────────────────────────

    def do_GET(self):
        parsed       = urllib.parse.urlparse(self.path)
        path         = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        # HTML pages
        if path in ('/', '/index.html'):
            serve_html_file(self, 'tracker.html')

        elif path in ('/scanner', '/scanner.html'):
            serve_html_file(self, 'crypto-scanner.html')

        # Portfolio prices with 24h change calculated from local DB
        elif path == '/api/prices':
            log('📊 /api/prices requested')
            enhanced = {
                cid: {'aud': data['aud'], 'aud_24h_change': calculate_24h_change(cid)}
                for cid, data in price_cache.items()
            }
            send_json(self, {
                'status':        'ok',
                'prices':        enhanced,
                'last_update':   price_cache_updated.isoformat() if price_cache_updated else None,
                'coins_tracked': len(enhanced),
            })

        # Full price history for a single coin
        elif path.startswith('/api/price-history/'):
            coin_id = path.split('/api/price-history/')[-1].split('?')[0]
            days    = int(query_params.get('days', [30])[0])
            history = get_price_history(coin_id, days)
            stats   = {}
            if history:
                prices      = [h['price'] for h in history]
                first_price = prices[0]
                last_price  = prices[-1]
                stats = {
                    'current':     last_price,
                    'highest':     max(prices),
                    'lowest':      min(prices),
                    'average':     sum(prices) / len(prices),
                    'change_pct':  ((last_price - first_price) / first_price * 100) if first_price > 0 else 0,
                    'data_points': len(prices),
                }
            send_json(self, {'status': 'ok', 'coin_id': coin_id, 'history': history, 'stats': stats})

        # Server health and cache status
        elif path == '/api/status':
            send_json(self, {
                'status':                   'ok',
                'server':                   'RJTVentures Crypto Server',
                'version':                  '3.1',
                'portfolio_coins':          len(price_cache),
                'price_cache_updated':      price_cache_updated.isoformat() if price_cache_updated else None,
                'price_interval_seconds':   PRICE_INTERVAL,
                'markets_coins':            len(markets_cache),
                'markets_cache_updated':    markets_cache_updated.isoformat() if markets_cache_updated else None,
                'markets_interval_seconds': MARKETS_INTERVAL,
            })

        # List of backup files
        elif path == '/api/backup/list':
            try:
                ensure_backup_dir()
                backups = [
                    {
                        'filename': fn,
                        'size':     os.stat(os.path.join(BACKUP_DIR, fn)).st_size,
                        'date':     datetime.fromtimestamp(
                                        os.path.getmtime(os.path.join(BACKUP_DIR, fn))
                                    ).isoformat(),
                    }
                    for fn in os.listdir(BACKUP_DIR) if fn.endswith('.json')
                ]
                send_json(self, {'status': 'ok', 'backups': backups})
            except Exception as e:
                send_json(self, {'status': 'error', 'message': str(e)}, 500)

        # Download a specific backup file
        elif path.startswith('/api/backup/download/'):
            filename = path.split('/api/backup/download/')[-1]
            filepath = os.path.join(BACKUP_DIR, filename)
            if not os.path.exists(filepath):
                self.send_error(404, 'Backup file not found')
                return
            try:
                with open(filepath, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_error(500, str(e))

        # Top-250 market data for the scanner (cached)
        elif path == '/api/markets':
            if not markets_cache:
                log('📈 First /api/markets request — fetching now...')
                fetch_markets()
            send_json(self, {
                'status':      'ok',
                'coins':       markets_cache,
                'last_update': markets_cache_updated.isoformat() if markets_cache_updated else None,
                'count':       len(markets_cache),
            })

        # Global market stats (total cap, BTC dominance, DeFi)
        elif path == '/api/global':
            if not global_cache:
                fetch_global_stats()
            send_json(self, {
                'status':      'ok',
                'data':        global_cache,
                'last_update': global_cache_updated.isoformat() if global_cache_updated else None,
            })

        # Trending coins (live, not cached)
        elif path == '/api/trending':
            data = fetch_trending_coins()
            if data:
                send_json(self, {'status': 'ok', 'data': data})
            else:
                send_json(self, {'status': 'error', 'message': 'Could not fetch trending'}, 503)

        # Coin sector categories (live, not cached)
        elif path == '/api/categories':
            data = fetch_categories()
            if data:
                send_json(self, {'status': 'ok', 'data': data})
            else:
                send_json(self, {'status': 'error', 'message': 'Could not fetch categories'}, 503)

        # Portfolio coin IDs from the latest backup
        elif path == '/api/portfolio':
            backup      = get_latest_backup()
            coin_ids    = get_portfolio_coin_ids()
            backup_date = backup.get('exportDate') if backup else None
            send_json(self, {
                'status':      'ok',
                'coin_ids':    coin_ids,
                'count':       len(coin_ids),
                'backup_date': backup_date,
            })

        # Shared watchlist (read)
        elif path == '/api/watchlist':
            send_json(self, {'status': 'ok', 'watchlist': load_watchlist()})

        # Chart data from local DB, formatted for Chart.js
        elif path.startswith('/api/chart/'):
            coin_id    = path.split('/api/chart/')[-1].split('?')[0]
            days       = int(query_params.get('days', [30])[0])
            history    = get_price_history(coin_id, days)
            chart_data = [
                [int(datetime.fromisoformat(h['timestamp']).timestamp() * 1000), h['price']]
                for h in history
            ]
            send_json(self, {
                'status':  'ok',
                'coin_id': coin_id,
                'days':    days,
                'prices':  chart_data,
                'points':  len(chart_data),
                'source':  'local_db',
            })

        # Fear & Greed Index — proxied from alternative.me (avoids browser CORS)
        elif path in ('/api/feargreed', '/api/feargreed_proxy'):
            try:
                req = urllib.request.Request(
                    'https://api.alternative.me/fng/?limit=1',
                    headers={'User-Agent': 'RJTVentures/3.1'}
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    entry = json.loads(resp.read())['data'][0]
                send_json(self, {
                    'status': 'ok',
                    'value':  int(entry['value']),
                    'label':  entry['value_classification'],
                })
            except Exception as e:
                send_json(self, {'status': 'error', 'message': str(e)}, 502)

        # Crypto news from CoinDesk + Cointelegraph RSS feeds
        elif path.startswith('/api/news'):
            filter_key = query_params.get('filter', [''])[0]
            try:
                articles = fetch_news(filter_key)
                log(f'📰 News served ({len(articles)} articles, filter="{filter_key or "all"}")')
                send_json(self, {'status': 'ok', 'articles': articles})
            except Exception as e:
                log(f'⚠️  News error: {e}')
                send_json(self, {'status': 'error', 'message': str(e)}, 502)

        # DCA plans from the latest backup
        elif path == '/api/dca_plans':
            backup = get_latest_backup()
            if not backup:
                send_json(self, {'status': 'ok', 'plans': [], 'message': 'No backup found yet'})
                return
            plans = [
                {
                    'symbol':             p.get('symbol', ''),
                    'displayName':        p.get('displayName', p.get('symbol', '')),
                    'amount':             p.get('amount', 0),
                    'frequencyDays':      p.get('frequencyDays', 14),
                    'frequencyText':      p.get('frequencyText', 'Fortnightly'),
                    'months':             p.get('months', 12),
                    'totalPurchases':     p.get('totalPurchases', 0),
                    'completedPurchases': p.get('completedPurchases', 0),
                    'nextPurchaseDate':   p.get('nextPurchaseDate'),
                    'active':             p.get('active', True),
                }
                for p in backup.get('dcaPlans', [])
            ]
            send_json(self, {'status': 'ok', 'plans': plans})

        else:
            self.send_error(404)

    # ── POST ─────────────────────────────────────────────────────────────────

    def do_POST(self):
        path = self.path
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))

        # Request fresh prices for a specific list of coins
        if path == '/api/prices':
            try:
                requested_coins = json.loads(body).get('coins', [])
                log(f'📥 Price request for {len(requested_coins)} coins')
                fetch_portfolio_prices(requested_coins)
                send_json(self, {
                    'status':        'ok',
                    'prices':        price_cache,
                    'last_update':   price_cache_updated.isoformat() if price_cache_updated else None,
                    'coins_tracked': len(price_cache),
                })
            except Exception as e:
                log(f'⚠️  Price POST error: {e}')
                self.send_error(500, str(e))

        # Add a new coin to the tracked list
        elif path == '/api/coins/add':
            try:
                coin_id = json.loads(body).get('coin_id', '').lower().strip()
                if not coin_id:
                    self.send_error(400, 'Missing coin_id')
                    return
                added = add_tracked_coin(coin_id)
                if added:
                    fetch_portfolio_prices()
                send_json(self, {
                    'status':      'ok',
                    'coin_id':     coin_id,
                    'message':     f'Added {coin_id}' if added else f'{coin_id} already tracked',
                    'total_coins': len(load_tracked_coins()),
                })
            except Exception as e:
                self.send_error(500, str(e))

        # Save a portfolio backup sent from the tracker
        elif path == '/api/backup/save':
            try:
                ensure_backup_dir()
                filename = f"portfolio-backup-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
                filepath = os.path.join(BACKUP_DIR, filename)
                with open(filepath, 'wb') as f:
                    f.write(body)
                log(f'💾 Backup saved: {filename}')
                send_json(self, {
                    'status':   'ok',
                    'filename': filename,
                    'size':     len(body),
                    'message':  'Backup saved successfully',
                })
            except Exception as e:
                self.send_error(500, str(e))

        # Update the shared watchlist
        elif path == '/api/watchlist':
            try:
                incoming = json.loads(body).get('watchlist', [])
                if not isinstance(incoming, list):
                    self.send_error(400, 'watchlist must be an array')
                    return
                # Normalise to uppercase, deduplicate, preserve order
                symbols = list(dict.fromkeys(
                    s.upper().strip() for s in incoming if isinstance(s, str) and s.strip()
                ))
                if save_watchlist(symbols):
                    log(f'⭐ Watchlist saved ({len(symbols)} coins)')
                    send_json(self, {'status': 'ok', 'watchlist': symbols, 'count': len(symbols)})
                else:
                    self.send_error(500, 'Failed to save watchlist')
            except Exception as e:
                self.send_error(500, str(e))

        else:
            self.send_error(404)


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print('=' * 70)
    print('  RJTVentures Crypto Server  v3.1')
    print('  Tracker + Scanner + News + Fear & Greed')
    print('=' * 70)
    print()
    print('Endpoints:')
    print('  GET  /                   → tracker.html')
    print('  GET  /scanner            → crypto-scanner.html')
    print('  GET  /api/prices         → portfolio prices (AUD + 24h change)')
    print('  GET  /api/markets        → top-250 market data (scanner)')
    print('  GET  /api/global         → global market cap + BTC dominance')
    print('  GET  /api/feargreed      → Fear & Greed Index')
    print('  GET  /api/news           → crypto news (?filter=bitcoin|markets|altcoins|defi)')
    print('  GET  /api/dca_plans      → DCA plans from latest backup')
    print('  GET  /api/watchlist      → shared watchlist')
    print('  GET  /api/portfolio      → portfolio coin IDs from backup')
    print('  GET  /api/trending       → trending coins')
    print('  GET  /api/categories     → coin sectors')
    print('  POST /api/backup/save    → save portfolio backup')
    print('  POST /api/watchlist      → update shared watchlist')
    print()
    print('Tip: create coingecko_key.txt with your Demo API key for higher rate limits.')
    print()

    ensure_backup_dir()
    init_price_db()

    print('Fetching initial data...')
    if fetch_portfolio_prices():
        print(f'  ✅ Portfolio prices ({len(price_cache)} coins)')
    else:
        print('  ⚠️  Portfolio price fetch failed — will retry in background')

    if fetch_markets():
        print(f'  ✅ Market data ({len(markets_cache)} coins)')
    else:
        print('  ⚠️  Market data fetch failed — will retry in background')

    if fetch_global_stats():
        print('  ✅ Global stats')
    else:
        print('  ⚠️  Global stats fetch failed — will retry in background')

    portfolio_coins = get_portfolio_coin_ids()
    if portfolio_coins:
        preview = ', '.join(portfolio_coins[:6]) + ('...' if len(portfolio_coins) > 6 else '')
        print(f'  ✅ Portfolio backup: {len(portfolio_coins)} coins ({preview})')
    else:
        print('  ⚠️  No portfolio backup yet — will populate after first tracker save')

    print()
    print('Starting background threads...')
    threading.Thread(target=_price_updater_loop,   daemon=True, name='PriceUpdater').start()
    threading.Thread(target=_markets_updater_loop, daemon=True, name='MarketsUpdater').start()
    threading.Thread(target=_daily_cleanup_loop,   daemon=True, name='DailyCleanup').start()
    print('  ✅ Price updater    (every 5 min)')
    print('  ✅ Markets updater  (every 2 min)')
    print('  ✅ Daily cleanup    (every 24 hr)')
    print()

    local_ip = get_local_ip()
    server   = HTTPServer(('', PORT), RJTVenturesHandler)

    print('=' * 70)
    print('  SERVER READY')
    print('=' * 70)
    print(f'  Tracker:   http://localhost:{PORT}')
    print(f'  Scanner:   http://localhost:{PORT}/scanner')
    print(f'  Network:   http://{local_ip}:{PORT}')
    print()
    print(f'  Backups:   {os.path.abspath(BACKUP_DIR)}/')
    print(f'  Database:  {os.path.abspath(PRICE_DB)}')
    print(f'  Watchlist: {os.path.abspath(WATCHLIST_FILE)}')
    print()
    print('  Ctrl+C to stop')
    print('=' * 70)
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print('Server stopped.')


if __name__ == '__main__':
    main()
