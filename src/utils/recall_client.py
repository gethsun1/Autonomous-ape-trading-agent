"""
Recall Network API Client
"""
import requests
import time
from typing import Dict, List, Optional, Any
from decimal import Decimal, ROUND_DOWN
from loguru import logger

from .config import config, get_api_url, get_token_decimals

class RecallClient:
    """Client for interacting with Recall Network API"""
    
    def __init__(self):
        self.base_url = get_api_url()
        self.headers = {
            "Authorization": f"Bearer {config.recall_api_key}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling and retries"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(3):
            try:
                response = self.session.request(method, url, timeout=30, **kwargs)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/3): {e}")
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
    
    def get_agent_profile(self) -> Dict[str, Any]:
        """Get authenticated agent profile"""
        return self._make_request("GET", "/api/agent/profile")
    
    def get_balances(self) -> Dict[str, float]:
        """Get agent token balances"""
        response = self._make_request("GET", "/api/agent/balances")
        
        # Convert to symbol -> amount mapping
        balances = {}
        for balance in response.get("balances", []):
            symbol = balance.get("symbol")
            amount = balance.get("amount", 0)
            if symbol:
                balances[symbol] = float(amount)
        
        return balances
    
    def get_portfolio(self) -> Dict[str, Any]:
        """Get agent portfolio information"""
        return self._make_request("GET", "/api/agent/portfolio")
    
    def get_trade_history(self) -> List[Dict[str, Any]]:
        """Get agent trade history"""
        response = self._make_request("GET", "/api/agent/trades")
        return response.get("trades", [])
    
    def get_token_price(self, token_address: str, chain: str = "evm") -> float:
        """Get current price for a token"""
        params = {
            "token": token_address,
            "chain": chain
        }
        response = self._make_request("GET", "/api/price", params=params)
        return float(response.get("price", 0))
    
    def get_trade_quote(self, from_token: str, to_token: str, amount: str) -> Dict[str, Any]:
        """Get quote for a potential trade"""
        params = {
            "fromToken": from_token,
            "toToken": to_token,
            "amount": amount
        }
        return self._make_request("GET", "/api/trade/quote", params=params)
    
    def execute_trade(self, from_token: str, to_token: str, amount: str, 
                     reason: str, slippage_tolerance: str = "0.5") -> Dict[str, Any]:
        """Execute a trade"""
        payload = {
            "fromToken": from_token,
            "toToken": to_token,
            "amount": amount,
            "reason": reason,
            "slippageTolerance": slippage_tolerance
        }
        
        logger.info(f"Executing trade: {amount} {from_token} -> {to_token}")
        response = self._make_request("POST", "/api/trade/execute", json=payload)
        
        if response.get("success"):
            logger.success(f"Trade executed successfully: {response}")
        else:
            logger.error(f"Trade failed: {response}")
        
        return response
    
    def to_base_units(self, amount_float: float, symbol: str) -> str:
        """Convert human units to base units for API"""
        decimals = get_token_decimals(symbol)
        scaled = Decimal(str(amount_float)) * (10 ** decimals)
        return str(int(scaled.quantize(Decimal("1"), rounding=ROUND_DOWN)))
    
    def from_base_units(self, amount_str: str, symbol: str) -> float:
        """Convert base units to human units"""
        decimals = get_token_decimals(symbol)
        return float(Decimal(amount_str) / (10 ** decimals))
    
    def health_check(self) -> bool:
        """Check if API is accessible"""
        try:
            self._make_request("GET", "/api/health")
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
