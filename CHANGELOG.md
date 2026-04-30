[CHANGELOG.md](https://github.com/user-attachments/files/27228785/CHANGELOG.md)
# Changelog

All notable changes to RJTVentures Crypto Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-04-30

### 🎉 Feature Release - Tools, Planning & Mobile Support

### Added
- **DCA Calculator**: Dollar Cost Averaging calculator with historical price simulation
  - Select any coin from holdings
  - Configure investment amount, frequency (weekly/fortnightly/monthly), and duration
  - Simulates purchases using historical price data from database
  - Shows total invested, number of purchases, average buy price, coins accumulated
  - Displays current value and profit/loss with percentage
  
- **DCA Planner**: Full DCA planning and execution system
  - Save DCA plans with complete configuration
  - Track progress with visual progress bars
  - Execute purchase button pre-fills Buy modal
  - Next purchase date with countdown/overdue indicators
  - Plans start on first purchase (not creation date)
  - View purchase history
  - Pause/Resume/Delete plans
  - Automatic completion notifications
  
- **Tax Reporting (ATO)**: Australian Tax Office compliant CSV exports
  - Capital Gains/Losses report (FIFO method)
  - All Transactions report
  - Financial year filtering (2024-2025, 2025-2026, 2026-2027, or all years)
  - Automatic cost base calculations for capital gains
  - ATO-ready CSV format for myTax upload
  
- **Mobile Responsive Design**: Fully optimized for phones and tablets
  - Responsive breakpoints at 1024px, 768px, and 480px
  - Touch-friendly buttons (44px minimum height)
  - Horizontally scrollable tables on small screens
  - Single-column layouts on mobile
  - Font size optimization (16px inputs to prevent iOS zoom)
  - Print-friendly styles
  
- **Import Latest Backup**: Multi-device synchronization
  - One-click import of most recent server backup
  - Automatic detection of latest backup
  - Shows backup details before importing
  - Syncs all data: holdings, transactions, DCA plans, budget, etc.
  - Perfect for keeping desktop and mobile in sync
  
- **New Tools Tab**: Dedicated tab for calculators and utilities
  - DCA Calculator
  - DCA Planner
  - Tax Reporting

### Changed
- **Automatic Backups**: Now scheduled instead of on-page-load
  - Runs at 00:00 (midnight) and 12:00 (noon) daily
  - Only backs up if data exists (prevents empty backups)
  - Shows console message with next backup time
  - **CRITICAL FIX**: Prevents data loss from empty backups
  
- **Backup System**: Enhanced to include all data
  - Manual backups now include: watchlist, dcaPlans, all portfolio data
  - Automatic backups include complete portfolio state
  - Version updated to '2.1' in all backups
  - Handles wrapped backup format: `{filename, data: {...}}`
  
- **Tab Navigation**: Now includes 🧰 Tools tab (8 tabs total)

### Fixed
- **Execute Purchase Button**: Removed invalid buyNotes field reference
- **DCA Plan Start Date**: Plans now start on first purchase execution, not creation
- **Import Backup**: Handles server's wrapped backup data structure
- **Empty Backup Prevention**: Automatic backups check for data before running
- **Backup Compatibility**: Gracefully handles old backup formats

### Technical Details
- **File Size**: 8,629 lines (+1,003 from v2.0)
- **New Functions**: 11 functions (4 DCA/Tax + 7 DCA Planner)
- **CSS Media Queries**: 3 breakpoints + print styles
- **Mobile Optimizations**: 150+ lines of responsive CSS
- **Backup Safety**: Scheduled backups with data validation

### Security & Safety
- ✅ Multiple backup locations supported
- ✅ Backup validation before import
- ✅ Prevents empty backup overwrites
- ✅ Data preservation on import failures

## [2.0.0] - 2026-04-26

### 🎉 Major Release - Complete Refactor

### Added
- **Budget System**: Full income/expense tracking with frequency (weekly, fortnightly, monthly, yearly)
- **Traditional Assets**: Property, superannuation, and other asset management
- **Liabilities Management**: Track mortgages, loans, and debts with equity calculations
- **Metals Support**: Track gold and silver holdings as part of crypto portfolio
- **Fee Tracking**: Capture transaction fees across all operations (buy, sell, swap, transfer)
- **Asset Assignment**: Link budget items to specific investments
- **Custom Budget Categories**: Create your own income/expense categories
- **Budget Filters**: Show all, income only, or expenses only
- **24h Change from Database**: Calculates 24-hour price changes from local price history instead of API
- **Automatic Daily Backups**: Runs on page load and every 24 hours
- **Browse Backups**: Scrollable modal to view and restore server backups
- **Staking Positions**: Moved to full-width display under category breakdowns
- **Price History Charts**: View historical prices with statistics (7d, 30d, 90d, 1y, max)
- **Tabbed Interface**: Dashboard, Holdings, Transactions, Watchlist, Investments, Budget, Settings
- **Portfolio Summary**: 9-box dashboard with key metrics

### Changed
- **Dashboard Layout**: Reorganized into 3 columns with consistent color scheme
  - Column 1: Total Assets, Total Liabilities, Total Profit/Loss
  - Column 2: Crypto + Metals, 24h Change, Total Fees Paid
  - Column 3: Traditional Assets, Net Worth, Last Updated
- **Investments Page**: Restructured layout
  - Staking moved to top (full-width under category breakdowns)
  - Traditional Assets + Liabilities side-by-side in one card
  - Clean card-based layout for traditional assets (removed table)
- **Holdings Table Headers**: Renamed for clarity
  - "Amount" → "Crypto Balance"
  - "Price (AUD)" → "Rate"
  - "Value (AUD)" → "Current AUD Value"
  - "24h Change" → "Avg Buy Price"
  - Added actual 24h change in separate column
- **Color Scheme**: Unified color palette
  - Green (#10b981): Positive values, net worth
  - Red (#ef4444): Negative values, liabilities, fees
  - Purple (#667eea): Crypto + Metals
  - Amber (#d97706): Traditional Assets
  - Tracker Green (#0f5c4a): Primary brand color
- **Crypto Total**: Now includes metals (gold, silver) but excludes traditional assets
- **Server**: Switched from CoinSpot to CoinGecko API (10,000+ coins vs 16)

### Fixed
- **Price History Stats**: Server now calculates and returns statistics (current, highest, lowest, average, change %, data points)
- **Traditional Assets Rendering**: Fixed undefined priceData error by checking for custom prices
- **Browse Backups**: Added scrolling to modal (max-height: 400px)
- **Backup Endpoints**: Corrected from `/api/backups/` to `/api/backup/` (singular)
- **24h Change Display**: Tracker now uses server-calculated values from price history database instead of localStorage cache
- **Console Errors**: Removed undefined access errors from traditional assets

### Code Quality
- Added comprehensive section headers for better code organization
- Grouped related functions logically
- Added JSDoc-style file header with author and license
- Cleaned up commented code
- Organized into clear functional sections:
  - Global State Variables
  - Coin Metadata & Category Mappings
  - Category & Classification Functions
  - Watchlist Management
  - Traditional Assets
  - API & Price Fetching
  - Holdings Table Rendering
  - Modal Management
  - Staking Positions
  - Liabilities Management
  - Transaction History
  - Budget System
  - Initialization & Auto-Save

### Technical Details
- **File Size**: 7,626 lines of code
- **Functions**: 124 functions
- **Section Headers**: 37 major section markers
- **localStorage Keys**: 15+ data structures
- **API Endpoints**: 8 server endpoints

## [1.3.0] - 2026-04-XX

### Added
- Automatic daily backups
- Transaction history
- Watchlist functionality
- Multi-source tracking

### Changed
- Improved UI layout
- Updated pricing mechanism

## [1.0.0] - 2026-03-XX

### Added
- Initial release
- Basic portfolio tracking
- Holdings management
- CoinSpot integration

---

**Version Naming Convention:**
- Major (X.0.0): Breaking changes, major feature additions
- Minor (x.X.0): New features, backwards compatible
- Patch (x.x.X): Bug fixes, minor improvements
