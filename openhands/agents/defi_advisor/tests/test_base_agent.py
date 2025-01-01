import pytest
from openhands.agents.base import BaseAgent
from openhands.agents.defi_advisor.agent import DefiAdvisorAgent

def test_defi_advisor_agent_implements_base_agent():
    """Test that DefiAdvisorAgent properly implements BaseAgent."""
    assert issubclass(DefiAdvisorAgent, BaseAgent)

def test_defi_advisor_agent_initialization():
    """Test that DefiAdvisorAgent can be initialized with config."""
    agent = DefiAdvisorAgent()
    config = {
        'price_apis': {'default_currency': 'USD'},
        'analysis_config': {'timeframe': '24h'},
        'risk_params': {'volatility_threshold': 0.1}
    }
    
    # Should not raise any exceptions
    agent.initialize(config)

def test_defi_advisor_agent_capabilities():
    """Test that DefiAdvisorAgent returns expected capabilities."""
    agent = DefiAdvisorAgent()
    capabilities = agent.get_capabilities()
    
    assert isinstance(capabilities, list)
    assert len(capabilities) > 0
    assert "Real-time cryptocurrency price data" in capabilities
    assert "Market trend analysis" in capabilities
    assert "Risk assessment for DeFi investments" in capabilities
    assert "Portfolio recommendations" in capabilities