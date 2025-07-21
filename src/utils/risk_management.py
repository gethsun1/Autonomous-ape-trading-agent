"""
Risk Management Module for Trading Agent
"""
import time
from typing import Dict, List, Optional, Tuple
from loguru import logger
from datetime import datetime, timedelta

from .config import config

class RiskManager:
    """Risk management system for trading operations"""
    
    def __init__(self):
        self.logger = logger.bind(component="RiskManager")
        self.trade_history = []
        self.daily_pnl = {}
        self.position_limits = {}
        
        # Risk parameters
        self.max_daily_loss = 0.05  # 5% max daily loss
        self.max_position_size = config.max_position_size
        self.stop_loss_pct = config.stop_loss_percentage
        self.max_trades_per_hour = 10
        self.min_trade_interval = 60  # seconds
        
        self.logger.info("Risk Manager initialized")
    
    def check_position_size(self, symbol: str, allocation: float, 
                          portfolio_value: float) -> Tuple[bool, str]:
        """Check if position size is within limits"""
        if allocation > self.max_position_size:
            return False, f"Position size {allocation:.2%} exceeds limit {self.max_position_size:.2%}"
        
        if allocation < 0:
            return False, "Negative position size not allowed"
        
        return True, "Position size OK"
    
    def check_daily_loss_limit(self, current_portfolio_value: float) -> Tuple[bool, str]:
        """Check if daily loss limit has been reached"""
        today = datetime.now().date()
        
        if today not in self.daily_pnl:
            # First trade of the day, record starting value
            self.daily_pnl[today] = {
                "start_value": current_portfolio_value,
                "current_value": current_portfolio_value,
                "pnl": 0.0
            }
            return True, "Daily loss check OK"
        
        # Update current value and calculate PnL
        start_value = self.daily_pnl[today]["start_value"]
        pnl_pct = (current_portfolio_value - start_value) / start_value
        
        self.daily_pnl[today]["current_value"] = current_portfolio_value
        self.daily_pnl[today]["pnl"] = pnl_pct
        
        if pnl_pct < -self.max_daily_loss:
            return False, f"Daily loss limit reached: {pnl_pct:.2%} < -{self.max_daily_loss:.2%}"
        
        return True, f"Daily PnL: {pnl_pct:.2%}"
    
    def check_trade_frequency(self) -> Tuple[bool, str]:
        """Check if trade frequency limits are respected"""
        now = time.time()
        
        # Check minimum interval since last trade
        if self.trade_history:
            last_trade_time = self.trade_history[-1]["timestamp"]
            if now - last_trade_time < self.min_trade_interval:
                return False, f"Minimum trade interval not met: {now - last_trade_time:.0f}s < {self.min_trade_interval}s"
        
        # Check hourly trade limit
        hour_ago = now - 3600
        recent_trades = [t for t in self.trade_history if t["timestamp"] > hour_ago]
        
        if len(recent_trades) >= self.max_trades_per_hour:
            return False, f"Hourly trade limit reached: {len(recent_trades)} >= {self.max_trades_per_hour}"
        
        return True, "Trade frequency OK"
    
    def check_stop_loss(self, symbol: str, current_price: float, 
                       entry_price: float, position_type: str) -> Tuple[bool, str]:
        """Check if stop loss should be triggered"""
        if position_type == "long":
            loss_pct = (entry_price - current_price) / entry_price
        else:  # short
            loss_pct = (current_price - entry_price) / entry_price
        
        if loss_pct > self.stop_loss_pct:
            return True, f"Stop loss triggered for {symbol}: {loss_pct:.2%} > {self.stop_loss_pct:.2%}"
        
        return False, f"Stop loss OK for {symbol}: {loss_pct:.2%}"
    
    def validate_trade(self, symbol: str, side: str, amount: float, 
                      current_price: float, portfolio_value: float) -> Tuple[bool, str]:
        """Comprehensive trade validation"""
        # Check position size
        allocation = (amount * current_price) / portfolio_value
        size_ok, size_msg = self.check_position_size(symbol, allocation, portfolio_value)
        if not size_ok:
            return False, f"Position size check failed: {size_msg}"
        
        # Check daily loss limit
        loss_ok, loss_msg = self.check_daily_loss_limit(portfolio_value)
        if not loss_ok:
            return False, f"Daily loss check failed: {loss_msg}"
        
        # Check trade frequency
        freq_ok, freq_msg = self.check_trade_frequency()
        if not freq_ok:
            return False, f"Trade frequency check failed: {freq_msg}"
        
        return True, "All risk checks passed"
    
    def record_trade(self, symbol: str, side: str, amount: float, 
                    price: float, success: bool, reason: str = ""):
        """Record a trade for risk tracking"""
        trade_record = {
            "timestamp": time.time(),
            "symbol": symbol,
            "side": side,
            "amount": amount,
            "price": price,
            "value": amount * price,
            "success": success,
            "reason": reason
        }
        
        self.trade_history.append(trade_record)
        
        # Keep only last 1000 trades
        if len(self.trade_history) > 1000:
            self.trade_history = self.trade_history[-1000:]
        
        self.logger.info(f"Recorded trade: {symbol} {side} {amount:.6f} @ {price:.2f}")
    
    def get_risk_metrics(self) -> Dict[str, any]:
        """Calculate current risk metrics"""
        if not self.trade_history:
            return {"message": "No trade history available"}
        
        now = time.time()
        
        # Recent trade statistics
        day_ago = now - 86400
        recent_trades = [t for t in self.trade_history if t["timestamp"] > day_ago]
        
        successful_trades = [t for t in recent_trades if t["success"]]
        failed_trades = [t for t in recent_trades if not t["success"]]
        
        # Calculate metrics
        metrics = {
            "total_trades_24h": len(recent_trades),
            "successful_trades_24h": len(successful_trades),
            "failed_trades_24h": len(failed_trades),
            "success_rate_24h": len(successful_trades) / len(recent_trades) if recent_trades else 0,
            "total_volume_24h": sum(t["value"] for t in recent_trades),
            "avg_trade_size_24h": sum(t["value"] for t in recent_trades) / len(recent_trades) if recent_trades else 0,
        }
        
        # Add daily PnL if available
        today = datetime.now().date()
        if today in self.daily_pnl:
            metrics["daily_pnl"] = self.daily_pnl[today]["pnl"]
            metrics["daily_pnl_usd"] = (
                self.daily_pnl[today]["current_value"] - 
                self.daily_pnl[today]["start_value"]
            )
        
        return metrics
    
    def should_reduce_risk(self) -> Tuple[bool, str]:
        """Determine if risk should be reduced based on recent performance"""
        metrics = self.get_risk_metrics()
        
        # Check success rate
        success_rate = metrics.get("success_rate_24h", 1.0)
        if success_rate < 0.5 and metrics.get("total_trades_24h", 0) >= 5:
            return True, f"Low success rate: {success_rate:.2%}"
        
        # Check daily PnL
        daily_pnl = metrics.get("daily_pnl", 0)
        if daily_pnl < -0.03:  # 3% daily loss
            return True, f"Significant daily loss: {daily_pnl:.2%}"
        
        return False, "Risk levels acceptable"
    
    def get_adjusted_position_size(self, base_allocation: float, 
                                 symbol: str, market_volatility: float = 0.05) -> float:
        """Adjust position size based on risk factors"""
        # Start with base allocation
        adjusted_allocation = base_allocation
        
        # Reduce if high volatility
        if market_volatility > 0.1:  # 10% volatility
            volatility_factor = min(0.1 / market_volatility, 1.0)
            adjusted_allocation *= volatility_factor
            self.logger.info(f"Reduced allocation for {symbol} due to high volatility: {volatility_factor:.2f}")
        
        # Reduce if recent poor performance
        should_reduce, reason = self.should_reduce_risk()
        if should_reduce:
            adjusted_allocation *= 0.5  # Halve position size
            self.logger.warning(f"Reduced allocation for {symbol} due to risk: {reason}")
        
        # Ensure within limits
        adjusted_allocation = min(adjusted_allocation, self.max_position_size)
        
        return adjusted_allocation
    
    def emergency_stop(self) -> bool:
        """Check if emergency stop should be triggered"""
        metrics = self.get_risk_metrics()
        
        # Emergency conditions
        daily_pnl = metrics.get("daily_pnl", 0)
        success_rate = metrics.get("success_rate_24h", 1.0)
        total_trades = metrics.get("total_trades_24h", 0)
        
        # Trigger emergency stop if:
        # 1. Daily loss > 7%
        # 2. Success rate < 30% with at least 10 trades
        if daily_pnl < -0.07:
            self.logger.critical(f"EMERGENCY STOP: Daily loss {daily_pnl:.2%}")
            return True
        
        if success_rate < 0.3 and total_trades >= 10:
            self.logger.critical(f"EMERGENCY STOP: Low success rate {success_rate:.2%}")
            return True
        
        return False
