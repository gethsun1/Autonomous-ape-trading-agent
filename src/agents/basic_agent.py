"""
Basic Trading Agent for Recall Network
Implements simple trading strategies and portfolio management
"""
import json
import time
from typing import Dict, List, Optional
from loguru import logger

from ..utils.config import config, get_token_address
from ..utils.recall_client import RecallClient
from ..data.market_data import MarketDataProvider

class BasicTradingAgent:
    """Basic trading agent with portfolio rebalancing capabilities"""
    
    def __init__(self, portfolio_config_path: str = "config/portfolio_config.json"):
        self.recall_client = RecallClient()
        self.market_data = MarketDataProvider()
        self.portfolio_config_path = portfolio_config_path
        
        # Initialize logging
        logger.add("logs/trading_agent.log", rotation="1 day", retention="30 days")
        
        # Verify API connectivity
        if not self.recall_client.health_check():
            raise ConnectionError("Cannot connect to Recall Network API")
        
        logger.info("Basic Trading Agent initialized successfully")
    
    def load_target_allocation(self) -> Dict[str, float]:
        """Load target portfolio allocation from config file"""
        try:
            with open(self.portfolio_config_path, 'r') as f:
                allocation = json.load(f)
            
            # Validate allocation sums to 1.0
            total = sum(allocation.values())
            if abs(total - 1.0) > 0.001:
                logger.warning(f"Portfolio allocation sums to {total}, normalizing...")
                allocation = {k: v/total for k, v in allocation.items()}
            
            logger.info(f"Loaded target allocation: {allocation}")
            return allocation
            
        except FileNotFoundError:
            logger.warning(f"Portfolio config not found at {self.portfolio_config_path}, using default")
            return {"USDC": 0.4, "WETH": 0.4, "WBTC": 0.2}
        except Exception as e:
            logger.error(f"Error loading portfolio config: {e}")
            raise
    
    def get_portfolio_status(self) -> Dict[str, any]:
        """Get current portfolio status including balances and values"""
        try:
            # Get current balances
            balances = self.recall_client.get_balances()
            
            # Get current prices
            symbols = list(balances.keys())
            prices = self.market_data.get_prices(symbols)
            
            # Calculate portfolio value and allocations
            total_value = 0
            portfolio = {}
            
            for symbol, balance in balances.items():
                price = prices.get(symbol, 0)
                value = balance * price
                total_value += value
                
                portfolio[symbol] = {
                    "balance": balance,
                    "price": price,
                    "value": value,
                    "allocation": 0  # Will be calculated below
                }
            
            # Calculate current allocations
            if total_value > 0:
                for symbol in portfolio:
                    portfolio[symbol]["allocation"] = portfolio[symbol]["value"] / total_value
            
            return {
                "total_value": total_value,
                "portfolio": portfolio,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Error getting portfolio status: {e}")
            raise
    
    def calculate_rebalancing_trades(self, target_allocation: Dict[str, float]) -> List[Dict[str, any]]:
        """Calculate trades needed to rebalance portfolio"""
        try:
            portfolio_status = self.get_portfolio_status()
            total_value = portfolio_status["total_value"]
            current_portfolio = portfolio_status["portfolio"]
            
            if total_value == 0:
                logger.warning("Portfolio has zero value, cannot rebalance")
                return []
            
            trades = []
            
            # Calculate required trades
            for symbol, target_weight in target_allocation.items():
                current_value = current_portfolio.get(symbol, {}).get("value", 0)
                current_weight = current_value / total_value if total_value > 0 else 0
                target_value = total_value * target_weight
                
                weight_diff = current_weight - target_weight
                value_diff = abs(current_value - target_value)
                
                # Check if rebalancing is needed
                if abs(weight_diff) >= config.rebalance_threshold:
                    price = current_portfolio.get(symbol, {}).get("price", 0)
                    if price > 0:
                        amount = value_diff / price
                        side = "sell" if weight_diff > 0 else "buy"
                        
                        trades.append({
                            "symbol": symbol,
                            "side": side,
                            "amount": amount,
                            "current_weight": current_weight,
                            "target_weight": target_weight,
                            "weight_diff": weight_diff
                        })
            
            # Sort trades: sells first, then buys
            trades.sort(key=lambda x: 0 if x["side"] == "sell" else 1)
            
            logger.info(f"Calculated {len(trades)} rebalancing trades")
            return trades
            
        except Exception as e:
            logger.error(f"Error calculating rebalancing trades: {e}")
            return []
    
    def execute_trade(self, symbol: str, side: str, amount: float, reason: str = "") -> bool:
        """Execute a single trade"""
        try:
            if side == "sell":
                from_token = get_token_address(symbol)
                to_token = get_token_address("USDC")
                trade_amount = self.recall_client.to_base_units(amount, symbol)
            else:  # buy
                from_token = get_token_address("USDC")
                to_token = get_token_address(symbol)
                # For buys, amount is in USDC
                trade_amount = self.recall_client.to_base_units(amount, "USDC")
            
            if not reason:
                reason = f"Portfolio rebalancing: {side} {symbol}"
            
            response = self.recall_client.execute_trade(
                from_token=from_token,
                to_token=to_token,
                amount=trade_amount,
                reason=reason
            )
            
            success = response.get("success", False)
            if success:
                logger.success(f"Trade executed: {side} {amount:.6f} {symbol}")
            else:
                logger.error(f"Trade failed: {response}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return False
    
    def rebalance_portfolio(self) -> bool:
        """Rebalance portfolio according to target allocation"""
        try:
            logger.info("Starting portfolio rebalancing...")
            
            # Load target allocation
            target_allocation = self.load_target_allocation()
            
            # Calculate required trades
            trades = self.calculate_rebalancing_trades(target_allocation)
            
            if not trades:
                logger.info("Portfolio is already balanced within threshold")
                return True
            
            # Execute trades
            successful_trades = 0
            for trade in trades:
                success = self.execute_trade(
                    symbol=trade["symbol"],
                    side=trade["side"],
                    amount=trade["amount"],
                    reason=f"Rebalancing: {trade['current_weight']:.3f} -> {trade['target_weight']:.3f}"
                )
                
                if success:
                    successful_trades += 1
                
                # Small delay between trades
                time.sleep(1)
            
            logger.info(f"Rebalancing complete: {successful_trades}/{len(trades)} trades successful")
            return successful_trades == len(trades)
            
        except Exception as e:
            logger.error(f"Error during portfolio rebalancing: {e}")
            return False
    
    def run_single_cycle(self):
        """Run a single trading cycle"""
        try:
            logger.info("=== Starting Trading Cycle ===")
            
            # Get portfolio status
            status = self.get_portfolio_status()
            logger.info(f"Portfolio value: ${status['total_value']:.2f}")
            
            # Log current allocations
            for symbol, data in status["portfolio"].items():
                logger.info(f"{symbol}: {data['allocation']:.3f} (${data['value']:.2f})")
            
            # Rebalance if needed
            self.rebalance_portfolio()
            
            logger.info("=== Trading Cycle Complete ===")
            
        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")

    def get_agent_info(self) -> Dict[str, any]:
        """Get agent profile and basic information"""
        try:
            profile = self.recall_client.get_agent_profile()
            return profile
        except Exception as e:
            logger.error(f"Error getting agent info: {e}")
            return {}

if __name__ == "__main__":
    # Create basic portfolio config if it doesn't exist
    import os
    os.makedirs("config", exist_ok=True)

    config_path = "config/portfolio_config.json"
    if not os.path.exists(config_path):
        default_config = {
            "USDC": 0.4,
            "WETH": 0.4,
            "WBTC": 0.2
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        print(f"Created default portfolio config at {config_path}")

    # Run the agent
    agent = BasicTradingAgent()

    # Show agent info
    info = agent.get_agent_info()
    if info.get("success"):
        agent_data = info.get("agent", {})
        print(f"Agent: {agent_data.get('name', 'Unknown')}")
        print(f"Status: {agent_data.get('status', 'Unknown')}")
        print(f"Verified: {agent_data.get('isVerified', False)}")

    agent.run_single_cycle()
