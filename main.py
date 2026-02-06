#!/usr/bin/env python3
"""
Elena - Automated Solana Trading Bot
Main entry point for the trading system
"""

import asyncio
import logging
from typing import List
from dotenv import load_dotenv

from traders.volume_trader import VolumeTrader
from traders.lore_trader import LoreTrader
from traders.tiktok_trader import TikTokTrader
from traders.copy_trader import CopyTrader
from core.manager import TradingManager
from utils.config import Config
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)


async def main():
    """Main function to run Elena trading bot"""
    logger.info("🤖 Starting Elena - Automated Solana Trading Bot")
    
    # Load configuration
    config = Config()
    
    # Initialize traders
    traders: List = []
    
    if config.is_enabled('volume_trader'):
        logger.info("📊 Initializing Volume Trader...")
        traders.append(VolumeTrader(config))
    
    if config.is_enabled('lore_trader'):
        logger.info("📖 Initializing Lore Trader...")
        traders.append(LoreTrader(config))
    
    if config.is_enabled('tiktok_trader'):
        logger.info("📱 Initializing TikTok Trader...")
        traders.append(TikTokTrader(config))
    
    if config.is_enabled('copy_trader'):
        logger.info("👥 Initializing Copy Trader...")
        traders.append(CopyTrader(config))
    
    if not traders:
        logger.error("❌ No traders enabled. Check your configuration.")
        return
    
    # Initialize trading manager
    manager = TradingManager(traders, config)
    
    # Start trading
    logger.info(f"🚀 Starting {len(traders)} trading mode(s)")
    try:
        await manager.run()
    except KeyboardInterrupt:
        logger.info("⏸️  Shutting down gracefully...")
        await manager.shutdown()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        await manager.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
