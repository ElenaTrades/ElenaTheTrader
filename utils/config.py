"""Configuration management"""

import os
import yaml
from typing import Any, Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration manager for Elena"""
    
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.env = os.getenv
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get environment variable"""
        return self.env(key, default)
    
    def get_trader_wallet(self, trader_name: str) -> str:
        """Get wallet address for a trader"""
        return self.config['traders'][trader_name]['wallet']
    
    def get_trader_config(self, trader_name: str, key: str, default: Any = None) -> Any:
        """Get configuration value for a trader"""
        return self.config['traders'][trader_name]['strategy'].get(key, default)
    
    def is_enabled(self, trader_name: str) -> bool:
        """Check if a trader is enabled"""
        return self.config['traders'][trader_name].get('enabled', False)
    
    def calculate_position_size(self) -> float:
        """Calculate position size in SOL based on risk management"""
        max_position = float(self.env('MAX_POSITION_SIZE_SOL', '10'))
        return max_position * 0.5  # Start with 50% of max
