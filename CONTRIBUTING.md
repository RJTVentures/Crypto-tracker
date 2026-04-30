[CONTRIBUTING.md](https://github.com/user-attachments/files/27228780/CONTRIBUTING.md)
# Contributing to RJTVentures Crypto Tracker

Thank you for considering contributing to this project! Here's how you can help.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting a bug, include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Browser/OS version
- Python version (for server issues)

### Suggesting Features

Feature suggestions are welcome! Please:
- Use a clear, descriptive title
- Provide detailed description of proposed feature
- Explain why this would be useful
- Include mockups/examples if possible

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/rjtventures-crypto-tracker.git
   cd rjtventures-crypto-tracker
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Test thoroughly

4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Provide clear description of changes
   - Link related issues
   - Include screenshots for UI changes

## Code Style Guidelines

### HTML/JavaScript
- Use 4-space indentation
- Add section comments for major function groups
- Use descriptive variable/function names
- Keep functions focused and single-purpose

### Python (Server)
- Follow PEP 8 style guide
- Use descriptive variable names
- Add docstrings to functions
- Handle errors gracefully

### Comments
```javascript
// Good: Explains WHY
// Calculate 24h change from database instead of API to avoid rate limits
const change24h = calculateFromDb(coinId);

// Bad: Explains WHAT (obvious from code)
// Set change to result of calculation
const change24h = calculateFromDb(coinId);
```

## Development Setup

### Prerequisites
- Python 3.8+
- Modern web browser
- Text editor / IDE

### Local Development
1. Start the server: `python3 server_coingecko.py`
2. Open `tracker-v2.0-COMPLETE.html` in browser
3. Make changes and test
4. Use browser DevTools for debugging

### Testing Checklist
- [ ] Test on Chrome/Firefox/Safari
- [ ] Test all CRUD operations (Create, Read, Update, Delete)
- [ ] Verify data persists in localStorage
- [ ] Check server endpoints respond correctly
- [ ] Test edge cases (empty data, large numbers, etc.)
- [ ] Verify responsive design on mobile

## Project Structure

```
tracker-v2.0-COMPLETE.html
├── Global State Variables (line ~2290)
├── Coin Metadata & Mappings (line ~2340)
├── Category Functions (line ~2466)
├── Watchlist Management (line ~2518)
├── Traditional Assets (line ~2690)
├── API & Price Fetching (line ~3408)
├── Holdings Rendering (line ~3683)
├── Modal Management (line ~5247)
├── Staking Positions (line ~5684)
├── Liabilities Management (line ~5931)
├── Transaction History (line ~6161)
├── Budget System (line ~7193)
└── Initialization (line ~7556)
```

## What We're Looking For

### High Priority
- Bug fixes
- Performance improvements
- Security enhancements
- Documentation improvements

### Medium Priority
- New features (discuss first in issues)
- UI/UX improvements
- Code refactoring
- Test coverage

### Nice to Have
- Additional chart types
- Export formats (PDF, Excel)
- Multi-language support
- Dark mode

## Questions?

Feel free to:
- Open an issue for discussion
- Ask in pull request comments
- Email: [your-email@example.com]

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in commit history

Thank you for contributing! 🚀
