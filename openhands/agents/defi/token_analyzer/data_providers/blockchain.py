from typing import Dict, Optional
from decimal import Decimal
import asyncio
import aiohttp

class BlockchainClient:
    """Simplified blockchain data provider for testing."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
    
    async def get_token_info(self, contract_address: str, blockchain: str = "ethereum") -> Dict:
        """Get basic token information."""
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
                "name": "Test Token",
                "symbol": "TEST",
                "decimals": 18,
                "total_supply": Decimal("1000000000")
            }
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise
    
    async def get_holder_distribution(self, contract_address: str, blockchain: str = "ethereum") -> Dict:
        """Get token holder distribution."""
        # Mock implementation for testing
        await asyncio.sleep(0.1)  # Simulate API call
        return {
            "total_holders": 1000,
            "top_holders": [
                {"address": "0x1", "balance": Decimal("100000"), "percentage": Decimal("10")},
                {"address": "0x2", "balance": Decimal("50000"), "percentage": Decimal("5")}
            ]
        }
    
    async def get_contract_code(self, contract_address: str, blockchain: str = "ethereum") -> Dict:
        """Get contract source code and verification status."""
        # Mock implementation for testing
        await asyncio.sleep(0.1)  # Simulate API call
        return {
            "is_verified": True,
            "source_code": "// SPDX-License-Identifier: MIT...",
            "compiler_version": "v0.8.17"
        }