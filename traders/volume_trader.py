"""
Volume Trader
Tracks volume spikes and momentum trading
"""

import logging
from typing import List, Dict
from datetime import datetime, timedelta

from core.base_trader import BaseTrader
from utils.config import Config
from utils.dex import get_volume_data, execute_swap

logger = logging.getLogger(__name__)


class VolumeTrader(BaseTrader):
    """Trader that identifies and trades volume spikes"""
    
    def __init__(self, config: Config):
        super().__init__(
            name="VolumeTrader",
            wallet=config.get_trader_wallet('volume_trader'),
            config=config
        )
        
        self.volume_threshold = config.get_trader_config(
            'volume_trader', 'volume_threshold_multiplier', 3.0
        )
        self.timeframe = config.get_trader_config(
            'volume_trader', 'timeframe_minutes', 15
        )
        self.min_volume = config.get_trader_config(
            'volume_trader', 'min_volume_usd', 50000
        )
        
    async def trade_cycle(self):
        """Execute one volume trading cycle"""
        try:
            # Fetch recent volume data
            volume_data = await get_volume_data(
                self.client, 
                timeframe_minutes=self.timeframe
            )
            
            # Identify volume spikes
            spikes = self._identify_spikes(volume_data)
            
            if spikes:
                self.logger.info(f"📊 Found {len(spikes)} volume spikes")
                
                for token in spikes:
                    await self._execute_volume_trade(token)
            
        except Exception as e:
            self.logger.error(f"Error in trade cycle: {e}", exc_info=True)
            
    def _identify_spikes(self, volume_data: List[Dict]) -> List[Dict]:
        """Identify tokens with volume spikes"""
        spikes = []
        
        for token_data in volume_data:
            current_volume = token_data.get('current_volume', 0)
            avg_volume = token_data.get('avg_volume', 0)
            
            if current_volume > avg_volume * self.volume_threshold:
                if current_volume >= self.min_volume:
                    spikes.append(token_data)
                    
        return spikes
    
    async def _execute_volume_trade(self, token: Dict):
        """Execute trade on volume spike"""
        try:
            self.logger.info(f"💰 Executing volume trade for {token['symbol']}")
            
            # Calculate position size
            position_size = self.config.calculate_position_size()
            
            # Execute swap
            result = await execute_swap(
                client=self.client,
                wallet=self.wallet,
                token_mint=token['mint'],
                amount_sol=position_size,
                side='buy'
            )
            
            if result['success']:
                self.logger.info(f"✅ Volume trade executed: {token['symbol']}")
                # TODO: Add position tracking and exit logic
            else:
                self.logger.warning(f"❌ Trade failed: {result['error']}")
                
        except Exception as e:
            self.logger.error(f"Error executing trade: {e}", exc_info=True)
    
    def get_sleep_interval(self) -> int:
        """Sleep for 1 minute between checks"""
        return 60
