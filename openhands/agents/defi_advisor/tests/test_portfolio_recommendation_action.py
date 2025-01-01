import pytest
from openhands.agents.defi_advisor.actions import PortfolioRecommendationAction

def test_portfolio_recommendation_initialization():
    """Test PortfolioRecommendationAction initialization with config."""
    action = PortfolioRecommendationAction()
    config = {
        'portfolio_params': {
            'risk_profiles': {
                'conservative': {'btc': 0.7, 'eth': 0.2, 'stables': 0.1},
                'aggressive': {'btc': 0.2, 'eth': 0.4, 'defi': 0.4}
            }
        }
    }
    
    action.initialize(config)
    assert 'conservative' in action.portfolio_params['risk_profiles']
    assert action.portfolio_params['risk_profiles']['conservative']['btc'] == 0.7

def test_portfolio_recommendation_default_config():
    """Test PortfolioRecommendationAction with default config."""
    action = PortfolioRecommendationAction()
    action.initialize({})
    
    assert 'conservative' in action.portfolio_params['risk_profiles']
    assert 'moderate' in action.portfolio_params['risk_profiles']
    assert 'aggressive' in action.portfolio_params['risk_profiles']

def test_portfolio_recommendation_conservative():
    """Test portfolio recommendation for conservative profile."""
    action = PortfolioRecommendationAction()
    action.initialize({})
    
    result = action.execute("Recommend a conservative portfolio")
    
    assert result['status'] == 'success'
    assert result['data']['risk_profile'] == 'conservative'
    assert 'allocation' in result['data']
    assert result['data']['allocation']['btc'] == 0.6
    assert result['data']['allocation']['stables'] == 0.1

def test_portfolio_recommendation_aggressive():
    """Test portfolio recommendation for aggressive profile."""
    action = PortfolioRecommendationAction()
    action.initialize({})
    
    result = action.execute("Recommend an aggressive portfolio")
    
    assert result['status'] == 'success'
    assert result['data']['risk_profile'] == 'aggressive'
    assert 'allocation' in result['data']
    assert result['data']['allocation']['defi'] == 0.3
    assert result['data']['allocation']['other'] == 0.1

def test_portfolio_recommendation_default_moderate():
    """Test portfolio recommendation defaults to moderate profile."""
    action = PortfolioRecommendationAction()
    action.initialize({})
    
    result = action.execute("Recommend a portfolio")
    
    assert result['status'] == 'success'
    assert result['data']['risk_profile'] == 'moderate'
    assert 'allocation' in result['data']
    assert result['data']['allocation']['btc'] == 0.4
    assert result['data']['allocation']['defi'] == 0.2

def test_portfolio_recommendation_formatting():
    """Test portfolio recommendation output formatting."""
    action = PortfolioRecommendationAction()
    action.initialize({})
    
    result = action.execute("Recommend a portfolio")
    
    assert 'recommendation' in result['data']
    assert isinstance(result['data']['recommendation'], str)
    assert '%' in result['data']['recommendation']
    assert 'BTC' in result['data']['recommendation'].upper()