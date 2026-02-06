# Contributing to Elena

Thank you for your interest in contributing to Elena! 🎉

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ElenaTheTrader.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests (if applicable)
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Start development
python main.py
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions small and focused

## Areas for Contribution

### High Priority
- [ ] Implement DEX integration (Jupiter, Raydium)
- [ ] Add position management and exit strategies
- [ ] Implement TikTok API integration
- [ ] Build sentiment analysis with Claude/GPT
- [ ] Add wallet tracking and monitoring

### Medium Priority
- [ ] Create backtesting framework
- [ ] Add comprehensive logging
- [ ] Build dashboard for monitoring
- [ ] Implement risk management features
- [ ] Add unit tests

### Nice to Have
- [ ] Web UI for configuration
- [ ] Telegram notifications
- [ ] Performance analytics
- [ ] Multiple DEX support
- [ ] Advanced order types

## Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Write clear commit messages
- Update documentation as needed
- Add tests if applicable
- Ensure your code runs without errors

## Questions?

Open an issue or reach out to the maintainers!

---

**Co-authored by:** [@rohunvora](https://github.com/rohunvora)
