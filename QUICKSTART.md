# Elena Quick Start Guide

Get Elena up and running in 5 minutes! 🚀

## Prerequisites

- **Python 3.11+** installed
- **Solana wallet** with some SOL
- **API Keys** (see below)

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/ElenaTrades/ElenaTheTrader.git
cd ElenaTheTrader

# Run setup script
chmod +x setup.sh
./setup.sh
```

## Step 2: Get API Keys

### OpenAI (for sentiment analysis)
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy the key (starts with `sk-`)

### Anthropic Claude (for AI analysis)
1. Go to https://console.anthropic.com/settings/keys
2. Create new API key
3. Copy the key (starts with `sk-ant-`)

### TikTok (for viral content monitoring)
1. Log into TikTok on web
2. Open browser DevTools → Application → Cookies
3. Find `sessionid` cookie value
4. Copy the value

### Twitter/X (for narrative tracking)
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create new app
3. Generate Bearer Token
4. Copy the token

## Step 3: Configure Wallets

```bash
# Create .env file from template
cp .env.example .env

# Edit .env file
nano .env
```

Add your configuration:

```bash
# Solana RPC (use public or your own)
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# Your wallet private keys (base58 encoded)
# WARNING: Keep these secret! Never commit to git!
VOLUME_TRADER_PRIVATE_KEY=your_key_here
LORE_TRADER_PRIVATE_KEY=your_key_here
TIKTOK_TRADER_PRIVATE_KEY=your_key_here
COPY_TRADER_PRIVATE_KEY=your_key_here

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
TIKTOK_SESSION_ID=...
TWITTER_BEARER_TOKEN=...

# Trading Limits (adjust based on your risk tolerance)
MAX_POSITION_SIZE_SOL=10
MAX_DAILY_LOSS_SOL=5
```

## Step 4: Customize Trading Parameters

Edit `config.yaml` to adjust strategies:

```yaml
traders:
  volume_trader:
    enabled: true  # Set to false to disable
    strategy:
      volume_threshold_multiplier: 3.0  # Lower = more sensitive
      min_volume_usd: 50000  # Minimum volume to consider
  
  lore_trader:
    enabled: true
    strategy:
      sentiment_threshold: 0.7  # 0.0 to 1.0
      narrative_strength_min: 0.6
  
  tiktok_trader:
    enabled: true
    strategy:
      viral_threshold_views: 100000
      early_detection_window_hours: 6
  
  copy_trader:
    enabled: true
    strategy:
      top_wallets_count: 10
      position_size_ratio: 0.5  # Copy 50% of their position
```

## Step 5: Run Elena

```bash
# Activate virtual environment
source venv/bin/activate

# Start Elena
python main.py
```

You should see output like:

```
🤖 Starting Elena - Automated Solana Trading Bot
📊 Initializing Volume Trader...
📖 Initializing Lore Trader...
📱 Initializing TikTok Trader...
👥 Initializing Copy Trader...
🚀 Starting 4 trading mode(s)
🟢 Trading Manager started
```

## Step 6: Monitor Performance

Elena will log all activities. Watch the console for:

- 💰 Trade executions
- 📊 Volume spikes detected
- 📖 Strong narratives found
- 📱 Viral content detected
- 👥 Wallet copies executed

Check `logs/` directory for detailed logs.

## Docker Alternative

If you prefer Docker:

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f elena

# Stop
docker-compose down
```

## Testing Before Live Trading

1. **Start with small amounts:** Set `MAX_POSITION_SIZE_SOL=0.1`
2. **Use devnet first:** Change RPC to devnet in `.env`
3. **Enable only one trader:** Disable others in `config.yaml`
4. **Monitor closely:** Watch logs for first few hours

## Troubleshooting

### "No module named 'solana'"
```bash
pip install -r requirements.txt
```

### "Connection refused"
Check your RPC URL is correct and accessible.

### "Invalid private key"
Ensure your private keys are base58 encoded (not hex).

### "API key invalid"
Double-check your API keys are correct and have proper permissions.

## Safety Tips

1. **Start small** - Don't risk more than you can afford to lose
2. **Monitor regularly** - Check on Elena frequently at first
3. **Set limits** - Use the built-in risk management
4. **Secure your keys** - Never share or commit private keys
5. **Test strategies** - Backtest before going live

## Next Steps

- Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand how Elena works
- Check [ROADMAP.md](ROADMAP.md) for upcoming features
- Join discussions and contribute improvements

## Getting Help

- **Issues:** https://github.com/ElenaTrades/ElenaTheTrader/issues
- **Discussions:** https://github.com/ElenaTrades/ElenaTheTrader/discussions

---

**Happy Trading! 🎯**

Remember: Cryptocurrency trading is risky. Elena is experimental software. Always DYOR!
