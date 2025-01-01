import pytest
from unittest.mock import Mock, patch
import aiohttp
import asyncio
from decimal import Decimal
from datetime import datetime, timedelta

from openhands.agents.defi.token_analyzer.data_providers.market import MarketDataClient

@pytest.mark.asyncio
async def test_get_token_price():
    """Test token price fetching."""
    client = MarketDataClient()
    
    price_data = await client.get_token_price(
        "0x1234...5678",
        blockchain="ethereum"
    )
    assert isinstance(price_data, dict)
    assert "price_usd" in price_data
    assert isinstance(price_data["price_usd"], Decimal)
    assert "price_change_24h" in price_data
    assert "volume_24h_usd" in price_data

@pytest.mark.asyncio
async def test_get_liquidity_info():
    """Test liquidity information fetching."""
    client = MarketDataClient()
    
    liquidity_data = await client.get_liquidity_info(
        "0x1234...5678",
        blockchain="ethereum"
    )
    assert isinstance(liquidity_data, dict)
    assert "total_liquidity_usd" in liquidity_data
    assert isinstance(liquidity_data["total_liquidity_usd"], Decimal)
    assert "dex_distribution" in liquidity_data
    assert isinstance(liquidity_data["dex_distribution"], dict)

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in market data fetching."""
    client = MarketDataClient()
    
    # Test with invalid token address
    with pytest.raises(ValueError):
        await client.get_token_price(
            "invalid_address",
            blockchain="ethereum"
        )
    
    # Test with network error
    client._mock_network_error = True
    with pytest.raises(Exception):
        await client.get_token_price(
            "0x1234...5678",
            blockchain="ethereum"
        )

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test rate limiting handling."""
    client = MarketDataClient()
    
    # Make multiple rapid requests
    tasks = []
    for _ in range(5):
        tasks.append(
            client.get_token_price(
                "0x1234...5678",
                blockchain="ethereum"
            )
        )
    
    # All requests should complete without rate limit errors
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        assert not isinstance(result, Exception)
        assert isinstance(result, dict)