# Elena Architecture

## System Overview

Elena is built as a modular, async-first trading system with four independent trading strategies running concurrently.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│                    (Entry Point)                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   TradingManager                            │
│              (Orchestrates all traders)                      │
└───┬──────────────┬──────────────┬──────────────┬───────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Volume  │  │  Lore    │  │ TikTok   │  │  Copy    │
│ Trader  │  │  Trader  │  │ Trader   │  │  Trader  │
└────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │            │             │             │
     └────────────┴─────────────┴─────────────┘
                  │
     ┌────────────┴─────────────┐
     │                          │
     ▼                          ▼
┌──────────┐            ┌──────────────┐
│   DEX    │            │  Utilities   │
│  Layer   │            │   - Config   │
│          │            │   - Social   │
│ Jupiter  │            │   - AI/NLP   │
│ Raydium  │            │   - Wallet   │
└─────┬────┘            └──────────────┘
      │
      ▼
┌──────────────┐
│   Solana     │
│  Blockchain  │
└──────────────┘
```

## Component Details

### 1. Trading Manager (`core/manager.py`)
- Initializes all traders
- Manages lifecycle (start/stop)
- Monitors system health
- Coordinates shutdown

### 2. Base Trader (`core/base_trader.py`)
- Abstract base class for all strategies
- Provides common functionality:
  - Solana client management
  - Trade statistics tracking
  - Status reporting
  - Async trading loop

### 3. Individual Traders

#### Volume Trader
- **Data Source:** DEX volume APIs
- **Cycle Time:** 60 seconds
- **Logic:**
  1. Fetch volume data for all tokens
  2. Calculate volume spike ratio
  3. Filter by threshold (3x)
  4. Execute trades on qualifying tokens

#### Lore Trader
- **Data Source:** Social media APIs
- **Cycle Time:** 120 seconds
- **Logic:**
  1. Scrape social platforms
  2. Extract trending narratives
  3. AI sentiment analysis
  4. Trade on strong narratives (>0.6 score)

#### TikTok Trader
- **Data Source:** TikTok API/scraping
- **Cycle Time:** 180 seconds
- **Logic:**
  1. Scan for viral crypto content
  2. Extract token mentions (NLP)
  3. Verify engagement metrics
  4. Enter positions early

#### Copy Trader
- **Data Source:** On-chain wallet monitoring
- **Cycle Time:** 30 seconds
- **Logic:**
  1. Monitor top 10 wallets
  2. Detect new transactions
  3. Copy buy transactions
  4. Scale position size (50% ratio)

### 4. Utilities

#### Config (`utils/config.py`)
- YAML configuration loading
- Environment variable management
- Dynamic trader settings

#### DEX Layer (`utils/dex.py`)
- Jupiter Aggregator integration
- Raydium API calls
- Swap execution
- Volume data fetching

#### Social Media (`utils/social.py`)
- TikTok scraping
- Content analysis
- Token mention extraction

#### Sentiment (`utils/sentiment.py`)
- AI-powered analysis (Claude/GPT)
- Narrative strength scoring
- Trend detection

#### Wallet Tracking (`utils/wallet_tracking.py`)
- Top wallet identification
- Real-time transaction monitoring
- ROI calculation

## Data Flow

### Trade Execution Flow
```
1. Trader identifies opportunity
2. Calculates position size (risk management)
3. Calls DEX layer (execute_swap)
4. DEX layer routes to Jupiter/Raydium
5. Transaction submitted to Solana
6. Result returned to trader
7. Trade recorded in stats
```

### Configuration Flow
```
1. config.yaml loaded at startup
2. .env variables merged
3. Config object passed to all traders
4. Traders read specific settings
5. Runtime adjustments possible
```

## Concurrency Model

- **Async/Await:** All traders use asyncio
- **Parallel Execution:** Each trader runs independently
- **No Shared State:** Traders don't interfere with each other
- **Separate Wallets:** Each trader has dedicated wallet

## Database Schema (Future)

```sql
-- Trades table
CREATE TABLE trades (
    id INTEGER PRIMARY KEY,
    trader_type TEXT,
    token_mint TEXT,
    side TEXT,
    amount_sol REAL,
    price REAL,
    timestamp INTEGER,
    tx_signature TEXT,
    pnl_sol REAL,
    success BOOLEAN
);

-- Positions table
CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    trader_type TEXT,
    token_mint TEXT,
    entry_price REAL,
    amount REAL,
    opened_at INTEGER,
    closed_at INTEGER,
    pnl_sol REAL,
    status TEXT
);
```

## Security Considerations

1. **Private Keys:** Never committed, only in .env
2. **Rate Limiting:** Built into each trader
3. **Error Handling:** Graceful failures, no crashes
4. **Position Limits:** Risk management enforced
5. **Monitoring:** All actions logged

## Performance Characteristics

- **Startup Time:** ~2-3 seconds
- **Memory Usage:** ~100-200MB per trader
- **CPU Usage:** Minimal (async I/O bound)
- **Network:** High (constant monitoring)

## Scalability

### Vertical Scaling
- Increase check frequency
- Add more traders
- Monitor more tokens

### Horizontal Scaling
- Deploy multiple instances
- Different token sets per instance
- Shared Redis for coordination

---

**Version:** 1.0.0  
**Last Updated:** Feb 6, 2026
