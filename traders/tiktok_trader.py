"""
TikTok Trader
Detects viral crypto content early
"""

import logging
from typing import List, Dict

from core.base_trader import BaseTrader
from utils.config import Config
from utils.social import scan_tiktok_viral, extract_token_mentions
from utils.dex import execute_swap

logger = logging.getLogger(__name__)


class TikTokTrader(BaseTrader):
    """Trader that catches viral trends on TikTok"""
    
    def __init__(self, config: Config):
        super().__init__(
            name="TikTokTrader",
            wallet=config.get_trader_wallet('tiktok_trader'),
            config=config
        )
        
        self.viral_threshold = config.get_trader_config(
            'tiktok_trader', 'viral_threshold_views', 100000
        )
        self.early_window_hours = config.get_trader_config(
            'tiktok_trader', 'early_detection_window_hours', 6
        )
        self.min_engagement = config.get_trader_config(
            'tiktok_trader', 'engagement_rate_min', 0.05
        )
        
    async def trade_cycle(self):
        """Execute one TikTok trading cycle"""
        try:
            # Scan TikTok for viral crypto content
            viral_content = await scan_tiktok_viral(
                threshold_views=self.viral_threshold,
                hours_ago=self.early_window_hours,
                min_engagement=self.min_engagement
            )
            
            if not viral_content:
                self.logger.debug("No viral content detected")
                return
            
            self.logger.info(f"📱 Found {len(viral_content)} viral posts")
            
            # Extract token mentions
            for content in viral_content:
                tokens = await extract_token_mentions(content)
                
                for token in tokens:
                    await self._execute_tiktok_trade(token, content)
                    
        except Exception as e:
            self.logger.error(f"Error in trade cycle: {e}", exc_info=True)
    
    async def _execute_tiktok_trade(self, token: Dict, content: Dict):
        """Execute trade on viral TikTok mention"""
        try:
            self.logger.info(
                f"💰 Executing TikTok trade for {token['symbol']} "
                f"(views: {content['views']:,})"
            )
            
            position_size = self.config.calculate_position_size()
            
            result = await execute_swap(
                client=self.client,
                wallet=self.wallet,
                token_mint=token['mint'],
                amount_sol=position_size,
                side='buy'
            )
            
            if result['success']:
                self.logger.info(f"✅ TikTok trade executed: {token['symbol']}")
            else:
                self.logger.warning(f"❌ Trade failed: {result['error']}")
                
        except Exception as e:
            self.logger.error(f"Error executing trade: {e}", exc_info=True)
    
    def get_sleep_interval(self) -> int:
        """Sleep for 3 minutes between checks"""
        return 180
