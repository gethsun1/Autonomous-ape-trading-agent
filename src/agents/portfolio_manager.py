"""
Advanced Portfolio Manager with AI Integration and Scheduling
"""
import json
import time
import schedule
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available, AI features disabled")

from .basic_agent import BasicTradingAgent
from ..utils.config import config

class AdvancedPortfolioManager(BasicTradingAgent):
    """Advanced portfolio manager with AI-powered strategy adjustments"""
    
    def __init__(self, portfolio_config_path: str = "config/portfolio_config.json"):
        super().__init__(portfolio_config_path)
        
        # Initialize OpenAI client if available
        self.openai_client = None
        if OPENAI_AVAILABLE and config.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=config.openai_api_key)
            logger.info("OpenAI client initialized for AI features")
        
        # Scheduling setup
        self.setup_scheduler()
        
        logger.info("Advanced Portfolio Manager initialized")
    
    def setup_scheduler(self):
        """Setup automated scheduling for portfolio management"""
        # Daily rebalancing
        schedule.every().day.at(config.rebalance_time).do(self.scheduled_rebalance)
        
        # Weekly AI strategy review (if enabled)
        if self.openai_client:
            schedule.every().monday.at("08:00").do(self.ai_strategy_review)
        
        # Hourly portfolio monitoring
        schedule.every().hour.do(self.monitor_portfolio)
        
        logger.info(f"Scheduler configured - rebalancing at {config.rebalance_time} daily")
    
    def ai_analyze_market_conditions(self) -> Dict[str, any]:
        """Use AI to analyze current market conditions"""
        if not self.openai_client:
            return {"analysis": "AI analysis not available", "confidence": 0}
        
        try:
            # Get current portfolio status
            portfolio_status = self.get_portfolio_status()
            
            # Get market data for analysis
            symbols = list(portfolio_status["portfolio"].keys())
            market_data = {}
            for symbol in symbols:
                market_data[symbol] = self.market_data.get_market_data(symbol)
            
            # Prepare prompt for AI analysis
            prompt = f"""
            Analyze the current cryptocurrency market conditions and provide insights for portfolio management.
            
            Current Portfolio:
            {json.dumps(portfolio_status, indent=2)}
            
            Market Data:
            {json.dumps(market_data, indent=2)}
            
            Please provide:
            1. Market sentiment analysis
            2. Risk assessment
            3. Recommended portfolio adjustments (if any)
            4. Confidence level (0-100)
            
            Respond in JSON format with keys: sentiment, risk_level, recommendations, confidence, reasoning
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                analysis = json.loads(analysis_text.strip("```json\n").strip("```"))
                logger.info("AI market analysis completed")
                return analysis
            except json.JSONDecodeError:
                logger.warning("AI response was not valid JSON")
                return {
                    "analysis": analysis_text,
                    "confidence": 50,
                    "sentiment": "neutral"
                }
                
        except Exception as e:
            logger.error(f"Error in AI market analysis: {e}")
            return {"analysis": f"Error: {e}", "confidence": 0}
    
    def ai_suggest_allocation(self, current_allocation: Dict[str, float]) -> Dict[str, float]:
        """Use AI to suggest portfolio allocation adjustments"""
        if not self.openai_client:
            return current_allocation
        
        try:
            # Get market analysis
            market_analysis = self.ai_analyze_market_conditions()
            
            prompt = f"""
            Based on current market conditions and analysis, suggest an optimal portfolio allocation.
            
            Current Allocation:
            {json.dumps(current_allocation, indent=2)}
            
            Market Analysis:
            {json.dumps(market_analysis, indent=2)}
            
            Available tokens: USDC, WETH, WBTC
            
            Rules:
            - Allocations must sum to 1.0
            - Minimum allocation per token: 0.05 (5%)
            - Maximum allocation per token: 0.70 (70%)
            - USDC can be used as a safe haven (higher allocation in uncertain times)
            
            Respond with ONLY a JSON object with token symbols as keys and allocation percentages as values.
            Example: {{"USDC": 0.3, "WETH": 0.5, "WBTC": 0.2}}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            suggestion_text = response.choices[0].message.content.strip()
            
            # Clean and parse JSON
            suggestion_text = suggestion_text.strip("```json\n").strip("```").strip()
            suggested_allocation = json.loads(suggestion_text)
            
            # Validate allocation
            total = sum(suggested_allocation.values())
            if abs(total - 1.0) > 0.01:
                logger.warning(f"AI suggested allocation sums to {total}, normalizing...")
                suggested_allocation = {k: v/total for k, v in suggested_allocation.items()}
            
            # Check constraints
            for symbol, allocation in suggested_allocation.items():
                if allocation < 0.05:
                    logger.warning(f"AI suggested {allocation:.3f} for {symbol}, adjusting to minimum 0.05")
                    suggested_allocation[symbol] = 0.05
                elif allocation > 0.70:
                    logger.warning(f"AI suggested {allocation:.3f} for {symbol}, adjusting to maximum 0.70")
                    suggested_allocation[symbol] = 0.70
            
            # Renormalize after constraint adjustments
            total = sum(suggested_allocation.values())
            suggested_allocation = {k: v/total for k, v in suggested_allocation.items()}
            
            logger.info(f"AI suggested allocation: {suggested_allocation}")
            return suggested_allocation
            
        except Exception as e:
            logger.error(f"Error in AI allocation suggestion: {e}")
            return current_allocation
    
    def ai_strategy_review(self):
        """Perform AI-powered strategy review and update allocation"""
        try:
            logger.info("Starting AI strategy review...")
            
            # Load current target allocation
            current_allocation = self.load_target_allocation()
            
            # Get AI suggestion
            suggested_allocation = self.ai_suggest_allocation(current_allocation)
            
            # Calculate difference
            max_change = max(abs(suggested_allocation.get(k, 0) - current_allocation.get(k, 0)) 
                           for k in set(list(current_allocation.keys()) + list(suggested_allocation.keys())))
            
            # Only update if significant change suggested
            if max_change > 0.05:  # 5% threshold
                logger.info(f"AI suggests significant allocation change (max: {max_change:.3f})")
                
                # Save new allocation
                with open(self.portfolio_config_path, 'w') as f:
                    json.dump(suggested_allocation, f, indent=2)
                
                logger.info("Portfolio allocation updated based on AI recommendation")
                
                # Trigger immediate rebalancing
                self.rebalance_portfolio()
            else:
                logger.info("AI suggests minimal changes, keeping current allocation")
                
        except Exception as e:
            logger.error(f"Error in AI strategy review: {e}")
    
    def monitor_portfolio(self):
        """Monitor portfolio for significant changes or alerts"""
        try:
            status = self.get_portfolio_status()
            
            # Check for significant value changes
            # This could be enhanced with historical tracking
            logger.info(f"Portfolio monitoring - Total value: ${status['total_value']:.2f}")
            
            # Check if emergency rebalancing is needed (large drift)
            target_allocation = self.load_target_allocation()
            trades = self.calculate_rebalancing_trades(target_allocation)
            
            # If large drift detected, trigger emergency rebalancing
            large_drift_trades = [t for t in trades if abs(t["weight_diff"]) > config.rebalance_threshold * 2]
            if large_drift_trades:
                logger.warning(f"Large portfolio drift detected, triggering emergency rebalancing")
                self.rebalance_portfolio()
                
        except Exception as e:
            logger.error(f"Error in portfolio monitoring: {e}")
    
    def scheduled_rebalance(self):
        """Scheduled portfolio rebalancing"""
        logger.info("Starting scheduled portfolio rebalancing...")
        self.rebalance_portfolio()
    
    def run_continuous(self):
        """Run the portfolio manager continuously with scheduling"""
        logger.info("🚀 Starting Advanced Portfolio Manager in continuous mode...")
        logger.info("Press Ctrl+C to stop")
        
        try:
            # Run initial cycle
            self.run_single_cycle()
            
            # Start scheduled operations
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("Portfolio manager stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous operation: {e}")
            raise

if __name__ == "__main__":
    manager = AdvancedPortfolioManager()
    
    # Show current status
    print("\n=== Portfolio Manager Status ===")
    status = manager.get_portfolio_status()
    print(f"Total Portfolio Value: ${status['total_value']:.2f}")
    
    for symbol, data in status["portfolio"].items():
        print(f"{symbol}: {data['allocation']:.1%} (${data['value']:.2f})")
    
    print("\n=== Starting Continuous Operation ===")
    manager.run_continuous()
