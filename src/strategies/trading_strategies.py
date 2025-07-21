"""
Trading Strategies for Recall Network Agent
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from loguru import logger
from datetime import datetime, timedelta

class TradingStrategy:
    """Base class for trading strategies"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logger.bind(strategy=name)
    
    def generate_signals(self, market_data: Dict[str, any]) -> Dict[str, str]:
        """Generate trading signals (buy/sell/hold) for each token"""
        raise NotImplementedError
    
    def calculate_position_sizes(self, signals: Dict[str, str], 
                               portfolio_value: float) -> Dict[str, float]:
        """Calculate position sizes based on signals"""
        raise NotImplementedError

class MomentumStrategy(TradingStrategy):
    """Momentum-based trading strategy"""
    
    def __init__(self, lookback_days: int = 7, momentum_threshold: float = 0.05):
        super().__init__("Momentum")
        self.lookback_days = lookback_days
        self.momentum_threshold = momentum_threshold
    
    def generate_signals(self, market_data: Dict[str, any]) -> Dict[str, str]:
        """Generate signals based on price momentum"""
        signals = {}
        
        for symbol, data in market_data.items():
            if symbol == "USDC":  # Skip stablecoin
                signals[symbol] = "hold"
                continue
            
            # Use 7-day price change as momentum indicator
            price_change_7d = data.get("price_change_7d", 0) / 100
            
            if price_change_7d > self.momentum_threshold:
                signals[symbol] = "buy"
                self.logger.info(f"{symbol}: BUY signal (7d change: {price_change_7d:.2%})")
            elif price_change_7d < -self.momentum_threshold:
                signals[symbol] = "sell"
                self.logger.info(f"{symbol}: SELL signal (7d change: {price_change_7d:.2%})")
            else:
                signals[symbol] = "hold"
        
        return signals
    
    def calculate_position_sizes(self, signals: Dict[str, str], 
                               portfolio_value: float) -> Dict[str, float]:
        """Calculate position sizes for momentum strategy"""
        # Equal weight for buy signals, reduce for sell signals
        buy_signals = [s for s in signals.values() if s == "buy"]
        
        if not buy_signals:
            return {"USDC": 1.0}  # All cash if no buy signals
        
        position_size = 0.8 / len(buy_signals)  # 80% invested, 20% cash
        positions = {"USDC": 0.2}  # 20% cash buffer
        
        for symbol, signal in signals.items():
            if signal == "buy":
                positions[symbol] = position_size
            elif signal == "sell":
                positions[symbol] = 0.05  # Minimal position
        
        return positions

class MeanReversionStrategy(TradingStrategy):
    """Mean reversion trading strategy"""
    
    def __init__(self, lookback_days: int = 30, reversion_threshold: float = 0.15):
        super().__init__("MeanReversion")
        self.lookback_days = lookback_days
        self.reversion_threshold = reversion_threshold
    
    def generate_signals(self, market_data: Dict[str, any]) -> Dict[str, str]:
        """Generate signals based on mean reversion"""
        signals = {}
        
        for symbol, data in market_data.items():
            if symbol == "USDC":
                signals[symbol] = "hold"
                continue
            
            # Use 30-day price change for mean reversion
            price_change_30d = data.get("price_change_30d", 0) / 100
            
            # Buy if significantly down (expecting reversion)
            if price_change_30d < -self.reversion_threshold:
                signals[symbol] = "buy"
                self.logger.info(f"{symbol}: BUY signal (30d change: {price_change_30d:.2%})")
            # Sell if significantly up (expecting reversion)
            elif price_change_30d > self.reversion_threshold:
                signals[symbol] = "sell"
                self.logger.info(f"{symbol}: SELL signal (30d change: {price_change_30d:.2%})")
            else:
                signals[symbol] = "hold"
        
        return signals
    
    def calculate_position_sizes(self, signals: Dict[str, str], 
                               portfolio_value: float) -> Dict[str, float]:
        """Calculate position sizes for mean reversion strategy"""
        # Conservative position sizing
        positions = {"USDC": 0.3}  # 30% cash
        
        buy_signals = [s for s in signals.values() if s == "buy"]
        if buy_signals:
            position_size = 0.7 / len(buy_signals)
            for symbol, signal in signals.items():
                if signal == "buy":
                    positions[symbol] = position_size
                elif signal == "sell":
                    positions[symbol] = 0.0
        
        return positions

