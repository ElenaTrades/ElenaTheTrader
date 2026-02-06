"""
Trading Manager
Orchestrates all trading modes and manages system lifecycle
"""

import asyncio
import logging
from typing import List
from datetime import datetime

from core.base_trader import BaseTrader
from utils.config import Config

logger = logging.getLogger(__name__)


class TradingManager:
    """Manages all active traders and system operations"""
    
    def __init__(self, traders: List[BaseTrader], config: Config):
        self.traders = traders
        self.config = config
        self.running = False
        self.tasks = []
        
    async def run(self):
        """Start all traders"""
        self.running = True
        logger.info("🟢 Trading Manager started")
        
        # Start each trader in parallel
        self.tasks = [
            asyncio.create_task(trader.run())
            for trader in self.traders
        ]
        
        # Add monitoring task
        self.tasks.append(asyncio.create_task(self._monitor()))
        
        # Wait for all tasks
        await asyncio.gather(*self.tasks, return_exceptions=True)
        
    async def shutdown(self):
        """Gracefully shutdown all traders"""
        logger.info("🔴 Shutting down Trading Manager...")
        self.running = False
        
        # Stop all traders
        for trader in self.traders:
            await trader.stop()
        
        # Cancel all tasks
        for task in self.tasks:
            if not task.done():
                task.cancel()
        
        logger.info("✅ Shutdown complete")
        
    async def _monitor(self):
        """Monitor system health and trader status"""
        while self.running:
            try:
                # Log status every 5 minutes
                await asyncio.sleep(300)
                
                logger.info("📊 System Status:")
                for trader in self.traders:
                    status = await trader.get_status()
                    logger.info(f"  - {trader.name}: {status}")
                    
            except Exception as e:
                logger.error(f"Error in monitoring: {e}")
                await asyncio.sleep(60)
