"""
Configuration template for Token Analysis Agent tests.
Copy this file to config.py and fill in your values.
"""

config = {
    "api_keys": {
        "etherscan": "",  # Get from https://etherscan.io/apis
        "bscscan": "",    # Get from https://bscscan.com/apis
        "infura": "",     # Get from https://infura.io/
        "alchemy": "",    # Get from https://www.alchemy.com/
        "coingecko": "",  # Get from https://www.coingecko.com/api/pricing
        "dextools": ""    # Get from https://www.dextools.io/app/api
    },
    "nodes": {
        "ethereum": {
            "mainnet": "https://mainnet.infura.io/v3/YOUR_KEY",
            "testnet": "https://goerli.infura.io/v3/YOUR_KEY"
        },
        "bsc": {
            "mainnet": "https://bsc-dataseed.binance.org",
            "testnet": "https://data-seed-prebsc-1-s1.binance.org:8545"
        }
    },
    "rate_limits": {
        "etherscan": 5,   # calls per second
        "bscscan": 5,     # calls per second
        "coingecko": 10,  # calls per second (50 with pro API)
        "defillama": 3,   # calls per second
        "dextools": 10    # calls per second
    },
    "timeouts": {
        "default": 10,    # seconds
        "blockchain": 30, # seconds for blockchain calls
        "market": 15     # seconds for market data calls
    },
    "cache": {
        "enabled": True,
        "ttl": 300       # cache TTL in seconds
    },
    "test_tokens": {
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
    },
    "test_pairs": {
        "uniswap_v2": {
            "USDT_ETH": "0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852",
            "USDC_ETH": "0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc"
        },
        "pancakeswap": {
            "BUSD_BNB": "0x58f876857a02d6762e0101bb5c46a8c1ed44dc16",
            "CAKE_BNB": "0x0ed7e52944161450477ee417de9cd3a859b14fd0"
        }
    }
}