"""Tests for configuration management"""

import pytest
from utils.config import Config


def test_config_loads():
    """Test that config loads successfully"""
    config = Config()
    assert config is not None


def test_get_trader_wallet():
    """Test getting trader wallet addresses"""
    config = Config()
    
    volume_wallet = config.get_trader_wallet('volume_trader')
    assert volume_wallet == 'Dsfm1XdBWBF68aSAYqZoTP6PRzxc4ZGgeXU14Zw8XAGU'
    
    lore_wallet = config.get_trader_wallet('lore_trader')
    assert lore_wallet == '3zJqfGWg577XLmyNk7XGF8WQvxTWWVghj7diop1FrYeE'


def test_is_enabled():
    """Test checking if traders are enabled"""
    config = Config()
    
    # All traders should be enabled by default
    assert config.is_enabled('volume_trader') == True
    assert config.is_enabled('lore_trader') == True
    assert config.is_enabled('tiktok_trader') == True
    assert config.is_enabled('copy_trader') == True


def test_get_trader_config():
    """Test getting trader-specific configuration"""
    config = Config()
    
    volume_threshold = config.get_trader_config(
        'volume_trader',
        'volume_threshold_multiplier',
        3.0
    )
    assert volume_threshold == 3.0
    
    sentiment_threshold = config.get_trader_config(
        'lore_trader',
        'sentiment_threshold',
        0.7
    )
    assert sentiment_threshold == 0.7


def test_calculate_position_size():
    """Test position size calculation"""
    config = Config()
    
    position_size = config.calculate_position_size()
    assert position_size > 0
    assert isinstance(position_size, float)
