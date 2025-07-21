# Contributing to Recall Network Trading Agent

Thank you for your interest in contributing to the Recall Network Trading Agent! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title** describing the issue
- **Detailed description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Environment details** (Python version, OS, etc.)
- **Log files** (sanitized, no API keys)
- **Screenshots** if applicable

### 💡 Suggesting Features

Feature suggestions are welcome! Please:

- **Check existing issues** for similar suggestions
- **Describe the feature** clearly and concisely
- **Explain the use case** and benefits
- **Consider implementation** complexity
- **Provide examples** if possible

### 🔧 Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/recall-trading-agent.git
   cd recall-trading-agent
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # OR
   .venv\Scripts\activate     # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development tools
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # OR
   git checkout -b bugfix/issue-description
   ```

### 📝 Code Style Guidelines

#### Python Code Style
- Follow **PEP 8** style guide
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes
- Keep line length under **100 characters**
- Use **meaningful variable names**

#### Example:
```python
def calculate_portfolio_value(balances: Dict[str, float], 
                            prices: Dict[str, float]) -> float:
    """
    Calculate total portfolio value in USD.
    
    Args:
        balances: Token balances by symbol
        prices: Current prices by symbol in USD
        
    Returns:
        Total portfolio value in USD
        
    Raises:
        ValueError: If balances and prices don't match
    """
    total_value = 0.0
    for symbol, balance in balances.items():
        if symbol not in prices:
            raise ValueError(f"Price not found for {symbol}")
        total_value += balance * prices[symbol]
    
    return total_value
```

#### Import Organization
```python
# Standard library imports
import os
import json
from typing import Dict, List, Optional

# Third-party imports
import requests
import pandas as pd
from loguru import logger

# Local imports
from .config import config
from .risk_management import RiskManager
```

### 🧪 Testing Guidelines

#### Writing Tests
- Write tests for all new features
- Maintain or improve test coverage
- Use descriptive test names
- Test both success and failure cases

#### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src

# Run specific test file
python -m pytest tests/test_trading_strategies.py

# Run with verbose output
python -m pytest tests/ -v
```

#### Test Structure
```python
import pytest
from unittest.mock import Mock, patch

from src.strategies.trading_strategies import MomentumStrategy

class TestMomentumStrategy:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.strategy = MomentumStrategy()
    
    def test_generate_buy_signal(self):
        """Test momentum strategy generates buy signal for positive momentum."""
        market_data = {
            "WETH": {"price_change_7d": 10.0}  # 10% gain
        }
        
        signals = self.strategy.generate_signals(market_data)
        
        assert signals["WETH"] == "buy"
    
    def test_generate_sell_signal(self):
        """Test momentum strategy generates sell signal for negative momentum."""
        market_data = {
            "WETH": {"price_change_7d": -8.0}  # 8% loss
        }
        
        signals = self.strategy.generate_signals(market_data)
        
        assert signals["WETH"] == "sell"
```

### 📚 Documentation

#### Code Documentation
- Write clear docstrings for all public APIs
- Include parameter types and descriptions
- Document return values and exceptions
- Provide usage examples for complex functions

#### README Updates
- Update README.md for new features
- Add configuration examples
- Update troubleshooting section if needed
- Include new dependencies in setup instructions

### 🔄 Pull Request Process

1. **Before submitting:**
   - Ensure all tests pass
   - Update documentation
   - Add changelog entry
   - Rebase on latest main branch

2. **Pull request description:**
   - Clear title describing the change
   - Detailed description of what was changed
   - Link to related issues
   - Screenshots for UI changes
   - Testing instructions

3. **Review process:**
   - Automated tests must pass
   - Code review by maintainers
   - Address feedback promptly
   - Squash commits if requested

### 🎯 Areas for Contribution

#### High Priority
- **New Trading Strategies** - Implement additional algorithmic strategies
- **Backtesting Engine** - Historical strategy performance analysis
- **Enhanced Risk Management** - Advanced risk models and controls
- **Performance Optimization** - Speed and efficiency improvements

#### Medium Priority
- **Additional Data Sources** - New market data providers
- **Multi-Chain Support** - Solana, Polygon integration
- **Monitoring Dashboard** - Web-based real-time interface
- **Alert System** - Email/SMS notifications

#### Low Priority
- **Documentation Improvements** - Tutorials, examples, guides
- **Code Quality** - Refactoring, optimization
- **Testing** - Expand test coverage
- **DevOps** - CI/CD, deployment automation

### 📋 Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(strategies): add RSI-based trading strategy

Implements Relative Strength Index strategy with configurable
overbought/oversold thresholds.

Closes #123
```

```
fix(risk): correct position size calculation

Fixed bug where position sizes were calculated incorrectly
for tokens with different decimal places.

Fixes #456
```

### 🚀 Release Process

1. **Version Bumping**
   - Follow semantic versioning (MAJOR.MINOR.PATCH)
   - Update version in relevant files
   - Create changelog entry

2. **Testing**
   - Run full test suite
   - Test in sandbox environment
   - Verify all features work correctly

3. **Documentation**
   - Update README if needed
   - Update API documentation
   - Create release notes

### 📞 Getting Help

- **Discord**: [discord.recall.network](http://discord.recall.network)
- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion

### 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Recall Network Trading Agent! 🚀
