# Elena API Documentation

## Configuration API

### Config Class

Located in `utils/config.py`

#### Methods

```python
config = Config(config_path="config.yaml")

# Get environment variable
value = config.get(key: str, default: Any = None) -> Any

# Get trader wallet address
wallet = config.get_trader_wallet(trader_name: str) -> str

# Get trader configuration
setting = config.get_trader_config(
    trader_name: str, 
    key: str, 
    default: Any = None
) -> Any

# Check if trader is enabled
enabled = config.is_enabled(trader_name: str) -> bool

# Calculate position size
size_sol = config.calculate_position_size() -> float
```

#### Example

```python
from utils.config import Config

config = Config()

# Get Solana RPC URL
rpc_url = config.get('SOLANA_RPC_URL')

# Get volume trader wallet
wallet = config.get_trader_wallet('volume_trader')

# Get volume threshold setting
threshold = config.get_trader_config(
    'volume_trader',
    'volume_threshold_multiplier',
    3.0
)

# Check if lore trader is enabled
if config.is_enabled('lore_trader'):
    print("Lore trader is active")
```

---

## Base Trader API

### BaseTrader Class

Located in `core/base_trader.py`

#### Abstract Methods (Must Implement)

```python
async def trade_cycle(self):
    """Execute one trading cycle"""
    pass

def get_sleep_interval(self) -> int:
    """Return seconds to sleep between cycles"""
    pass
```

#### Provided Methods

```python
# Start trading
await trader.run()

# Stop trading
await trader.stop()

# Get current status
status = await trader.get_status()
# Returns: {
#   'running': bool,
#   'trades': int,
#   'wins': int,
#   'losses': int,
#   'pnl_sol': float,
#   'uptime_seconds': float,
#   'wallet': str
# }

# Record trade result
trader.record_trade(success: bool, pnl: float)
```

#### Creating Custom Trader

```python
from core.base_trader import BaseTrader
from utils.config import Config

class MyCustomTrader(BaseTrader):
    def __init__(self, config: Config):
        super().__init__(
            name="MyCustomTrader",
            wallet=config.get_trader_wallet('my_custom_trader'),
            config=config
        )
        # Your custom initialization
    
    async def trade_cycle(self):
        # Your trading logic here
        self.logger.info("Executing trade cycle")
        
        # Example: execute a trade
        # ... trading logic ...
        
        # Record result
        self.record_trade(success=True, pnl=0.5)
    
    def get_sleep_interval(self) -> int:
        return 60  # Check every 60 seconds
```

---

## DEX API

### Functions

Located in `utils/dex.py`

```python
# Get volume data for tokens
volume_data = await get_volume_data(
    client: AsyncClient,
    timeframe_minutes: int = 15
) -> List[Dict]

# Execute a token swap
result = await execute_swap(
    client: AsyncClient,
    wallet: str,
    token_mint: str,
    amount_sol: float,
    side: str  # 'buy' or 'sell'
) -> Dict

# Result format:
# {
#     'success': bool,
#     'error': str | None,
#     'tx': str | None
# }
```

---

## Social Media API

### Functions

Located in `utils/social.py`

```python
# Scan TikTok for viral content
viral_posts = await scan_tiktok_viral(
    threshold_views: int,
    hours_ago: int,
    min_engagement: float
) -> List[Dict]

# Extract token mentions from content
tokens = await extract_token_mentions(
    content: Dict
) -> List[Dict]
```

---

## Sentiment Analysis API

### Functions

Located in `utils/sentiment.py`

```python
# Get trending narratives from platforms
narratives = await get_trending_narratives(
    platforms: List[str]  # ['twitter', 'discord', 'telegram']
) -> List[Dict]

# Analyze narrative strength
strength = await analyze_narrative_strength(
    narrative: Dict
) -> float  # 0.0 to 1.0
```

---

## Wallet Tracking API

### Functions

Located in `utils/wallet_tracking.py`

```python
# Get top performing wallets
top_wallets = await get_top_wallets(
    count: int,
    min_roi: float  # e.g., 2.0 for 2x ROI
) -> List[Dict]

# Monitor wallet activity
activities = await monitor_wallet_activity(
    client: AsyncClient,
    wallet_addresses: List[str]
) -> List[Dict]
```

---

## Trading Manager API

### TradingManager Class

Located in `core/manager.py`

```python
from core.manager import TradingManager
from utils.config import Config

# Initialize
manager = TradingManager(
    traders: List[BaseTrader],
    config: Config
)

# Start all traders
await manager.run()

# Gracefully shutdown
await manager.shutdown()
```

---

## Command Line Interface

### Running Elena

```bash
# Basic usage
python main.py

# With custom config
python main.py --config custom_config.yaml

# Enable debug logging
python main.py --debug

# Run specific trader only
python main.py --trader volume_trader
```

---

## Environment Variables

Required in `.env` file:

```bash
# Solana
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_WSS_URL=wss://api.mainnet-beta.solana.com

# Wallets (NEVER COMMIT ACTUAL KEYS!)
VOLUME_TRADER_PRIVATE_KEY=base58_encoded_key
LORE_TRADER_PRIVATE_KEY=base58_encoded_key
TIKTOK_TRADER_PRIVATE_KEY=base58_encoded_key
COPY_TRADER_PRIVATE_KEY=base58_encoded_key

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
TIKTOK_SESSION_ID=...
TWITTER_BEARER_TOKEN=...

# Trading Limits
MAX_POSITION_SIZE_SOL=10
MAX_DAILY_LOSS_SOL=5
```

---

## Events and Logging

### Log Levels

- **INFO:** Normal operations, trade executions
- **WARNING:** Failed trades, unusual conditions
- **ERROR:** Critical errors, exceptions
- **DEBUG:** Detailed execution info

### Log Format

```
2026-02-06 14:30:15 | elena.VolumeTrader | INFO | Trade executed: SOL/TOKEN
```

---

## Error Handling

All traders implement graceful error handling:

```python
try:
    # Trading logic
    await self.execute_trade()
except Exception as e:
    self.logger.error(f"Error: {e}", exc_info=True)
    # Continue running, don't crash
```

---

**Version:** 1.0.0  
**Last Updated:** Feb 6, 2026
