# Changelog

All notable changes to RJTVentures Crypto Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-04-22

### Fixed
- Updated Polygon coin ID from `polygon` to `polygon-ecosystem-token` to match CoinGecko's rebrand from MATIC to POL
- Fixed watchlist prices showing "Loading..." indefinitely
- Added missing `/api/backups/list` endpoint for browsing server backups
- Added `/api/backup/download/{filename}` endpoint for downloading specific backups
- Fixed `fetchPrices()` to include watchlist coins when fetching prices
- All 404 errors resolved

### Changed
- Server now correctly fetches 24 coins including Polygon
- Coin search mapping updated to support "polygon", "matic", and "pol" symbols
- Version indicator added to page header for easier troubleshooting

## [1.2.0] - 2026-04-22

### Fixed
- Watchlist prices now update correctly with auto-refresh
- `fetchPrices()` now fetches prices for both Holdings and Watchlist coins
- Price cache properly includes watchlist coins

### Changed
- Improved price fetching logic to support watchlist-only coins

## [1.1.0] - 2026-04-22

### Fixed
- Removed unnecessary loading message from watchlist modal (search is instant)
- Browser caching issues resolved

### Added
- Cache-busting meta tags to force browser reload on updates
- Version number in page title and header

## [1.0.0] - 2026-04-20

### Added
- Initial public release
- Full portfolio tracking system
- Watchlist feature for tracking coins before purchase
- Transaction history with complete audit trail
- Real-time price updates every 5 minutes
- Price history charts with 365-day retention
- Server-side backup system with 30-day retention
- Banker green/gold professional theme
- Support for 10,000+ cryptocurrencies via CoinGecko API
- LocalStorage for client-side data persistence
- SQLite database for price history
- Export/Import functionality
- Multi-source holdings (Hardware Wallet, CoinSpot, etc.)
- Cost basis and profit/loss calculations
- 24-hour performance tracking
- Responsive design for mobile and desktop
- Self-hosted with no external dependencies
- Complete privacy - all data stored locally

### Technical Details
- Python 3.8+ server
- Single-page HTML/CSS/JavaScript frontend
- Chart.js for data visualization
- CoinGecko API integration
- SQLite for price history
- Automatic backup management
- CORS handling for local development

---

## Future Releases

### [2.0.0] - Planned
- Tabbed interface for cleaner navigation
- Dashboard summary page
- Improved mobile experience
- Performance optimizations

### Under Consideration
- Price alerts and notifications
- Multi-currency support (USD, EUR, etc.)
- Portfolio comparison tools
- Tax reporting features
- Docker containerization
- Mobile app version
- DeFi protocol integration
- NFT tracking support
