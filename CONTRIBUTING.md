# Contributing to RJTVentures Crypto Tracker

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Collect information about the bug:
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Browser/OS version
   - Server logs if relevant

Create an issue with:
- Clear, descriptive title
- Detailed description
- Steps to reproduce
- Any relevant logs or screenshots

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature has already been suggested
- Clearly describe the feature and its benefits
- Explain your use case
- Consider if it fits the project's scope

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Test thoroughly

4. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Describe what you changed and why
   - Reference any related issues
   - Include screenshots for UI changes

## 💻 Development Setup

### Prerequisites
- Python 3.8+
- Git
- Modern web browser

### Local Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/rjtventures-crypto-tracker.git
cd rjtventures-crypto-tracker

# Run installation
./install.sh

# Start the server
python3 server_coingecko.py
```

### Testing

Before submitting:
1. Test all existing features still work
2. Test your new feature thoroughly
3. Test on multiple browsers if UI changes
4. Check server logs for errors

## 📝 Code Style

### Python (server_coingecko.py)
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and small

### JavaScript (tracker.html)
- Use meaningful variable names
- Add comments for complex functions
- Maintain consistent indentation (4 spaces)
- Use ES6+ features where appropriate

### CSS
- Follow existing naming conventions
- Keep selectors specific
- Group related styles
- Comment complex layouts

## 🎯 Areas for Contribution

### High Priority
- [ ] Bug fixes
- [ ] Documentation improvements
- [ ] Performance optimizations
- [ ] Browser compatibility fixes

### Medium Priority
- [ ] New cryptocurrency support
- [ ] Additional chart types
- [ ] Export format options
- [ ] UI/UX improvements

### Nice to Have
- [ ] Dark mode theme
- [ ] Mobile app version
- [ ] Docker support
- [ ] Additional languages

## 🐛 Debugging

### Server Issues
```bash
# Check server logs
python3 server_coingecko.py

# Verify port availability
lsof -i :8080
```

### Frontend Issues
- Open browser console (F12)
- Check for JavaScript errors
- Verify localStorage data
- Test with cache cleared

### Database Issues
```bash
# Check database
sqlite3 price_history.db ".schema"
sqlite3 price_history.db "SELECT COUNT(*) FROM price_history;"
```

## 📋 Checklist for PR

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All existing tests pass
- [ ] New tests added for new features
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated
- [ ] No console errors or warnings
- [ ] Tested on multiple browsers
- [ ] Commit messages are clear

## ❓ Questions?

- Check the README.md
- Search existing issues
- Open a new issue for discussion

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to RJTVentures Crypto Tracker! 🙏
