"""
Market data provider for cryptocurrency prices and market information
"""
import requests
import time
from typing import Dict, List, Optional
from loguru import logger

from ..utils.config import config, TOKEN_CONFIG

class MarketDataProvider:
    """Provides real-time market data from multiple sources"""
    
    def __init__(self):
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        
        # Add API key if available
        if config.coingecko_api_key:
            self.session.headers.update({
                "x-cg-demo-api-key": config.coingecko_api_key
            })
    
    def get_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Get current prices for multiple tokens"""
        try:
            # Map symbols to CoinGecko IDs
            coingecko_ids = []
            symbol_to_id = {}
            
            for symbol in symbols:
                if symbol in TOKEN_CONFIG:
                    cg_id = TOKEN_CONFIG[symbol]["coingecko_id"]
                    coingecko_ids.append(cg_id)
                    symbol_to_id[cg_id] = symbol
            
            if not coingecko_ids:
                return {}
            
            # Fetch prices from CoinGecko
            ids_str = ",".join(coingecko_ids)
            response = self.session.get(
                f"{self.coingecko_base}/simple/price",
                params={
                    "ids": ids_str,
                    "vs_currencies": "usd"
                },
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Convert back to symbol-based mapping
            prices = {}
            for cg_id, price_data in data.items():
                symbol = symbol_to_id.get(cg_id)
                if symbol and "usd" in price_data:
                    prices[symbol] = float(price_data["usd"])
            
            logger.info(f"Fetched prices for {len(prices)} tokens")
            return prices
            
        except Exception as e:
            logger.error(f"Failed to fetch prices: {e}")
            return {}
    
    def get_price(self, symbol: str) -> Optional[float]:
        """Get current price for a single token"""
        prices = self.get_prices([symbol])
        return prices.get(symbol)
    
    def get_market_data(self, symbol: str) -> Dict[str, any]:
        """Get detailed market data for a token"""
        try:
            if symbol not in TOKEN_CONFIG:
                raise ValueError(f"Unknown token symbol: {symbol}")
            
            cg_id = TOKEN_CONFIG[symbol]["coingecko_id"]
            
            response = self.session.get(
                f"{self.coingecko_base}/coins/{cg_id}",
                params={
                    "localization": "false",
                    "tickers": "false",
                    "market_data": "true",
                    "community_data": "false",
                    "developer_data": "false",
                    "sparkline": "false"
                },
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            market_data = data.get("market_data", {})
            
            return {
                "symbol": symbol,
                "price": market_data.get("current_price", {}).get("usd", 0),
                "market_cap": market_data.get("market_cap", {}).get("usd", 0),
                "volume_24h": market_data.get("total_volume", {}).get("usd", 0),
                "price_change_24h": market_data.get("price_change_percentage_24h", 0),
                "price_change_7d": market_data.get("price_change_percentage_7d", 0),
                "price_change_30d": market_data.get("price_change_percentage_30d", 0),
                "high_24h": market_data.get("high_24h", {}).get("usd", 0),
                "low_24h": market_data.get("low_24h", {}).get("usd", 0),
                "circulating_supply": market_data.get("circulating_supply", 0),
                "total_supply": market_data.get("total_supply", 0),
                "last_updated": market_data.get("last_updated")
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch market data for {symbol}: {e}")
            return {}
    
    def get_trending_tokens(self, limit: int = 10) -> List[Dict[str, any]]:
        """Get trending tokens from CoinGecko"""
        try:
            response = self.session.get(
                f"{self.coingecko_base}/search/trending",
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            trending = data.get("coins", [])[:limit]
            
            return [
                {
                    "symbol": coin["item"]["symbol"],
                    "name": coin["item"]["name"],
                    "market_cap_rank": coin["item"]["market_cap_rank"],
                    "price_btc": coin["item"]["price_btc"]
                }
                for coin in trending
            ]
            
        except Exception as e:
            logger.error(f"Failed to fetch trending tokens: {e}")
            return []
    
    def wait_for_rate_limit(self):
        """Wait to respect rate limits"""
        if not config.coingecko_api_key:
            # Free tier: 30 calls/minute
            time.sleep(2)
        else:
            # Pro tier: higher limits
            time.sleep(0.1)
