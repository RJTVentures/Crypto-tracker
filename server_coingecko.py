#!/usr/bin/env python3
"""
Crypto Tracker Server - CoinGecko Edition
Runs on your old Mac to provide CoinGecko prices without CORS issues
Now with automatic backup functionality and price history database!

SWITCHED FROM COINSPOT TO COINGECKO:
- CoinGecko has 10,000+ coins (vs CoinSpot's 16)
- All your coins will work automatically
- Free API, no rate limits for basic usage
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import threading
import time
import os
import shutil
import sqlite3

# Configuration
PORT = 8080
COINGECKO_API = 'https://api.coingecko.com/api/v3/simple/price'
UPDATE_INTERVAL = 300  # 5 minutes in seconds
BACKUP_DIR = 'backups'
KEEP_BACKUPS_DAYS = 30
PRICE_DB = 'price_history.db'
COINS_FILE = 'tracked_coins.json'  # File to store coin list

# Global cache for prices
price_cache = {}
last_update = None

# Default coins to track
DEFAULT_COINS = [
    'bitcoin', 'ethereum', 'cardano', 'ripple', 'solana', 'dogecoin',
    'litecoin', 'tron', 'stellar', 'eos', 'power-ledger', 'redfox-labs-2',
    'neo', 'gas', 'tether', 'rchain', 'aave', 'chainlink', 'the-graph',
    'hedera-hashgraph', 'fetch-ai'
]

def load_coins_to_fetch():
    """Load coins list from file, or use defaults"""
    if os.path.exists(COINS_FILE):
        try:
            with open(COINS_FILE, 'r') as f:
                coins = json.load(f)
                return coins if isinstance(coins, list) else DEFAULT_COINS
        except:
            return DEFAULT_COINS
    else:
        # Create file with defaults
        save_coins_to_fetch(DEFAULT_COINS)
        return DEFAULT_COINS

def save_coins_to_fetch(coins):
    """Save coins list to file"""
    try:
        with open(COINS_FILE, 'w') as f:
            json.dump(coins, f, indent=2)
        return True
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Error saving coins list: {e}")
        return False

def add_coin_to_fetch(coin_id):
    """Add a new coin to the tracking list"""
    coins = load_coins_to_fetch()
    coin_id = coin_id.lower().strip()
    
    if coin_id not in coins:
        coins.append(coin_id)
        if save_coins_to_fetch(coins):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ➕ Added {coin_id} to tracking list ({len(coins)} total)")
            return True
    return False

# Load coins on startup
COINS_TO_FETCH = load_coins_to_fetch()

def init_price_database():
    """Initialize the price history database"""
    conn = sqlite3.connect(PRICE_DB)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            coin_id TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp TEXT NOT NULL,
            PRIMARY KEY (coin_id, timestamp)
        )
    ''')
    
    c.execute('''
        CREATE INDEX IF NOT EXISTS idx_coin_timestamp 
        ON price_history(coin_id, timestamp)
    ''')
    
    conn.commit()
    conn.close()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 💾 Price history database initialized")

def save_price_to_database(coin_id, price):
    """Save a single price point to the database"""
    try:
        conn = sqlite3.connect(PRICE_DB)
        c = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        c.execute(
            'INSERT OR REPLACE INTO price_history (coin_id, price, timestamp) VALUES (?, ?, ?)',
            (coin_id, price, timestamp)
        )
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Error saving price for {coin_id}: {e}")

def save_all_prices_to_database():
    """Save all current prices to the database"""
    if not price_cache:
        return
    
    saved_count = 0
    for coin_id, price_data in price_cache.items():
        # Handle both dict and legacy float formats
        if isinstance(price_data, dict):
            price = price_data.get('aud', 0)
        else:
            price = price_data
            
        if price and price > 0:
            try:
                save_price_to_database(coin_id, price)
                saved_count += 1
            except Exception as e:
                continue
    
    if saved_count > 0:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 💾 Saved {saved_count} prices to database")

def cleanup_old_price_data(days=365):
    """Remove price data older than specified days"""
    try:
        conn = sqlite3.connect(PRICE_DB)
        c = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        c.execute('DELETE FROM price_history WHERE timestamp < ?', (cutoff_date,))
        deleted_count = c.rowcount
        
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🗑️  Cleaned up {deleted_count} old price records")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Error cleaning old price data: {e}")

def get_price_history_from_db(coin_id, days=30):
    """Retrieve price history from database"""
    try:
        conn = sqlite3.connect(PRICE_DB)
        c = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        c.execute(
            'SELECT timestamp, price FROM price_history WHERE coin_id = ? AND timestamp >= ? ORDER BY timestamp ASC',
            (coin_id, cutoff_date)
        )
        
        results = c.fetchall()
        conn.close()
        
        return [{'timestamp': row[0], 'price': row[1]} for row in results]
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Error fetching price history: {e}")
        return []

def ensure_backup_directory():
    """Create backup directory if it doesn't exist"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📁 Created backup directory")

