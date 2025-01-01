from typing import Dict, Optional
from decimal import Decimal
import asyncio
import logging
import aiohttp

class MarketDataClient:
    """Simplified market data provider for testing."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
    
    async def get_token_price(self, contract_address: str, blockchain: str = "ethereum") -> Dict:
        """Get current token price."""
        try:
            # Mock implementation for testing
            await asyncio.sleep(0.1)  # Simulate API call
            
            if not contract_address.startswith("0x"):
                raise ValueError("Invalid contract address format")
                
            if blockchain not in ["ethereum", "bsc"]:
                raise ValueError(f"Unsupported blockchain: {blockchain}")
                
            if "invalid_key" in self.config.values():
                raise Exception("Invalid API key")
                
            # Simulate network error
            if hasattr(self, "_mock_network_error"):
                raise aiohttp.ClientError("Network error")
                
            return {
                "price_usd": Decimal("1.23"),
                "price_change_24h": Decimal("5.5"),
                "volume_24h_usd": Decimal("1000000")
            }
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise
    
    async def get_liquidity_info(self, contract_address: str, blockchain: str = "ethereum") -> Dict:
        """Get liquidity information."""
        # Mock implementation for testing
        await asyncio.sleep(0.1)  # Simulate API call
        return {
            "total_liquidity_usd": Decimal("500000"),
            "dex_distribution": {
                "uniswap_v2": Decimal("300000"),
                "sushiswap": Decimal("200000")
            }
        }