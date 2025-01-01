import pytest
from datetime import datetime
from decimal import Decimal
import asyncio
from unittest.mock import Mock, patch

from openhands.agents.defi.token_analyzer.agent import TokenAnalysisAgent
from openhands.agents.defi.token_analyzer.models import TokenAnalysis, DistributionMetrics, RiskAssessment, MarketMetrics

@pytest.mark.asyncio
async def test_analyze_token_basic(
    mock_token_info,
    mock_holder_distribution,
    mock_market_data
):
    """Test basic token analysis functionality."""
    # Create mock clients with async return values
    mock_blockchain_client = Mock()
    mock_blockchain_client.get_token_info.return_value = asyncio.Future()
    mock_blockchain_client.get_token_info.return_value.set_result(mock_token_info)
    mock_blockchain_client.get_holder_distribution.return_value = asyncio.Future()
    mock_blockchain_client.get_holder_distribution.return_value.set_result(mock_holder_distribution)
    
    mock_market_client = Mock()
    mock_market_client.get_token_price.return_value = asyncio.Future()
    mock_market_client.get_token_price.return_value.set_result(mock_market_data)
    
    mock_security_analyzer = Mock()
    mock_security_analyzer.analyze_contract.return_value = asyncio.Future()
    mock_security_analyzer.analyze_contract.return_value.set_result({
        "risk_score": Decimal("75"),
        "issues": []
    })
    
    # Initialize agent with mocks
    agent = TokenAnalysisAgent(
        blockchain_client=mock_blockchain_client,
        market_client=mock_market_client,
        security_analyzer=mock_security_analyzer
    )
    
    # Perform analysis
    analysis = await agent.analyze_token(
        contract_address="0x1234...5678",
        blockchain="ethereum"
    )
    
    # Verify analysis results
    assert isinstance(analysis, TokenAnalysis)
    assert analysis.token_name == mock_token_info["name"]
    assert analysis.token_symbol == mock_token_info["symbol"]
    assert isinstance(analysis.distribution, DistributionMetrics)
    assert isinstance(analysis.risk, RiskAssessment)
    assert len(analysis.recommendations) > 0
    assert len(analysis.red_flags) > 0

@pytest.mark.asyncio
async def test_risk_assessment(mock_token_info):
    """Test risk assessment functionality."""
    agent = TokenAnalysisAgent()
    
    distribution = DistributionMetrics(
        total_supply=Decimal("1000000000"),
        circulating_supply=Decimal("800000000"),
        holder_count=1000,
        top_10_holders_percentage=Decimal("60"),
        top_50_holders_percentage=Decimal("80"),
        top_100_holders_percentage=Decimal("90"),
        liquidity_pool_percentage=Decimal("20"),
        team_wallet_percentage=Decimal("15"),
        staking_locked_percentage=Decimal("30"),
        gini_coefficient=Decimal("0.85"),
        holder_concentration=Decimal("0.75"),
        liquidity_ratio=Decimal("0.15")
    )
    
    market = MarketMetrics(
        price_usd=Decimal("1.23"),
        market_cap_usd=Decimal("123000000"),
        volume_24h_usd=Decimal("5000000"),
        price_change_24h=Decimal("5.5"),
        volume_change_24h=Decimal("10"),
        volatility_30d=Decimal("0.5"),
        correlation_with_eth=Decimal("0.7"),
        correlation_with_btc=Decimal("0.6")
    )
    
    security = {
        "risk_score": Decimal("75"),
        "issues": []
    }
    
    risk = agent._assess_risk(distribution, market, security)
    
    assert isinstance(risk, RiskAssessment)
    assert isinstance(risk.overall_risk_score, Decimal)
    assert len(risk.risk_factors) > 0
    assert len(risk.recommendations) > 0
    assert "high" in risk.concentration_risk.lower()

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in analysis."""
    mock_blockchain_client = Mock()
    mock_blockchain_client.get_token_info.side_effect = Exception("API Error")
    
    agent = TokenAnalysisAgent(blockchain_client=mock_blockchain_client)
    
    with pytest.raises(Exception):
        await agent.analyze_token(
            contract_address="0x1234...5678",
            blockchain="ethereum"
        )