#!/bin/bash

# =====================================================
# RJTVentures Crypto Tracker - Installation Script
# =====================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "     🏦 RJTVentures Crypto Tracker - Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "This script will set up your crypto tracker."
echo ""
read -p "Press ENTER to continue or Ctrl+C to cancel..."
echo ""

# Check Python version
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Checking Python version..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  • macOS: brew install python3"
    echo "  • Ubuntu/Debian: sudo apt install python3"
    echo "  • Windows: Download from python.org"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Create necessary directories
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Creating directories..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

mkdir -p backups
echo "✅ Created backups/ directory"
echo ""

# Initialize tracked coins file if it doesn't exist
if [ ! -f "tracked_coins.json" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Step 3: Initializing coin tracking..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    cat > tracked_coins.json << 'EOF'
[
  "bitcoin",
  "ethereum",
  "cardano",
  "ripple",
  "solana",
  "dogecoin",
  "litecoin",
  "tron",
  "stellar",
  "eos",
  "power-ledger",
  "redfox-labs-2",
  "neo",
  "gas",
  "tether",
  "rchain",
  "aave",
  "chainlink",
  "the-graph",
  "hedera-hashgraph",
  "fetch-ai"
]
EOF
    echo "✅ Created tracked_coins.json with default coins"
else
    echo "✅ tracked_coins.json already exists (keeping your coins)"
fi
echo ""

# Success message
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                    ✅ INSTALLATION COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1. Start the server:"
echo "   python3 server_coingecko.py"
echo ""
echo "2. Open your browser:"
echo "   http://localhost:8080"
echo ""
echo "3. Start tracking your crypto!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📖 Documentation: README.md"
echo "❓ Having issues? Check the Troubleshooting section in README.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
