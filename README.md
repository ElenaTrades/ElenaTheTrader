# Elena 🤖💰

[![CI](https://github.com/ElenaTrades/ElenaTheTrader/workflows/CI/badge.svg)](https://github.com/ElenaTrades/ElenaTheTrader/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Built on Solana](https://img.shields.io/badge/Built%20on-Solana-9945FF?logo=solana)](https://solana.com)

An intelligent automated Solana trader with four specialized trading modes, each powered by unique data sources and strategies.

---

## 🎯 Trading Modes

### 1. Volume Trader
**Wallet:** `Dsfm1XdBWBF68aSAYqZoTP6PRzxc4ZGgeXU14Zw8XAGU`

Tracks and analyzes trading volume spikes across Solana DEXs to identify tokens with unusual activity. Capitalizes on momentum by entering positions during volume surges and exiting before the trend reverses.

**Strategy:**
- Monitors DEX volume in real-time
- Identifies 3x+ volume spikes
- Enters positions on confirmed momentum
- Exits when volume drops below threshold

---

### 2. Lore Trader
**Wallet:** `3zJqfGWg577XLmyNk7XGF8WQvxTWWVghj7diop1FrYeE`

Analyzes community narratives, memes, and cultural trends to identify tokens with strong storytelling potential. Trades based on sentiment analysis and the power of community-driven narratives in the crypto space.

**Strategy:**
- Monitors Twitter, Discord, Telegram
- Uses AI sentiment analysis
- Identifies emerging narratives
- Trades on narrative strength >0.6

---

### 3. TikTok Trader
**Wallet:** `AgqPKDQpubJcnahXVeSdQy4KimVuQearp4FKokRASXPu`

Scans TikTok for viral crypto content and emerging trends before they hit mainstream platforms. Gets in early on tokens gaining traction through viral social media content, catching waves before they peak.

**Strategy:**
- Scans TikTok for viral posts (>100K views)
- 6-hour early detection window
- Extracts token mentions using NLP
- Enters before mainstream adoption

---

### 4. Copy Trader
**Wallet:** `CkSAH87iysawMBVaWginNW1tcWDSJ3x9UuL8Lkfjmmuu`

Mirrors the trades of the most profitable Solana wallets in real-time. Identifies and follows top-performing traders, automatically replicating their positions to capture their alpha.

**Strategy:**
- Tracks top 10 wallets (>2x ROI/30d)
- Real-time transaction monitoring
- 5-second copy delay
- 50% position size ratio

---

## 🚀 Quick Start

**→ [Read the full Quick Start Guide](QUICKSTART.md) for detailed setup instructions**

### TL;DR

```bash
# Clone and setup
git clone https://github.com/ElenaTrades/ElenaTheTrader.git
cd ElenaTheTrader
./setup.sh

# Configure (add your API keys and wallet keys)
cp .env.example .env
nano .env

# Run
source venv/bin/activate
python main.py
```

### Docker (Recommended)

```bash
docker-compose up -d
docker-compose logs -f elena
```

### Useful Scripts

```bash
# Check wallet balances
python scripts/check_balance.py

# Monitor trading activity
python scripts/monitor.py
```

---

## 📁 Project Structure

```
Elena/
├── main.py                 # Entry point
├── config.yaml            # Configuration
├── requirements.txt       # Dependencies
├── core/
│   ├── base_trader.py    # Base trader class
│   └── manager.py        # Trading manager
├── traders/
│   ├── volume_trader.py  # Volume strategy
│   ├── lore_trader.py    # Narrative strategy
│   ├── tiktok_trader.py  # Viral content strategy
│   └── copy_trader.py    # Copy trading strategy
└── utils/
    ├── config.py         # Config manager
    ├── dex.py           # DEX interactions
    ├── sentiment.py     # Sentiment analysis
    ├── social.py        # Social media monitoring
    └── wallet_tracking.py # Wallet analysis
```

---

## ⚙️ Configuration

Edit `config.yaml` to customize:
- Enable/disable specific traders
- Adjust trading thresholds
- Configure risk management
- Set position sizes

Edit `.env` for:
- RPC endpoints
- Wallet private keys
- API credentials
- Database connections

---

## 📊 Monitoring

Each trader reports:
- Number of trades executed
- Win/loss ratio
- Total PnL in SOL
- Current positions
- System uptime

Logs are stored in `logs/` directory.

---

## 🛡️ Risk Management

Built-in protections:
- Stop loss: 15% per position
- Take profit: 50% per position
- Daily loss limit: 5 SOL
- Max concurrent positions: 5
- Position size limits: 20% of capital

---

## 🤝 Contributors

**Co-Author & Contributor:** [@rohunvora](https://github.com/rohunvora)

Want to contribute? Check out [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

---

## ⚠️ Disclaimer

This is an experimental trading bot. Cryptocurrency trading involves substantial risk of loss. This software is provided "as is" without warranty of any kind. Use at your own risk. Always do your own research and never invest more than you can afford to lose.

---

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Architecture](docs/ARCHITECTURE.md)** - System design and components
- **[API Documentation](docs/API.md)** - Complete API reference
- **[Roadmap](ROADMAP.md)** - Future development plans
- **[Security](SECURITY.md)** - Security best practices
- **[Contributing](CONTRIBUTING.md)** - How to contribute

## 🔗 Links

- **Repository:** https://github.com/ElenaTrades/ElenaTheTrader
- **Issues:** https://github.com/ElenaTrades/ElenaTheTrader/issues
- **Discussions:** https://github.com/ElenaTrades/ElenaTheTrader/discussions

---

**Built on Solana** ⚡ | **Powered by AI** 🤖
