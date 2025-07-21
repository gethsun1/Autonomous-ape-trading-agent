#!/bin/bash

# Recall Network Trading Agent Setup Script
echo "🚀 Setting up Recall Network Trading Agent..."

# Create project directory
mkdir -p recall-trading-agent
cd recall-trading-agent

# Initialize Git repository
git init
echo "*.env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".venv/" >> .gitignore
echo "logs/" >> .gitignore

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Create project structure
mkdir -p {src,config,logs,tests,docs}
mkdir -p src/{agents,strategies,utils,data}

# Create requirements.txt
cat > requirements.txt << EOF
requests>=2.31.0
python-dotenv>=1.0.0
schedule>=1.2.0
openai>=1.0.0
pandas>=2.0.0
numpy>=1.24.0
python-dateutil>=2.8.0
pydantic>=2.0.0
loguru>=0.7.0
EOF

# Install dependencies
pip install -r requirements.txt

# Create .env template
cat > .env.template << EOF
# Recall Network API Key (Required)
RECALL_API_KEY=pk_live_your_key_here

# OpenAI API Key (Optional)
OPENAI_API_KEY=sk-your_openai_key_here

# CoinGecko API Key (Optional)
COINGECKO_API_KEY=your_coingecko_key_here

# Configuration
ENVIRONMENT=sandbox
LOG_LEVEL=INFO
REBALANCE_THRESHOLD=0.02
TRADE_AMOUNT_USD=100
MAX_POSITION_SIZE=0.3
STOP_LOSS_PERCENTAGE=0.05
EOF

echo "✅ Project setup complete!"
echo "📝 Next steps:"
echo "1. Copy .env.template to .env and fill in your API keys"
echo "2. Activate virtual environment: source .venv/bin/activate"
echo "3. Run the basic trading agent: python src/agents/basic_agent.py"