def cleanup_old_backups():
    """Remove backups older than KEEP_BACKUPS_DAYS"""
    try:
        cutoff_date = datetime.now() - timedelta(days=KEEP_BACKUPS_DAYS)
        removed_count = 0
        
        for filename in os.listdir(BACKUP_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(BACKUP_DIR, filename)
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_time < cutoff_date:
                    os.remove(filepath)
                    removed_count += 1
        
        if removed_count > 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🗑️  Cleaned up {removed_count} old backups")
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Error cleaning backups: {e}")

def fetch_coingecko_prices():
    """Fetch latest prices from CoinGecko API"""
    global price_cache, last_update, COINS_TO_FETCH
    
    try:
        # Reload coins list in case it was updated
        COINS_TO_FETCH = load_coins_to_fetch()
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching prices from CoinGecko...")
        
        # Build API URL
        ids = ','.join(COINS_TO_FETCH)
        url = f"{COINGECKO_API}?ids={ids}&vs_currencies=aud&include_24hr_change=true"
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'CryptoTracker/2.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            # Convert CoinGecko format with 24h change
            new_cache = {}
            for coin_id, coin_data in data.items():
                new_cache[coin_id] = {
                    'aud': coin_data.get('aud', 0),
                    'aud_24h_change': coin_data.get('aud_24h_change', 0)
                }
            
            price_cache = new_cache
            last_update = datetime.now().isoformat()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Successfully fetched {len(price_cache)} coin prices")
            
            # Save prices to database
            save_all_prices_to_database()
            
            return True
                
    except urllib.error.URLError as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error fetching prices: {e}")
        return False

def price_updater():
    """Background thread to update prices every 5 minutes"""
    while True:
        fetch_coingecko_prices()
        time.sleep(UPDATE_INTERVAL)

def daily_cleanup():
    """Background thread for daily cleanup tasks"""
    while True:
        time.sleep(86400)  # 24 hours
        cleanup_old_price_data(365)
        cleanup_old_backups()

def get_local_ip():
    """Get the local IP address"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

class CryptoTrackerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Simplified logging"""
        print(f"[{self.log_date_time_string()}] {format % args}")
    
    def do_GET(self):
        # API endpoint to get current prices
        if self.path == '/api/prices':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Return prices in the format tracker expects
            formatted_prices = {}
            for coin_id, price_data in price_cache.items():
                if isinstance(price_data, dict):
                    formatted_prices[coin_id] = price_data
                else:
                    # Legacy format compatibility
                    formatted_prices[coin_id] = {
                        'aud': price_data,
                        'aud_24h_change': 0
                    }
            
            response = {
                'status': 'ok',
                'prices': formatted_prices,
                'last_update': last_update
            }
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        # API endpoint to get price history from database
        elif self.path.startswith('/api/price-history/'):
            coin_id = self.path.split('/api/price-history/')[-1].split('?')[0]
            
            # Parse query parameters
            query_params = {}
            if '?' in self.path:
                query_string = self.path.split('?')[1]
                for param in query_string.split('&'):
                    if '=' in param:
                        key, value = param.split('=')
                        query_params[key] = value
            
            days = int(query_params.get('days', '30'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                price_history = get_price_history_from_db(coin_id, days)
                
                # Calculate statistics
                stats = {}
                if len(price_history) > 0:
                    prices = [p['price'] for p in price_history]
                    current_price = prices[-1]
                    first_price = prices[0]
                    
                    stats = {
                        'current': current_price,
                        'highest': max(prices),
                        'lowest': min(prices),
                        'average': sum(prices) / len(prices),
                        'change': ((current_price - first_price) / first_price * 100) if first_price > 0 else 0,
                        'data_points': len(prices)
                    }
                
                response = {
                    'status': 'ok',
                    'coin_id': coin_id,
                    'days': days,
                    'history': price_history,
                    'stats': stats
                }
            
            except Exception as e:
                response = {
                    'status': 'error',
                    'message': str(e)
                }
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        # API endpoint to list backups
        elif self.path == '/api/backups/list':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                ensure_backup_directory()
                backups = []
                
                if os.path.exists(BACKUP_DIR):
                    for filename in sorted(os.listdir(BACKUP_DIR), reverse=True):
                        if filename.endswith('.json'):
                            filepath = os.path.join(BACKUP_DIR, filename)
                            file_stat = os.stat(filepath)
                            
                            backups.append({
                                'filename': filename,
                                'size': file_stat.st_size,
                                'date': datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                            })
                
                response = {
                    'status': 'ok',
                    'backups': backups
                }
                
            except Exception as e:
                response = {
                    'status': 'error',
                    'message': str(e)
                }
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        # API endpoint to download a specific backup
        elif self.path.startswith('/api/backup/download/'):
            filename = self.path.split('/api/backup/download/')[-1]
            filepath = os.path.join(BACKUP_DIR, filename)
            
            try:
                if not os.path.exists(filepath):
                    self.send_error(404, 'Backup file not found')
                    return
                
                with open(filepath, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(f.read())
                
            except Exception as e:
                self.send_error(500, str(e))
            
            return
        
        # Serve tracker HTML
        elif self.path == '/' or self.path == '/index.html':
            try:
                with open('tracker.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, 'tracker.html not found')
            return
        
        self.send_error(404)
    
    def do_POST(self):
        # API endpoint to add a coin to tracking list
        if self.path == '/api/coins/add':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                coin_id = data.get('coin_id', '').lower().strip()
                
                if not coin_id:
                    self.send_error(400, 'Missing coin_id')
                    return
                
                # Add coin to tracking list
                if add_coin_to_fetch(coin_id):
                    # Immediately fetch price for new coin
                    fetch_coingecko_prices()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    response = {
                        'status': 'ok',
                        'coin_id': coin_id,
                        'message': f'Added {coin_id} to tracking list',
                        'total_coins': len(load_coins_to_fetch())
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    response = {
                        'status': 'ok',
                        'coin_id': coin_id,
                        'message': f'{coin_id} already tracked'
                    }
                    self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_error(500, f'Failed to add coin: {str(e)}')
            
            return
        
        # API endpoint to save backup
        elif self.path == '/api/backup/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                ensure_backup_directory()
                
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                filename = f'portfolio-backup-{timestamp}.json'
                filepath = os.path.join(BACKUP_DIR, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(post_data)
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 💾 Backup saved: {filename}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'ok',
                    'filename': filename,
                    'message': 'Backup saved successfully'
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_error(500, f'Backup failed: {str(e)}')
            
            return
        
        self.send_error(404)
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    """Main function to start the server"""
    
    print("=" * 70)
    print("  CRYPTO TRACKER SERVER - CoinGecko Edition")
    print("  with Auto-Backup & Price History Database")
    print("=" * 70)
    print()
    print("🔄 SWITCHED FROM COINSPOT TO COINGECKO")
    print("   • 10,000+ coins available (vs CoinSpot's 16)")
    print("   • All your coins now supported!")
    print()
    
    ensure_backup_directory()
    init_price_database()
    
    print("Fetching initial prices from CoinGecko...")
    if fetch_coingecko_prices():
        print(f"✅ Initial price fetch successful ({len(price_cache)} coins)")
    else:
        print("⚠️  Initial price fetch failed, will retry in background")
    
    print()
    
    print("Starting background price updater...")
    updater_thread = threading.Thread(target=price_updater, daemon=True)
    updater_thread.start()
    print("✅ Background updater started")
    
    print()
    
    print("Starting daily cleanup thread...")
    cleanup_thread = threading.Thread(target=daily_cleanup, daemon=True)
    cleanup_thread.start()
    print("✅ Daily cleanup thread started")
    
    print()
    
    local_ip = get_local_ip()
    backup_path = os.path.abspath(BACKUP_DIR)
    db_path = os.path.abspath(PRICE_DB)
    
    server = HTTPServer(('', PORT), CryptoTrackerHandler)
    
    print("=" * 70)
    print("  SERVER READY!")
    print("=" * 70)
    print()
    print(f"📡 Server running on port {PORT}")
    print()
    print("🌐 Access from:")
    print(f"   • This Mac:      http://localhost:{PORT}")
    print(f"   • Other devices: http://{local_ip}:{PORT}")
    print()
    print("🔄 Prices update every 5 minutes")
    print()
    print("💾 Automatic Backups:")
    print(f"   • Location: {backup_path}/")
    print(f"   • Retention: {KEEP_BACKUPS_DAYS} days")
    print()
    print("📊 Price History Database:")
    print(f"   • Database: {db_path}")
    print(f"   • Collection: Every 5 minutes")
    print(f"   • Retention: 365 days")
    print()
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("  SERVER STOPPED")
        print("=" * 70)
        print("✅ Server shut down cleanly")
        print()

if __name__ == '__main__':
    main()
