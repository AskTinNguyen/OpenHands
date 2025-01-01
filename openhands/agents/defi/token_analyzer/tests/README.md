# Token Analysis Agent Testing Guide

This guide explains how to run both mock and real tests for the Token Analysis Agent.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Types](#test-types)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### API Keys Required
```
- Etherscan: For Ethereum blockchain data
- BSCScan: For BSC blockchain data
- Infura/Alchemy: For Ethereum node access
- CoinGecko Pro: For market data (higher rate limits)
- DexTools: For DEX data
```

### Node Access Required
```python
# Required RPC Endpoints:
{
    "ethereum": {
        "mainnet": "https://mainnet.infura.io/v3/YOUR_KEY",
        "testnet": "https://goerli.infura.io/v3/YOUR_KEY"
    },
    "bsc": {
        "mainnet": "https://bsc-dataseed.binance.org",
        "testnet": "https://data-seed-prebsc-1-s1.binance.org:8545"
    }
}
```

## Installation

1. Install Required Packages:
```bash
pip install web3  # For blockchain interaction
pip install eth-typing  # For Ethereum types
pip install eth-utils  # For Ethereum utilities
pip install requests  # For API calls
pip install aiohttp  # For async API calls
pip install pytest-asyncio  # For async tests
pip install pytest-timeout  # For test timeouts
```

2. Create Configuration:
```python
# config.py
config = {
    "api_keys": {
        "etherscan": "YOUR_ETHERSCAN_KEY",
        "bscscan": "YOUR_BSCSCAN_KEY",
        "infura": "YOUR_INFURA_KEY",
        "coingecko": "YOUR_COINGECKO_KEY",
        "dextools": "YOUR_DEXTOOLS_KEY"
    },
    "nodes": {
        "ethereum": {
            "mainnet": "YOUR_ETH_NODE_URL",
            "testnet": "YOUR_TESTNET_URL"
        },
        "bsc": {
            "mainnet": "YOUR_BSC_NODE_URL",
            "testnet": "YOUR_BSC_TESTNET_URL"
        }
    },
    "rate_limits": {
        "etherscan": 5,  # calls per second
        "bscscan": 5,
        "coingecko": 10,
        "defillama": 3,
        "dextools": 10
    }
}
```

## Configuration

1. Create Test Configuration:
```python
# test_config.py
TEST_TOKENS = {
    "ethereum": {
        "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f"
    },
    "bsc": {
        "BUSD": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
        "CAKE": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
        "WBNB": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
    }
}

TEST_PAIRS = {
    "uniswap_v2": {
        "USDT_ETH": "0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852",
        "USDC_ETH": "0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc"
    },
    "pancakeswap": {
        "BUSD_BNB": "0x58f876857a02d6762e0101bb5c46a8c1ed44dc16",
        "CAKE_BNB": "0x0ed7e52944161450477ee417de9cd3a859b14fd0"
    }
}
```

2. Configure Rate Limiting:
```python
# rate_limiter.py
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls_per_second: int = 1):
        self.calls_per_second = calls_per_second
        self.calls = []
        
    async def wait(self):
        """Wait if needed to respect rate limits."""
        now = datetime.utcnow()
        
        # Remove old calls
        self.calls = [t for t in self.calls 
                     if t > now - timedelta(seconds=1)]
        
        # Wait if too many calls
        if len(self.calls) >= self.calls_per_second:
            wait_time = 1 - (now - self.calls[0]).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        # Add current call
        self.calls.append(now)
```

## Running Tests

### Mock Tests
These tests use mock data and don't require API keys:
```bash
# Run all mock tests
pytest openhands/agents/defi/token_analyzer/tests/

# Run specific mock test file
pytest openhands/agents/defi/token_analyzer/tests/test_agent.py

# Run specific mock test
pytest openhands/agents/defi/token_analyzer/tests/test_agent.py -k test_analyze_token_basic
```

### Real Tests
These tests require API keys and network access:
```bash
# Run all real tests
pytest openhands/agents/defi/token_analyzer/tests/ -m real

# Run specific real test file
pytest openhands/agents/defi/token_analyzer/tests/test_real_data.py

# Run specific real test
pytest openhands/agents/defi/token_analyzer/tests/test_real_data.py -k test_real_token_info
```

## Test Types

### 1. Unit Tests
Test individual components in isolation:
```python
@pytest.mark.asyncio
async def test_get_token_info():
    """Test basic token info retrieval."""
    client = BlockchainClient()
    info = await client.get_token_info("0x...")
    assert isinstance(info, dict)
    assert "name" in info
```

### 2. Integration Tests
Test component interactions:
```python
@pytest.mark.asyncio
async def test_full_analysis():
    """Test complete token analysis flow."""
    agent = TokenAnalysisAgent()
    analysis = await agent.analyze_token("0x...")
    assert isinstance(analysis, TokenAnalysis)
```

### 3. Real Data Tests
Test with actual blockchain and market data:
```python
@pytest.mark.real
@pytest.mark.asyncio
async def test_real_market_data():
    """Test with real USDT market data."""
    client = MarketDataClient(config)
    price = await client.get_token_price(TEST_TOKENS["ethereum"]["USDT"])
    assert abs(Decimal("1") - price["price_usd"]) < Decimal("0.1")
```

## Troubleshooting

### Common Issues

1. Rate Limiting
```
Error: Too many requests
Solution: Implement rate limiting or increase delays between calls
```

2. API Key Issues
```
Error: Invalid API key
Solution: Check API key configuration and permissions
```

3. Network Issues
```
Error: Network connection failed
Solution: Check RPC endpoint configuration and network connectivity
```

4. Test Timeouts
```
Error: Test exceeded timeout
Solution: Increase timeout setting or optimize test
pytest --timeout=300 tests/
```

### Debug Mode
Run tests with detailed logging:
```bash
pytest -v --log-cli-level=DEBUG tests/
```

### Test Categories
Use test markers to run specific categories:
```bash
# Run only mock tests
pytest -v -m "not real" tests/

# Run only real tests
pytest -v -m real tests/

# Run only specific component tests
pytest -v -m "blockchain" tests/
```