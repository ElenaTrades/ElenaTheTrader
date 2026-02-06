"""
Copy Trader
Mirrors trades from top-performing wallets
"""

import logging
from typing import List, Dict

from core.base_trader import BaseTrader
from utils.config import Config
from utils.wallet_tracking import get_top_wallets, monitor_wallet_activity
from utils.dex import execute_swap

logger = logging.getLogger(__name__)


class CopyTrader(BaseTrader):
    """Trader that copies successful wallet trades"""
    
    def __init__(self, config: Config):
        super().__init__(
            name="CopyTrader",
            wallet=config.get_trader_wallet('copy_trader'),
            config=config
        )
        
        self.top_wallets_count = config.get_trader_config(
            'copy_trader', 'top_wallets_count', 10
        )
        self.min_roi = config.get_trader_config(
            'copy_trader', 'min_wallet_roi_30d', 2.0
        )
        self.copy_delay = config.get_trader_config(
            'copy_trader', 'copy_delay_seconds', 5
        )
        self.position_ratio = config.get_trader_config(
            'copy_trader', 'position_size_ratio', 0.5
        )
        
        self.monitored_wallets = []
        
    async def trade_cycle(self):
        """Execute one copy trading cycle"""
        try:
            # Update list of top wallets periodically
            if not self.monitored_wallets or self.stats['trades'] % 100 == 0:
                await self._update_top_wallets()
            
            # Monitor activity from top wallets
            activities = await monitor_wallet_activity(
                self.client,
                self.monitored_wallets
            )
            
            if activities:
                self.logger.info(f"👥 Detected {len(activities)} wallet activities")
                
                for activity in activities:
                    await self._copy_trade(activity)
                    
        except Exception as e:
            self.logger.error(f"Error in trade cycle: {e}", exc_info=True)
    
    async def _update_top_wallets(self):
        """Update the list of top-performing wallets to copy"""
        try:
            self.logger.info("🔍 Updating top wallets list...")
            
            top_wallets = await get_top_wallets(
                count=self.top_wallets_count,
                min_roi=self.min_roi
            )
            
            self.monitored_wallets = [w['address'] for w in top_wallets]
            
            self.logger.info(
                f"✅ Now monitoring {len(self.monitored_wallets)} wallets"
            )
            
        except Exception as e:
            self.logger.error(f"Error updating wallets: {e}", exc_info=True)
    
    async def _copy_trade(self, activity: Dict):
        """Copy a trade from a monitored wallet"""
        try:
            # Only copy buys
            if activity['side'] != 'buy':
                return
            
            token = activity['token']
            
            self.logger.info(
                f"💰 Copying trade: {token['symbol']} from "
                f"{activity['wallet'][:8]}..."
            )
            
            # Calculate our position size (ratio of their position)
            their_size_sol = activity.get('amount_sol', 0)
            our_size_sol = their_size_sol * self.position_ratio
            
            # Cap at our max position size
            max_size = self.config.calculate_position_size()
            our_size_sol = min(our_size_sol, max_size)
            
            result = await execute_swap(
                client=self.client,
                wallet=self.wallet,
                token_mint=token['mint'],
                amount_sol=our_size_sol,
                side='buy'
            )
            
            if result['success']:
                self.logger.info(f"✅ Copy trade executed: {token['symbol']}")
            else:
                self.logger.warning(f"❌ Trade failed: {result['error']}")
                
        except Exception as e:
            self.logger.error(f"Error copying trade: {e}", exc_info=True)
    
    def get_sleep_interval(self) -> int:
        """Sleep for 30 seconds between checks"""
        return 30
