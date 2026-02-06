"""
Base Trader Class
Abstract base class for all trading strategies
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime

from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair

from utils.config import Config


class BaseTrader(ABC):
    """Abstract base class for all traders"""
    
    def __init__(self, name: str, wallet: str, config: Config):
        self.name = name
        self.wallet = wallet
        self.config = config
        self.running = False
        self.logger = logging.getLogger(f"elena.{name}")
        
        # Solana client
        self.client = AsyncClient(config.get('SOLANA_RPC_URL'))
        
        # Trading stats
        self.stats = {
            'trades': 0,
            'wins': 0,
            'losses': 0,
            'total_pnl_sol': 0.0,
            'started_at': None
        }
        
    async def run(self):
        """Main trading loop"""
        self.running = True
        self.stats['started_at'] = datetime.now()
        self.logger.info(f"🟢 {self.name} started")
        
        try:
            while self.running:
                await self.trade_cycle()
                await asyncio.sleep(self.get_sleep_interval())
        except Exception as e:
            self.logger.error(f"Error in trading loop: {e}", exc_info=True)
        finally:
            await self.stop()
            
    async def stop(self):
        """Stop the trader"""
        self.running = False
        await self.client.close()
        self.logger.info(f"🔴 {self.name} stopped")
        
    @abstractmethod
    async def trade_cycle(self):
        """Execute one trading cycle - must be implemented by subclass"""
        pass
    
    @abstractmethod
    def get_sleep_interval(self) -> int:
        """Return seconds to sleep between cycles"""
        pass
    
    async def get_status(self) -> Dict[str, Any]:
        """Return current trader status"""
        uptime = None
        if self.stats['started_at']:
            uptime = (datetime.now() - self.stats['started_at']).total_seconds()
            
        return {
            'running': self.running,
            'trades': self.stats['trades'],
            'wins': self.stats['wins'],
            'losses': self.stats['losses'],
            'pnl_sol': self.stats['total_pnl_sol'],
            'uptime_seconds': uptime,
            'wallet': self.wallet
        }
    
    def record_trade(self, success: bool, pnl: float):
        """Record trade result"""
        self.stats['trades'] += 1
        if success:
            self.stats['wins'] += 1
        else:
            self.stats['losses'] += 1
        self.stats['total_pnl_sol'] += pnl
