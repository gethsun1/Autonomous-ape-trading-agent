#!/usr/bin/env python3
"""
Recall Network Trading Agent - Main Entry Point
Complete trading bot with AI integration, risk management, and multiple strategies
"""
import os
import sys
import argparse
import json
from pathlib import Path
from loguru import logger

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.agents.basic_agent import BasicTradingAgent
from src.agents.portfolio_manager import AdvancedPortfolioManager
from src.strategies.trading_strategies import StrategyManager
from src.utils.risk_management import RiskManager
from src.utils.config import config

def setup_logging():
    """Setup logging configuration"""
    # Remove default logger
    logger.remove()
    
    # Add console logger
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=config.log_level
    )
    
    # Add file logger
    os.makedirs("logs", exist_ok=True)
    logger.add(
        "logs/trading_agent_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )

def create_default_configs():
    """Create default configuration files if they don't exist"""
    os.makedirs("config", exist_ok=True)
    
    # Portfolio configuration
    portfolio_config_path = "config/portfolio_config.json"
    if not os.path.exists(portfolio_config_path):
        default_portfolio = {
            "USDC": 0.25,
            "WETH": 0.50,
            "WBTC": 0.25
        }
        with open(portfolio_config_path, 'w') as f:
            json.dump(default_portfolio, f, indent=2)
        logger.info(f"Created default portfolio config: {portfolio_config_path}")
    
    # Strategy configuration
    strategy_config_path = "config/strategy_config.json"
    if not os.path.exists(strategy_config_path):
        default_strategies = {
            "active_strategies": ["momentum", "volatility"],
            "strategy_weights": {
                "momentum": 0.4,
                "mean_reversion": 0.3,
                "volatility": 0.3
            },
            "rebalance_threshold": 0.02,
            "risk_management": {
                "max_position_size": 0.3,
                "stop_loss_percentage": 0.05,
                "max_daily_loss": 0.05
            }
        }
        with open(strategy_config_path, 'w') as f:
            json.dump(default_strategies, f, indent=2)
        logger.info(f"Created default strategy config: {strategy_config_path}")

def run_basic_agent():
    """Run the basic trading agent"""
    logger.info("Starting Basic Trading Agent...")
    
    agent = BasicTradingAgent()
    
    # Show agent info
    info = agent.get_agent_info()
    if info.get("success"):
        agent_data = info.get("agent", {})
        logger.info(f"Agent: {agent_data.get('name', 'Unknown')}")
        logger.info(f"Status: {agent_data.get('status', 'Unknown')}")
        logger.info(f"Verified: {agent_data.get('isVerified', False)}")
    
    # Run single cycle
    agent.run_single_cycle()

def run_portfolio_manager():
    """Run the advanced portfolio manager"""
    logger.info("Starting Advanced Portfolio Manager...")
    
    manager = AdvancedPortfolioManager()
    
    # Show current status
    logger.info("=== Portfolio Manager Status ===")
    status = manager.get_portfolio_status()
    logger.info(f"Total Portfolio Value: ${status['total_value']:.2f}")
    
    for symbol, data in status["portfolio"].items():
        logger.info(f"{symbol}: {data['allocation']:.1%} (${data['value']:.2f})")
    
    # Run continuously
    manager.run_continuous()

def run_strategy_test():
    """Test trading strategies"""
    logger.info("Testing Trading Strategies...")
    
    from src.data.market_data import MarketDataProvider
    
    # Get market data
    market_data_provider = MarketDataProvider()
    symbols = ["WETH", "WBTC", "USDC"]
    
    market_data = {}
    for symbol in symbols:
        data = market_data_provider.get_market_data(symbol)
        if data:
            market_data[symbol] = data
    
    if not market_data:
        logger.error("Could not fetch market data for strategy testing")
        return
    
    # Test strategies
    strategy_manager = StrategyManager()
    
    logger.info("=== Market Data ===")
    for symbol, data in market_data.items():
        logger.info(f"{symbol}: ${data['price']:.2f} (24h: {data['price_change_24h']:.2f}%, 7d: {data['price_change_7d']:.2f}%)")
    
    logger.info("=== Strategy Signals ===")
    combined_signals = strategy_manager.get_combined_signals(market_data)
    
    for symbol, signal in combined_signals.items():
        logger.info(f"{symbol}: {signal.upper()}")
    
    # Test individual strategies
    for strategy_name in strategy_manager.strategies.keys():
        logger.info(f"=== {strategy_name.title()} Strategy ===")
        allocation = strategy_manager.get_strategy_allocation(strategy_name, market_data, 10000)
        for symbol, weight in allocation.items():
            logger.info(f"{symbol}: {weight:.1%}")

def run_risk_test():
    """Test risk management system"""
    logger.info("Testing Risk Management System...")
    
    risk_manager = RiskManager()
    
    # Simulate some trades
    import time
    trades = [
        ("WETH", "buy", 0.5, 2000, True),
        ("WBTC", "buy", 0.1, 45000, True),
        ("WETH", "sell", 0.2, 2100, True),
        ("WBTC", "sell", 0.05, 44000, False),
    ]
    
    for symbol, side, amount, price, success in trades:
        risk_manager.record_trade(symbol, side, amount, price, success)
        time.sleep(1)
    
    # Get risk metrics
    metrics = risk_manager.get_risk_metrics()
    logger.info("=== Risk Metrics ===")
    for key, value in metrics.items():
        if isinstance(value, float):
            logger.info(f"{key}: {value:.4f}")
        else:
            logger.info(f"{key}: {value}")
    
    # Test risk checks
    logger.info("=== Risk Checks ===")
    valid, msg = risk_manager.validate_trade("WETH", "buy", 1.0, 2000, 10000)
    logger.info(f"Trade validation: {valid} - {msg}")
    
    should_reduce, reason = risk_manager.should_reduce_risk()
    logger.info(f"Should reduce risk: {should_reduce} - {reason}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Recall Network Trading Agent")
    parser.add_argument(
        "mode",
        choices=["basic", "portfolio", "strategy-test", "risk-test"],
        help="Operating mode"
    )
    parser.add_argument(
        "--config",
        default="config/portfolio_config.json",
        help="Portfolio configuration file"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Setup
    setup_logging()
    create_default_configs()
    
    # Validate API key
    if not config.recall_api_key:
        logger.error("RECALL_API_KEY not found in environment variables")
        logger.error("Please set your API key in .env file")
        sys.exit(1)
    
    logger.info(f"Starting Recall Trading Agent in {args.mode} mode")
    logger.info(f"Environment: {config.environment}")
    
    try:
        if args.mode == "basic":
            run_basic_agent()
        elif args.mode == "portfolio":
            run_portfolio_manager()
        elif args.mode == "strategy-test":
            run_strategy_test()
        elif args.mode == "risk-test":
            run_risk_test()
    
    except KeyboardInterrupt:
        logger.info("Trading agent stopped by user")
    except Exception as e:
        logger.error(f"Error running trading agent: {e}")
        raise

if __name__ == "__main__":
    main()
