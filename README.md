# 🤖 Recall Network Trading Agent

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Recall%20Network-purple.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)

*A sophisticated cryptocurrency trading bot built for the Recall Network platform*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🔧 Configuration](#-configuration) • [🛡️ Safety](#-safety-features) • [📊 Strategies](#-trading-strategies)

</div>

---

## 🌟 Overview

The **Recall Network Trading Agent** is a professional-grade cryptocurrency trading bot designed specifically for the Recall Network competition platform. It combines cutting-edge AI technology with robust risk management to deliver automated, intelligent trading strategies.

### ✨ Key Highlights

- 🧠 **AI-Powered Decision Making** - Leverages OpenAI GPT-4 for market analysis and strategic allocation
- 📈 **Multi-Strategy Framework** - Implements momentum, mean reversion, and volatility-based trading strategies
- 🛡️ **Enterprise-Grade Risk Management** - Comprehensive position sizing, stop-loss, and exposure controls
- 🔄 **Automated Portfolio Rebalancing** - Maintains optimal allocations with configurable drift thresholds
- 📊 **Real-Time Market Intelligence** - Integrates multiple data sources for informed decision making
- 🧪 **Safe Sandbox Testing** - Risk-free testing environment with simulated funds
- 📝 **Professional Logging & Monitoring** - Detailed performance tracking and operational insights
- ⚡ **High-Performance Architecture** - Optimized for speed, reliability, and scalability

### 🎯 Perfect For

- **Algorithmic Traders** seeking to compete in Recall Network competitions
- **Portfolio Managers** wanting automated rebalancing and risk management
- **Crypto Enthusiasts** interested in systematic trading approaches
- **Developers** looking to build upon a robust trading framework
- **Researchers** studying automated trading strategies and AI integration

## 🚀 Quick Start

### 📋 Prerequisites

Before you begin, ensure you have the following:

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.8+ | Core runtime environment |
| **Git** | Latest | Version control and cloning |
| **Recall Network API Key** | - | Trading platform access ([Get yours here](https://register.recall.network)) |

### ⚡ One-Command Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/recall-trading-agent.git
cd recall-trading-agent

# Run the automated setup script
chmod +x setup_project.sh && ./setup_project.sh

# Activate the virtual environment
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows
```

### 🔑 API Key Configuration

1. **Copy the environment template:**
   ```bash
   cp .env.template .env
   ```

2. **Edit `.env` with your credentials:**
   ```bash
   # ===== REQUIRED =====
   RECALL_API_KEY=pk_live_your_actual_key_here

   # ===== OPTIONAL BUT RECOMMENDED =====
   OPENAI_API_KEY=sk-your_openai_key_here        # For AI features
   COINGECKO_API_KEY=your_coingecko_key_here     # For enhanced data

   # ===== CONFIGURATION =====
   ENVIRONMENT=sandbox                            # sandbox or production
   REBALANCE_THRESHOLD=0.02                      # 2% drift threshold
   TRADE_AMOUNT_USD=100                          # Base trade amount
   MAX_POSITION_SIZE=0.3                         # 30% max per position
   STOP_LOSS_PERCENTAGE=0.05                     # 5% stop loss
   ```

### 🎮 Launch Options

Choose your preferred mode of operation:

```bash
# 🔰 Beginner: Single-cycle basic agent
python main.py basic

# 🚀 Advanced: Continuous portfolio manager with AI
python main.py portfolio

# 🧪 Testing: Strategy backtesting and analysis
python main.py strategy-test

# 🛡️ Validation: Risk management system test
python main.py risk-test
```

### ✅ Verify Installation

Run a quick health check:

```bash
python -c "
from src.utils.recall_client import RecallClient
client = RecallClient()
print('✅ Installation successful!' if client.health_check() else '❌ Setup incomplete')
"
```

## 🔑 API Keys & External Services

### 🎯 Required Services

#### Recall Network API Key
<table>
<tr><td><strong>🔗 Registration</strong></td><td><a href="https://register.recall.network">register.recall.network</a></td></tr>
<tr><td><strong>💰 Cost</strong></td><td>Free for sandbox • Competition fees vary</td></tr>
<tr><td><strong>🎯 Purpose</strong></td><td>Core trading platform access</td></tr>
<tr><td><strong>📝 Format</strong></td><td><code>pk_live_...</code></td></tr>
<tr><td><strong>🔒 Security</strong></td><td>Never commit to version control</td></tr>
</table>

### 🚀 Optional Enhancements

#### OpenAI API Key (Recommended for AI Features)
<table>
<tr><td><strong>🔗 Registration</strong></td><td><a href="https://platform.openai.com/api-keys">platform.openai.com/api-keys</a></td></tr>
<tr><td><strong>💰 Cost</strong></td><td>$0.01-0.10 per analysis • Pay-per-use</td></tr>
<tr><td><strong>🎯 Purpose</strong></td><td>AI market analysis • Strategy optimization</td></tr>
<tr><td><strong>📝 Format</strong></td><td><code>sk-proj-...</code> or <code>sk-...</code></td></tr>
<tr><td><strong>✨ Features</strong></td><td>GPT-4 powered allocation suggestions</td></tr>
</table>

#### CoinGecko API Key (Enhanced Market Data)
<table>
<tr><td><strong>🔗 Registration</strong></td><td><a href="https://www.coingecko.com/en/api">coingecko.com/en/api</a></td></tr>
<tr><td><strong>💰 Cost</strong></td><td>Free tier: 30 calls/min • Pro: Higher limits</td></tr>
<tr><td><strong>🎯 Purpose</strong></td><td>Real-time price data • Market analytics</td></tr>
<tr><td><strong>📊 Data</strong></td><td>Price history • Volume • Market cap</td></tr>
<tr><td><strong>⚡ Limits</strong></td><td>Free: 30/min • Pro: 500+/min</td></tr>
</table>

## 🔧 Configuration

### 📊 Portfolio Allocation (`config/portfolio_config.json`)

Define your target asset allocation percentages:

```json
{
  "USDC": 0.25,    // 25% - Stable coin for safety
  "WETH": 0.50,    // 50% - Ethereum exposure
  "WBTC": 0.25     // 25% - Bitcoin exposure
}
```

**💡 Tips:**
- Allocations must sum to 1.0 (100%)
- Minimum 5% per asset recommended
- USDC acts as a safe haven during volatility
- AI can suggest dynamic adjustments

### ⚙️ Strategy Configuration (`config/strategy_config.json`)

Control trading strategies and risk parameters:

```json
{
  "active_strategies": ["momentum", "volatility"],
  "strategy_weights": {
    "momentum": 0.4,        // 40% weight to momentum signals
    "mean_reversion": 0.3,  // 30% weight to mean reversion
    "volatility": 0.3       // 30% weight to volatility analysis
  },
  "rebalance_threshold": 0.02,  // Trigger rebalancing at 2% drift
  "risk_management": {
    "max_position_size": 0.3,      // 30% maximum per position
    "stop_loss_percentage": 0.05,   // 5% stop loss
    "max_daily_loss": 0.05,         // 5% daily loss limit
    "max_trades_per_hour": 10,      // Rate limiting
    "min_trade_interval": 60        // Minimum seconds between trades
  }
}
```

### 🌍 Environment Variables (`.env`)

```bash
# ===== CORE CONFIGURATION =====
RECALL_API_KEY=pk_live_your_key_here
ENVIRONMENT=sandbox                    # sandbox | production
LOG_LEVEL=INFO                        # DEBUG | INFO | WARNING | ERROR

# ===== TRADING PARAMETERS =====
REBALANCE_THRESHOLD=0.02              # 2% drift threshold
TRADE_AMOUNT_USD=100                  # Base trade amount
MAX_POSITION_SIZE=0.3                 # 30% max position
STOP_LOSS_PERCENTAGE=0.05             # 5% stop loss

# ===== OPTIONAL INTEGRATIONS =====
OPENAI_API_KEY=sk-your_key_here       # AI features
COINGECKO_API_KEY=your_key_here       # Enhanced market data

# ===== SCHEDULING =====
REBALANCE_TIME=09:00                  # Daily rebalance time (24h format)
PRICE_UPDATE_INTERVAL=300             # Price update frequency (seconds)
```

## 📊 Trading Strategies

Our multi-strategy framework combines different market approaches for robust performance:

### 🚀 Momentum Strategy
<table>
<tr><td><strong>📈 Logic</strong></td><td>Follows strong price trends and market momentum</td></tr>
<tr><td><strong>🎯 Buy Signal</strong></td><td>Tokens with >5% gain in 7 days</td></tr>
<tr><td><strong>📉 Sell Signal</strong></td><td>Tokens with <-5% loss in 7 days</td></tr>
<tr><td><strong>💰 Allocation</strong></td><td>Equal weight among buy signals, 20% cash buffer</td></tr>
<tr><td><strong>⏱️ Timeframe</strong></td><td>7-day momentum analysis</td></tr>
<tr><td><strong>🎲 Risk Level</strong></td><td>Medium-High (trend following)</td></tr>
</table>

### 🔄 Mean Reversion Strategy
<table>
<tr><td><strong>📈 Logic</strong></td><td>Buys oversold assets expecting price recovery</td></tr>
<tr><td><strong>🎯 Buy Signal</strong></td><td>Tokens down >15% in 30 days</td></tr>
<tr><td><strong>📉 Sell Signal</strong></td><td>Tokens up >15% in 30 days</td></tr>
<tr><td><strong>💰 Allocation</strong></td><td>Conservative sizing, 30% cash buffer</td></tr>
<tr><td><strong>⏱️ Timeframe</strong></td><td>30-day price analysis</td></tr>
<tr><td><strong>🎲 Risk Level</strong></td><td>Medium (contrarian approach)</td></tr>
</table>

### 📊 Volatility Strategy
<table>
<tr><td><strong>📈 Logic</strong></td><td>Adjusts exposure based on market volatility</td></tr>
<tr><td><strong>🎯 Buy Signal</strong></td><td>Low volatility (expecting breakouts)</td></tr>
<tr><td><strong>📉 Sell Signal</strong></td><td>High volatility (risk reduction)</td></tr>
<tr><td><strong>💰 Allocation</strong></td><td>Dynamic sizing based on volatility levels</td></tr>
<tr><td><strong>⏱️ Timeframe</strong></td><td>Real-time volatility calculation</td></tr>
<tr><td><strong>🎲 Risk Level</strong></td><td>Low-Medium (volatility adaptive)</td></tr>
</table>

### 🤖 AI-Enhanced Strategy (Optional)
<table>
<tr><td><strong>📈 Logic</strong></td><td>GPT-4 powered market analysis and allocation</td></tr>
<tr><td><strong>🎯 Features</strong></td><td>Market sentiment • Risk assessment • Dynamic allocation</td></tr>
<tr><td><strong>📊 Analysis</strong></td><td>Multi-factor market condition evaluation</td></tr>
<tr><td><strong>💰 Allocation</strong></td><td>AI-suggested portfolio weights with constraints</td></tr>
<tr><td><strong>⏱️ Frequency</strong></td><td>Weekly strategy reviews</td></tr>
<tr><td><strong>🎲 Risk Level</strong></td><td>Adaptive (AI-determined)</td></tr>
</table>

## 🛡️ Risk Management System

Our comprehensive risk management framework protects your capital through multiple layers of protection:

### 🎯 Position Controls
| Feature | Default | Purpose |
|---------|---------|---------|
| **Max Position Size** | 30% | Prevents over-concentration in single assets |
| **Min Position Size** | 5% | Ensures meaningful diversification |
| **Stop Loss** | 5% | Automatic exit on significant losses |
| **Position Limits** | Per-token caps | Enforces diversification requirements |

### 📊 Portfolio Protection
| Feature | Default | Purpose |
|---------|---------|---------|
| **Daily Loss Limit** | 5% | Halts trading on significant daily losses |
| **Drawdown Monitoring** | Real-time | Tracks portfolio decline from peaks |
| **Volatility Adjustment** | Dynamic | Reduces exposure during high volatility |
| **Emergency Stop** | Automatic | Immediate halt on critical conditions |

### ⏱️ Trading Controls
| Feature | Default | Purpose |
|---------|---------|---------|
| **Trade Frequency** | 10/hour max | Prevents over-trading and API abuse |
| **Min Trade Interval** | 60 seconds | Ensures deliberate trade execution |
| **Rate Limiting** | API-compliant | Respects platform limitations |
| **Validation Layers** | Multi-stage | Comprehensive pre-trade checks |

### 🚨 Emergency Protocols
- **Automatic Halt**: Triggered by severe losses (>7% daily) or poor performance (<30% success rate)
- **Risk Reduction**: Automatic position sizing reduction during adverse conditions
- **Manual Override**: Emergency stop functionality for immediate intervention
- **Recovery Mode**: Gradual re-entry after emergency stops

## 📁 Project Architecture

```
recall-trading-agent/
├── 🚀 main.py                     # Main entry point & CLI interface
├── 📋 requirements.txt            # Python dependencies
├── 🔧 setup_project.sh           # Automated setup script
├── 📖 README.md                  # This comprehensive guide
├── 🔒 .env.template              # Environment variables template
├── 🔒 .gitignore                 # Git ignore rules
│
├── 📂 src/                       # Source code directory
│   ├── 🤖 agents/               # Trading agent implementations
│   │   ├── basic_agent.py        # → Simple portfolio rebalancing
│   │   └── portfolio_manager.py  # → Advanced AI-powered manager
│   │
│   ├── 📊 strategies/           # Trading strategy modules
│   │   └── trading_strategies.py # → Momentum, mean reversion, volatility
│   │
│   ├── 🛠️ utils/                # Core utilities and services
│   │   ├── config.py            # → Configuration management
│   │   ├── recall_client.py     # → Recall Network API client
│   │   └── risk_management.py   # → Risk controls and safety
│   │
│   └── 📈 data/                 # Data providers and processing
│       └── market_data.py       # → CoinGecko integration & analysis
│
├── ⚙️ config/                   # Configuration files
│   ├── portfolio_config.json    # → Asset allocation targets
│   └── strategy_config.json     # → Strategy parameters & weights
│
├── 📝 logs/                     # Application logs (auto-created)
│   ├── trading_agent_YYYY-MM-DD.log  # → Daily log files
│   └── ...                      # → Historical logs (30-day retention)
│
└── 🧪 tests/                    # Test suite (future expansion)
    └── ...                      # → Unit tests and integration tests
```

### 🏗️ Architecture Highlights

- **🔌 Modular Design**: Each component is independently testable and replaceable
- **🔄 Event-Driven**: Reactive architecture responding to market conditions
- **📊 Data Pipeline**: Clean separation between data ingestion, processing, and trading
- **🛡️ Safety First**: Risk management integrated at every level
- **📈 Scalable**: Easy to add new strategies, data sources, and features

## 💻 Usage Examples & Code Snippets

### 🔰 Basic Trading Agent
Perfect for getting started with simple portfolio rebalancing:

```python
from src.agents.basic_agent import BasicTradingAgent

# Initialize the basic agent
agent = BasicTradingAgent()

# Check agent status
info = agent.get_agent_info()
print(f"Agent: {info['agent']['name']}")
print(f"Verified: {info['agent']['isVerified']}")

# Get current portfolio status
status = agent.get_portfolio_status()
print(f"Total Value: ${status['total_value']:.2f}")

# Run a single rebalancing cycle
agent.run_single_cycle()
```

### 🚀 Advanced Portfolio Manager
For continuous operation with AI integration:

```python
from src.agents.portfolio_manager import AdvancedPortfolioManager

# Initialize advanced manager
manager = AdvancedPortfolioManager()

# Run continuous operation with scheduling
manager.run_continuous()  # Includes daily rebalancing, AI reviews, monitoring
```

### 📊 Custom Strategy Development
Build your own trading strategies:

```python
from src.strategies.trading_strategies import StrategyManager, TradingStrategy

# Use existing strategies
strategy_manager = StrategyManager()
signals = strategy_manager.get_combined_signals(market_data)

# Create custom strategy
class MyCustomStrategy(TradingStrategy):
    def generate_signals(self, market_data):
        # Your custom logic here
        return {"WETH": "buy", "WBTC": "hold", "USDC": "hold"}

    def calculate_position_sizes(self, signals, portfolio_value):
        # Your position sizing logic
        return {"WETH": 0.6, "WBTC": 0.3, "USDC": 0.1}

# Add to strategy manager
strategy_manager.add_strategy("my_strategy", MyCustomStrategy("MyStrategy"))
```

### 🛡️ Risk Management Integration
Implement custom risk controls:

```python
from src.utils.risk_management import RiskManager

risk_manager = RiskManager()

# Validate trade before execution
valid, message = risk_manager.validate_trade(
    symbol="WETH",
    side="buy",
    amount=1.0,
    current_price=2000,
    portfolio_value=10000
)

if valid:
    # Execute trade
    print("Trade approved")
else:
    print(f"Trade rejected: {message}")

# Get risk metrics
metrics = risk_manager.get_risk_metrics()
print(f"Success rate: {metrics['success_rate_24h']:.2%}")
```

## 📊 Monitoring & Analytics

### 📈 Real-Time Dashboard
- **Console Output**: Live trading status, portfolio updates, and trade confirmations
- **Performance Metrics**: Real-time P&L, success rates, and risk indicators
- **Market Analysis**: Current prices, trends, and volatility measurements
- **Strategy Signals**: Live strategy recommendations and signal strength

### 📝 Comprehensive Logging
```
logs/
├── trading_agent_2024-01-15.log    # Daily trading activities
├── trading_agent_2024-01-14.log    # Historical logs (30-day retention)
└── ...
```

**Log Levels:**
- `DEBUG`: Detailed execution flow and variable states
- `INFO`: Trading decisions, portfolio updates, and system status
- `WARNING`: Risk alerts, API issues, and recoverable errors
- `ERROR`: Critical failures and emergency stops

### 📊 Performance Tracking
- **Portfolio Metrics**: Total value, allocation drift, and rebalancing frequency
- **Risk Analytics**: Daily P&L, drawdown analysis, and volatility exposure
- **Strategy Performance**: Individual strategy success rates and contribution
- **Trade History**: Complete audit trail with timestamps and reasoning

## 🛡️ Safety & Security Features

### 🧪 Sandbox Environment
- **Risk-Free Testing**: All operations use simulated funds on Ethereum mainnet fork
- **Real Market Conditions**: Authentic price feeds and market dynamics
- **No Financial Risk**: Zero possibility of real fund loss during development
- **Unlimited Testing**: Experiment freely with strategies and configurations

### 🔒 Security Measures
- **API Key Protection**: Environment variable storage with .gitignore protection
- **Rate Limiting**: Intelligent API call management to prevent service blocking
- **Input Validation**: Multi-layer validation before any trade execution
- **Error Recovery**: Graceful handling of network issues and API failures

### ✅ Validation Pipeline
1. **Pre-Trade Checks**: Position size, risk limits, and frequency validation
2. **Market Validation**: Price sanity checks and liquidity verification
3. **Risk Assessment**: Portfolio impact analysis and stop-loss evaluation
4. **Final Approval**: Multi-factor confirmation before execution

## 🔧 Troubleshooting Guide

### 🚨 Common Issues & Solutions

#### 🔑 API Key Problems
| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Invalid API Key** | `401 Unauthorized` errors | Verify key format: `pk_live_...` |
| **Wrong Environment** | Unexpected behavior | Check `ENVIRONMENT=sandbox` in `.env` |
| **Key Not Found** | `RECALL_API_KEY not found` | Ensure `.env` file exists and is loaded |

#### 🌐 Connection Issues
| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Network Timeout** | `Connection timeout` errors | Check internet connection and firewall |
| **Rate Limiting** | `429 Too Many Requests` | Reduce trade frequency or upgrade API plan |
| **API Downtime** | `503 Service Unavailable` | Check Recall Network status page |

#### 💰 Balance & Trading Issues
| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Insufficient Funds** | `Insufficient balance` errors | Use [Recall Network faucet](https://faucet.recall.network) |
| **No USDC Balance** | Cannot execute trades | Ensure USDC balance for base currency |
| **Trade Failures** | Trades not executing | Check position sizes and risk limits |

#### 🐍 Python Environment Issues
| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Import Errors** | `ModuleNotFoundError` | Activate virtual environment: `source .venv/bin/activate` |
| **Version Conflicts** | Dependency errors | Reinstall: `pip install -r requirements.txt --force-reinstall` |
| **Permission Errors** | File access denied | Check file permissions and virtual environment |

### 🔍 Diagnostic Commands

```bash
# Check API connectivity
python -c "from src.utils.recall_client import RecallClient; print('✅ Connected' if RecallClient().health_check() else '❌ Failed')"

# Verify environment setup
python -c "from src.utils.config import config; print(f'Environment: {config.environment}')"

# Test market data
python -c "from src.data.market_data import MarketDataProvider; print(MarketDataProvider().get_price('WETH'))"

# Check portfolio status
python main.py basic --dry-run
```

### 📞 Getting Help

#### 📚 Documentation Resources
- **Recall Network Docs**: [docs.recall.network](https://docs.recall.network)
- **API Reference**: [docs.recall.network/api-reference](https://docs.recall.network/api-reference)
- **Competition Guide**: [docs.recall.network/competitions](https://docs.recall.network/competitions)

#### 🤝 Community Support
- **Discord**: [discord.recall.network](http://discord.recall.network)
- **GitHub Issues**: Report bugs and feature requests
- **Twitter**: [@recallnet](https://x.com/recallnet) for updates

#### 🔍 Debug Information
When seeking help, include:
1. **Log files** from `logs/` directory
2. **Environment details** (Python version, OS)
3. **Configuration** (sanitized, no API keys)
4. **Error messages** (full stack traces)

## 🚀 Advanced Features & Roadmap

### 🎯 Current Capabilities
- ✅ **Multi-Strategy Trading** - Momentum, mean reversion, volatility strategies
- ✅ **AI Integration** - GPT-4 powered market analysis and allocation
- ✅ **Risk Management** - Comprehensive position and portfolio controls
- ✅ **Real-Time Data** - CoinGecko and Recall Network integration
- ✅ **Automated Scheduling** - Daily rebalancing and monitoring
- ✅ **Sandbox Testing** - Risk-free development environment

### 🔮 Planned Enhancements
- 🔄 **Backtesting Engine** - Historical strategy performance analysis
- 📊 **Advanced Analytics** - Sharpe ratio, alpha/beta calculations
- 🌐 **Multi-Chain Support** - Solana, Polygon, and other networks
- 📱 **Web Dashboard** - Real-time monitoring interface
- 🔔 **Alert System** - Email/SMS notifications for important events
- 🤖 **ML Models** - Custom machine learning strategy development

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🛠️ Development Setup
```bash
# Fork the repository and clone your fork
git clone https://github.com/yourusername/recall-trading-agent.git
cd recall-trading-agent

# Create a development branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Submit a pull request
```

### 📝 Contribution Guidelines
- **Code Style**: Follow PEP 8 and use type hints
- **Testing**: Add tests for new features
- **Documentation**: Update README and docstrings
- **Commit Messages**: Use conventional commit format

### 🎯 Areas for Contribution
- **New Trading Strategies** - Implement additional algorithmic strategies
- **Data Sources** - Integrate new market data providers
- **Risk Models** - Enhance risk management capabilities
- **UI/UX** - Develop monitoring dashboards and interfaces
- **Testing** - Expand test coverage and scenarios

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### 📋 License Summary
- ✅ **Commercial Use** - Use in commercial projects
- ✅ **Modification** - Modify and distribute
- ✅ **Distribution** - Share with others
- ✅ **Private Use** - Use for personal projects
- ❌ **Liability** - No warranty or liability
- ❌ **Trademark Use** - No trademark rights granted

## ⚠️ Important Disclaimers

### 🚨 Risk Warning
> **CRYPTOCURRENCY TRADING INVOLVES SUBSTANTIAL RISK OF LOSS**
>
> This software is provided for **educational and testing purposes only**. Cryptocurrency markets are highly volatile and unpredictable. Past performance does not guarantee future results.

### 🛡️ Liability Disclaimer
- **No Financial Advice**: This software does not constitute financial advice
- **Use at Your Own Risk**: Users are responsible for their own trading decisions
- **No Guarantees**: No warranty of profitability or performance
- **Loss of Funds**: Never trade with funds you cannot afford to lose

### 🔒 Security Notice
- **API Key Security**: Keep your API keys secure and never share them
- **Sandbox First**: Always test thoroughly in sandbox before live trading
- **Regular Updates**: Keep the software updated for security patches
- **Backup Strategies**: Maintain manual oversight of automated trading

---

<div align="center">

### 🌟 Star this repository if you find it useful!

**Built with ❤️ for the Recall Network community**

[🚀 Get Started](#-quick-start) • [📖 Documentation](#-documentation) • [🤝 Contribute](#-contributing) • [💬 Discord](http://discord.recall.network)

</div>