class VolatilityStrategy(TradingStrategy):
    """Volatility-based trading strategy"""
    
    def __init__(self, vol_threshold_low: float = 0.02, vol_threshold_high: float = 0.08):
        super().__init__("Volatility")
        self.vol_threshold_low = vol_threshold_low
        self.vol_threshold_high = vol_threshold_high
    
    def calculate_volatility(self, market_data: Dict[str, any]) -> Dict[str, float]:
        """Calculate implied volatility from price changes"""
        volatilities = {}
        
        for symbol, data in market_data.items():
            if symbol == "USDC":
                volatilities[symbol] = 0.0
                continue
            
            # Estimate volatility from recent price changes
            price_change_24h = abs(data.get("price_change_24h", 0)) / 100
            price_change_7d = abs(data.get("price_change_7d", 0)) / 100
            
            # Simple volatility estimate
            volatility = (price_change_24h * 7 + price_change_7d) / 2
            volatilities[symbol] = volatility
        
        return volatilities
    
    def generate_signals(self, market_data: Dict[str, any]) -> Dict[str, str]:
        """Generate signals based on volatility levels"""
        signals = {}
        volatilities = self.calculate_volatility(market_data)
        
        for symbol, volatility in volatilities.items():
            if symbol == "USDC":
                signals[symbol] = "hold"
                continue
            
            if volatility < self.vol_threshold_low:
                # Low volatility - expect breakout
                signals[symbol] = "buy"
                self.logger.info(f"{symbol}: BUY signal (low vol: {volatility:.3f})")
            elif volatility > self.vol_threshold_high:
                # High volatility - reduce exposure
                signals[symbol] = "sell"
                self.logger.info(f"{symbol}: SELL signal (high vol: {volatility:.3f})")
            else:
                signals[symbol] = "hold"
        
        return signals
    
    def calculate_position_sizes(self, signals: Dict[str, str], 
                               portfolio_value: float) -> Dict[str, float]:
        """Calculate position sizes based on volatility"""
        positions = {"USDC": 0.25}  # 25% cash
        
        buy_signals = [s for s in signals.values() if s == "buy"]
        if buy_signals:
            position_size = 0.75 / len(buy_signals)
            for symbol, signal in signals.items():
                if signal == "buy":
                    positions[symbol] = position_size
                elif signal == "sell":
                    positions[symbol] = 0.1  # Small position
        
        return positions

class StrategyManager:
    """Manages multiple trading strategies and combines signals"""
    
    def __init__(self):
        self.strategies = {
            "momentum": MomentumStrategy(),
            "mean_reversion": MeanReversionStrategy(),
            "volatility": VolatilityStrategy()
        }
        self.logger = logger.bind(component="StrategyManager")
    
    def add_strategy(self, name: str, strategy: TradingStrategy):
        """Add a new strategy"""
        self.strategies[name] = strategy
        self.logger.info(f"Added strategy: {name}")
    
    def remove_strategy(self, name: str):
        """Remove a strategy"""
        if name in self.strategies:
            del self.strategies[name]
            self.logger.info(f"Removed strategy: {name}")
    
    def get_combined_signals(self, market_data: Dict[str, any]) -> Dict[str, str]:
        """Combine signals from all strategies"""
        all_signals = {}
        
        # Get signals from each strategy
        for name, strategy in self.strategies.items():
            try:
                signals = strategy.generate_signals(market_data)
                all_signals[name] = signals
                self.logger.info(f"Generated signals for {name}: {signals}")
            except Exception as e:
                self.logger.error(f"Error generating signals for {name}: {e}")
        
        # Combine signals using majority voting
        combined_signals = {}
        symbols = set()
        for signals in all_signals.values():
            symbols.update(signals.keys())
        
        for symbol in symbols:
            votes = {"buy": 0, "sell": 0, "hold": 0}
            
            for signals in all_signals.values():
                signal = signals.get(symbol, "hold")
                votes[signal] += 1
            
            # Choose signal with most votes
            combined_signals[symbol] = max(votes, key=votes.get)
        
        self.logger.info(f"Combined signals: {combined_signals}")
        return combined_signals
    
    def get_strategy_allocation(self, strategy_name: str, market_data: Dict[str, any], 
                              portfolio_value: float) -> Dict[str, float]:
        """Get allocation from a specific strategy"""
        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        strategy = self.strategies[strategy_name]
        signals = strategy.generate_signals(market_data)
        allocation = strategy.calculate_position_sizes(signals, portfolio_value)
        
        return allocation
