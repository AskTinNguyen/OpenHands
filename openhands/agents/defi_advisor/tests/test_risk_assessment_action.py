import pytest
from unittest.mock import MagicMock
from openhands.agents.defi_advisor.actions import RiskAssessmentAction

def test_risk_assessment_initialization():
    """Test RiskAssessmentAction initialization with config."""
    action = RiskAssessmentAction()
    config = {
        'risk_params': {
            'volatility_threshold': 0.15,
            'volume_threshold': 2000000,
            'market_cap_threshold': 20000000
        }
    }
    
    action.initialize(config)
    assert action.risk_params['volatility_threshold'] == 0.15
    assert action.risk_params['volume_threshold'] == 2000000

def test_risk_assessment_default_config():
    """Test RiskAssessmentAction with default config."""
    action = RiskAssessmentAction()
    action.initialize({})
    
    assert action.risk_params['volatility_threshold'] == 0.1
    assert action.risk_params['volume_threshold'] == 1000000
    assert action.risk_params['market_cap_threshold'] == 10000000

def test_risk_assessment_execution(mock_requests):
    """Test successful risk assessment execution."""
    action = RiskAssessmentAction()
    action.initialize({})
    
    result = action.execute("Assess the risk of bitcoin")
    
    assert result['status'] == 'success'
    assert 'data' in result
    assert 'risk_level' in result['data']
    assert 'risk_factors' in result['data']
    assert 'assessment' in result['data']

def test_risk_assessment_high_risk(mock_requests, monkeypatch):
    """Test risk assessment for high-risk asset."""
    def mock_high_risk_get(*args, **kwargs):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'market_data': {
                'price_change_percentage_24h': 25.0,  # High volatility
                'market_cap': {'usd': 5000000},      # Low market cap
                'total_volume': {'usd': 500000}      # Low volume
            }
        }
        return mock_response
    
    monkeypatch.setattr('requests.get', mock_high_risk_get)
    
    action = RiskAssessmentAction()
    action.initialize({})
    
    result = action.execute("Assess the risk of some_token")
    
    assert result['status'] == 'success'
    assert result['data']['risk_level'] == 'high'
    assert len(result['data']['risk_factors']) > 0
    assert 'high volatility' in result['data']['risk_factors']

def test_risk_assessment_unknown_asset(mock_requests, monkeypatch):
    """Test risk assessment for unknown asset."""
    def mock_error_get(*args, **kwargs):
        mock_response = MagicMock()
        mock_response.status_code = 404
        return mock_response
    
    monkeypatch.setattr('requests.get', mock_error_get)
    
    action = RiskAssessmentAction()
    action.initialize({})
    
    result = action.execute("Assess the risk of UNKNOWN_COIN")
    
    assert result['status'] == 'error'
    assert 'message' in result
    assert 'Unable to assess risk' in result['message']