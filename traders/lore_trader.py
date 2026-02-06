"""
Lore Trader
Analyzes narratives and community sentiment
"""

import logging
from typing import List, Dict

from core.base_trader import BaseTrader
from utils.config import Config
from utils.sentiment import analyze_narrative_strength, get_trending_narratives
from utils.dex import execute_swap

logger = logging.getLogger(__name__)


class LoreTrader(BaseTrader):
    """Trader that follows community narratives and meme potential"""
    
    def __init__(self, config: Config):
        super().__init__(
            name="LoreTrader",
            wallet=config.get_trader_wallet('lore_trader'),
            config=config
        )
        
        self.sentiment_threshold = config.get_trader_config(
            'lore_trader', 'sentiment_threshold', 0.7
        )
        self.narrative_strength_min = config.get_trader_config(
            'lore_trader', 'narrative_strength_min', 0.6
        )
        self.platforms = config.get_trader_config(
            'lore_trader', 'monitor_platforms', ['twitter', 'discord']
        )
        
    async def trade_cycle(self):
        """Execute one lore trading cycle"""
        try:
            # Get trending narratives from social platforms
            narratives = await get_trending_narratives(self.platforms)
            
            if not narratives:
                self.logger.debug("No trending narratives found")
                return
            
            # Analyze each narrative
            for narrative in narratives:
                strength = await analyze_narrative_strength(narrative)
                
                if strength >= self.narrative_strength_min:
                    self.logger.info(
                        f"📖 Strong narrative detected: {narrative['topic']} "
                        f"(strength: {strength:.2f})"
                    )
                    await self._execute_lore_trade(narrative)
                    
        except Exception as e:
            self.logger.error(f"Error in trade cycle: {e}", exc_info=True)
    
    async def _execute_lore_trade(self, narrative: Dict):
        """Execute trade based on narrative strength"""
        try:
            # Find token associated with narrative
            token = narrative.get('associated_token')
            if not token:
                self.logger.warning("No token associated with narrative")
                return
            
            self.logger.info(f"💰 Executing lore trade for {token['symbol']}")
            
            position_size = self.config.calculate_position_size()
            
            result = await execute_swap(
                client=self.client,
                wallet=self.wallet,
                token_mint=token['mint'],
                amount_sol=position_size,
                side='buy'
            )
            
            if result['success']:
                self.logger.info(f"✅ Lore trade executed: {token['symbol']}")
            else:
                self.logger.warning(f"❌ Trade failed: {result['error']}")
                
        except Exception as e:
            self.logger.error(f"Error executing trade: {e}", exc_info=True)
    
    def get_sleep_interval(self) -> int:
        """Sleep for 2 minutes between checks"""
        return 120
