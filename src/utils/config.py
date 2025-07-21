"""
Configuration management for Recall Network Trading Agent
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv()

class TradingConfig(BaseSettings):
    """Trading bot configuration with validation"""
    
    # API Keys
    recall_api_key: str
    openai_api_key: str = ""
    coingecko_api_key: str = ""
    
    # Environment
    environment: str = "sandbox"
    log_level: str = "INFO"
    
    # Trading Parameters
    rebalance_threshold: float = 0.02  # 2%
    trade_amount_usd: float = 100.0
    max_position_size: float = 0.3  # 30% max per position
    stop_loss_percentage: float = 0.05  # 5%
    
    # Timing
    rebalance_time: str = "09:00"
    price_update_interval: int = 300  # 5 minutes
    
    @validator('environment')
    def validate_environment(cls, v):
        if v not in ['sandbox', 'production']:
            raise ValueError('Environment must be "sandbox" or "production"')
        return v
    
    @validator('rebalance_threshold')
    def validate_threshold(cls, v):
        if not 0.001 <= v <= 0.1:
            raise ValueError('Rebalance threshold must be between 0.1% and 10%')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global configuration instance
config = TradingConfig(
    recall_api_key=os.getenv("RECALL_API_KEY", ""),
    openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    coingecko_api_key=os.getenv("COINGECKO_API_KEY", ""),
    environment=os.getenv("ENVIRONMENT", "sandbox"),
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    rebalance_threshold=float(os.getenv("REBALANCE_THRESHOLD", "0.02")),
    trade_amount_usd=float(os.getenv("TRADE_AMOUNT_USD", "100.0")),
    max_position_size=float(os.getenv("MAX_POSITION_SIZE", "0.3")),
    stop_loss_percentage=float(os.getenv("STOP_LOSS_PERCENTAGE", "0.05")),
)

# API URLs
API_URLS = {
    "sandbox": "https://api.sandbox.competitions.recall.network",
    "production": "https://api.competitions.recall.network"
}

# Token configurations
TOKEN_CONFIG = {
    "USDC": {
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "decimals": 6,
        "coingecko_id": "usd-coin",
        "chain": "evm",
        "symbol": "USDC"
    },
    "WETH": {
        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "decimals": 18,
        "coingecko_id": "weth",
        "chain": "evm",
        "symbol": "WETH"
    },
    "WBTC": {
        "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "decimals": 8,
        "coingecko_id": "wrapped-bitcoin",
        "chain": "evm",
        "symbol": "WBTC"
    },
    "SOL": {
        "address": "So11111111111111111111111111111111111111112",
        "decimals": 9,
        "coingecko_id": "solana",
        "chain": "svm",
        "symbol": "SOL"
    }
}

def get_api_url() -> str:
    """Get the appropriate API URL based on environment"""
    return API_URLS[config.environment]

def get_token_address(symbol: str) -> str:
    """Get token address by symbol"""
    if symbol not in TOKEN_CONFIG:
        raise ValueError(f"Unknown token symbol: {symbol}")
    return TOKEN_CONFIG[symbol]["address"]

def get_token_decimals(symbol: str) -> int:
    """Get token decimals by symbol"""
    if symbol not in TOKEN_CONFIG:
        raise ValueError(f"Unknown token symbol: {symbol}")
    return TOKEN_CONFIG[symbol]["decimals"]
