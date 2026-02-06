"""Pytest configuration and fixtures"""

import pytest
import os


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables"""
    env_vars = {
        'SOLANA_RPC_URL': 'https://api.devnet.solana.com',
        'SOLANA_WSS_URL': 'wss://api.devnet.solana.com',
        'MAX_POSITION_SIZE_SOL': '5',
        'MAX_DAILY_LOSS_SOL': '2',
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    return env_vars


@pytest.fixture
def sample_volume_data():
    """Sample volume data for testing"""
    return [
        {
            'mint': 'TOKEN1',
            'symbol': 'TKN1',
            'current_volume': 150000,
            'avg_volume': 50000,
        },
        {
            'mint': 'TOKEN2',
            'symbol': 'TKN2',
            'current_volume': 75000,
            'avg_volume': 50000,
        }
    ]


@pytest.fixture
def sample_narrative():
    """Sample narrative data for testing"""
    return {
        'topic': 'AI Agents',
        'platforms': ['twitter', 'discord'],
        'mentions': 1250,
        'sentiment': 0.8,
        'associated_token': {
            'mint': 'AITOKEN',
            'symbol': 'AIGT'
        }
    }
