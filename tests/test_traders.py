"""Tests for trader implementations"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from core.base_trader import BaseTrader
from utils.config import Config


class MockTrader(BaseTrader):
    """Mock trader for testing"""
    
    def __init__(self, config: Config):
        super().__init__("MockTrader", "test_wallet", config)
        self.cycles_executed = 0
    
    async def trade_cycle(self):
        self.cycles_executed += 1
    
    def get_sleep_interval(self) -> int:
        return 1


@pytest.mark.asyncio
async def test_trader_initialization():
    """Test that traders initialize correctly"""
    config = Config()
    trader = MockTrader(config)
    
    assert trader.name == "MockTrader"
    assert trader.wallet == "test_wallet"
    assert trader.running == False
    assert trader.stats['trades'] == 0


@pytest.mark.asyncio
async def test_trader_status():
    """Test getting trader status"""
    config = Config()
    trader = MockTrader(config)
    
    status = await trader.get_status()
    
    assert 'running' in status
    assert 'trades' in status
    assert 'wins' in status
    assert 'losses' in status
    assert 'pnl_sol' in status
    assert 'wallet' in status


def test_record_trade():
    """Test recording trade results"""
    config = Config()
    trader = MockTrader(config)
    
    # Record winning trade
    trader.record_trade(success=True, pnl=1.5)
    assert trader.stats['trades'] == 1
    assert trader.stats['wins'] == 1
    assert trader.stats['losses'] == 0
    assert trader.stats['total_pnl_sol'] == 1.5
    
    # Record losing trade
    trader.record_trade(success=False, pnl=-0.5)
    assert trader.stats['trades'] == 2
    assert trader.stats['wins'] == 1
    assert trader.stats['losses'] == 1
    assert trader.stats['total_pnl_sol'] == 1.0
