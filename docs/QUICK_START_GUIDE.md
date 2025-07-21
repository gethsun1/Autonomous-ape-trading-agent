# 🚀 Quick Start Guide - Recall Network Trading Agent

Get your trading bot up and running in under 10 minutes!

## 📋 Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Recall Network account created
- [ ] API key obtained from [register.recall.network](https://register.recall.network)

## ⚡ 5-Minute Setup

### Step 1: Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/recall-trading-agent.git
cd recall-trading-agent

# Run automated setup
chmod +x setup_project.sh && ./setup_project.sh

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows
```

### Step 2: Configure API Keys (1 minute)

```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your API key
# Replace 'your_key_here' with your actual Recall Network API key
```

**Required in `.env`:**
```bash
RECALL_API_KEY=pk_live_your_actual_key_here
ENVIRONMENT=sandbox
```

### Step 3: Test Connection (1 minute)

```bash
# Quick connectivity test
python -c "
from src.utils.recall_client import RecallClient
client = RecallClient()
print('✅ Connected to Recall Network!' if client.health_check() else '❌ Connection failed')
"
```

### Step 4: Run Your First Trade (1 minute)

```bash
# Run basic trading agent
python main.py basic
```

**Expected output:**
```
🚀 Starting Basic Trading Agent...
Agent: Your Agent Name
Status: active
Verified: True
=== Starting Trading Cycle ===
Portfolio value: $1000.00
USDC: 0.400 ($400.00)
WETH: 0.400 ($400.00)
WBTC: 0.200 ($200.00)
Portfolio is already balanced within threshold
=== Trading Cycle Complete ===
```

## 🎯 What Just Happened?

1. **Setup Complete**: Virtual environment created with all dependencies
2. **API Connected**: Successfully connected to Recall Network sandbox
3. **Portfolio Analyzed**: Current holdings and allocations reviewed
4. **Rebalancing Check**: Determined if portfolio needs adjustment
5. **Safe Operation**: All trades executed in risk-free sandbox environment

## 🚀 Next Steps

### Option A: Basic Usage (Recommended for Beginners)
```bash
# Run single rebalancing cycle
python main.py basic

# Test different strategies
python main.py strategy-test

# Check risk management
python main.py risk-test
```

### Option B: Advanced Continuous Operation
```bash
# Run advanced portfolio manager with AI
python main.py portfolio
```

This will start continuous operation with:
- ✅ Daily automated rebalancing
- ✅ Hourly portfolio monitoring  
- ✅ AI-powered strategy adjustments (if OpenAI key provided)
- ✅ Real-time risk management

## 🔧 Customization

### Modify Portfolio Allocation
Edit `config/portfolio_config.json`:
```json
{
  "USDC": 0.30,    // 30% stable coin
  "WETH": 0.50,    // 50% Ethereum
  "WBTC": 0.20     // 20% Bitcoin
}
```

### Adjust Risk Settings
Edit `.env`:
```bash
REBALANCE_THRESHOLD=0.02      # Trigger rebalancing at 2% drift
MAX_POSITION_SIZE=0.3         # Maximum 30% per position
STOP_LOSS_PERCENTAGE=0.05     # 5% stop loss
```

## 🛡️ Safety Features Active

- **Sandbox Environment**: No real money at risk
- **Position Limits**: Maximum 30% per asset
- **Stop Loss**: 5% automatic protection
- **Daily Loss Limit**: 5% maximum daily loss
- **Trade Frequency**: Limited to prevent over-trading

## 📊 Monitoring Your Bot

### Real-Time Console Output
Watch live trading decisions and portfolio updates in your terminal.

### Log Files
Detailed logs saved to `logs/trading_agent_YYYY-MM-DD.log`

### Portfolio Status
Check current status anytime:
```bash
python -c "
from src.agents.basic_agent import BasicTradingAgent
agent = BasicTradingAgent()
status = agent.get_portfolio_status()
print(f'Portfolio Value: ${status[\"total_value\"]:.2f}')
"
```

## 🆘 Troubleshooting

### Common Issues

**❌ "RECALL_API_KEY not found"**
- Solution: Ensure `.env` file exists and contains your API key

**❌ "Connection timeout"**
- Solution: Check internet connection and try again

**❌ "Insufficient balance"**
- Solution: Get sandbox funds from [faucet.recall.network](https://faucet.recall.network)

**❌ "ModuleNotFoundError"**
- Solution: Activate virtual environment: `source .venv/bin/activate`

### Get Help
- 📖 Full documentation in [README.md](../README.md)
- 💬 Join [Discord community](http://discord.recall.network)
- 🐛 Report issues on [GitHub](https://github.com/yourusername/recall-trading-agent/issues)

## 🎉 Congratulations!

You now have a fully functional cryptocurrency trading bot running on the Recall Network platform! 

### What's Next?
1. **Experiment** with different portfolio allocations
2. **Add AI features** by getting an OpenAI API key
3. **Monitor performance** and adjust strategies
4. **Join competitions** on the Recall Network platform
5. **Contribute** to the project and help improve it

---

**Happy Trading! 🚀**

*Remember: This is a sandbox environment with no real financial risk. Perfect for learning and experimentation!*
