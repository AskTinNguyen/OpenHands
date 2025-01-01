import pytest
from unittest.mock import MagicMock
from openhands.agents.defi_advisor.actions import MarketAnalysisAction

def test_market_analysis_initialization():
    """Test MarketAnalysisAction initialization with config."""
    action = MarketAnalysisAction()
    config = {
        'analysis_params': {
            'timeframe': '12h',
            'indicators': ['rsi', 'macd']
        }
    }
    
    action.initialize(config)
    assert action.analysis_params['timeframe'] == '12h'
    assert 'rsi' in action.analysis_params['indicators']

def test_market_analysis_default_config():
    """Test MarketAnalysisAction with default config."""
    action = MarketAnalysisAction()
    action.initialize({})
    
    assert action.analysis_params['timeframe'] == '24h'
    assert 'volume' in action.analysis_params['indicators']
    assert 'market_cap' in action.analysis_params['indicators']

def test_market_analysis_execution(mock_requests):
    """Test successful market analysis execution."""
    action = MarketAnalysisAction()
    action.initialize({})
    
    result = action.execute("Analyze the market trend for bitcoin")
    
    assert result['status'] == 'success'
    assert 'data' in result
    assert 'trend' in result['data']
    assert 'price_change_24h' in result['data']
    assert 'analysis' in result['data']
    
    # Verify trend calculation
    # Mock data shows price increase from 48000 to 50000
    assert result['data']['trend'] == 'bullish'
    assert '4.17%' in result['data']['price_change_24h']

def test_market_analysis_unknown_crypto(mock_requests, monkeypatch):
    """Test market analysis for unknown cryptocurrency."""
    def mock_error_get(*args, **kwargs):
        mock_response = MagicMock()
        mock_response.status_code = 404
        return mock_response
    
    monkeypatch.setattr('requests.get', mock_error_get)
    
    action = MarketAnalysisAction()
    action.initialize({})
    
    result = action.execute("Analyze the market trend for UNKNOWN_COIN")
    
    assert result['status'] == 'error'
    assert 'message' in result
    assert 'Unable to analyze market trend' in result['message']

def test_market_analysis_malformed_request():
    """Test market analysis with malformed request."""
    action = MarketAnalysisAction()
    action.initialize({})
    
    result = action.execute("Invalid request without trend information")
    
    assert result['status'] == 'error'
    assert 'message' in result