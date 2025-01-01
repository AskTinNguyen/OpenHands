import pytest
from unittest.mock import Mock, patch
import aiohttp
import asyncio
from datetime import datetime
from decimal import Decimal

from openhands.agents.defi.token_analyzer.data_providers.blockchain import BlockchainClient

@pytest.mark.asyncio
async def test_get_token_info():
    """Test fetching token information."""
    client = BlockchainClient()
    
    # Test Ethereum token
    eth_info = await client.get_token_info(
        "0x1234...5678",
        blockchain="ethereum"
    )
    assert isinstance(eth_info, dict)
    assert "name" in eth_info
    assert "symbol" in eth_info
    assert isinstance(eth_info["total_supply"], Decimal)
    
    # Test BSC token
    bsc_info = await client.get_token_info(
        "0x1234...5678",
        blockchain="bsc"
    )
    assert isinstance(bsc_info, dict)
    assert "name" in bsc_info
    assert "symbol" in bsc_info
    
    # Test unsupported blockchain
    with pytest.raises(ValueError):
        await client.get_token_info(
            "0x1234...5678",
            blockchain="unsupported"
        )

@pytest.mark.asyncio
async def test_get_holder_distribution():
    """Test fetching holder distribution."""
    client = BlockchainClient()
    
    distribution = await client.get_holder_distribution(
        "0x1234...5678",
        blockchain="ethereum"
    )
    assert isinstance(distribution, dict)
    assert "total_holders" in distribution
    assert "top_holders" in distribution
    assert isinstance(distribution["total_holders"], int)
    assert isinstance(distribution["top_holders"], list)
    assert len(distribution["top_holders"]) > 0

@pytest.mark.asyncio
async def test_get_contract_code():
    """Test fetching contract code."""
    client = BlockchainClient()
    
    code = await client.get_contract_code(
        "0x1234...5678",
        blockchain="ethereum"
    )
    assert isinstance(code, dict)
    assert "is_verified" in code
    assert "source_code" in code
    assert "compiler_version" in code
    assert isinstance(code["is_verified"], bool)

@pytest.mark.asyncio
async def test_api_error_handling():
    """Test API error handling."""
    client = BlockchainClient()
    
    # Test with invalid API key
    with patch.dict(client.config, {"etherscan_key": "invalid_key"}):
        with pytest.raises(Exception):
            await client.get_token_info(
                "0x1234...5678",
                blockchain="ethereum"
            )
    
    # Test with network error
    client._mock_network_error = True
    with pytest.raises(Exception):
        await client.get_token_info(
            "0x1234...5678",
            blockchain="ethereum"
        )

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test API rate limiting handling."""
    client = BlockchainClient()
    
    # Make multiple rapid requests
    tasks = []
    for _ in range(5):
        tasks.append(
            client.get_token_info(
                "0x1234...5678",
                blockchain="ethereum"
            )
        )
    
    # All requests should complete without rate limit errors
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        assert not isinstance(result, Exception)
        assert isinstance(result, dict)