import pytest
from openhands.agents.defi_advisor.actions import PriceFetchAction

def test_price_fetch_initialization():
    """Test PriceFetchAction initialization with config."""
    action = PriceFetchAction()
    config = {
        'api_keys': {'coingecko': 'test_key'},
        'default_currency': 'EUR'
    }
    
    action.initialize(config)
    assert action.default_currency == 'EUR'
    assert action.api_keys == {'coingecko': 'test_key'}

def test_price_fetch_default_config():
    """Test PriceFetchAction with default config."""
    action = PriceFetchAction()
    action.initialize({})
    assert action.default_currency == 'USD'
    assert action.api_keys == {}

def test_price_fetch_execution(mock_requests):
    """Test successful price fetch execution."""
    action = PriceFetchAction()
    action.initialize({})
    
    result = action.execute("What's the current price of bitcoin?")
    
    assert result['status'] == 'success'
    assert 'data' in result
    assert result['data']['price'] == 50000
    assert result['data']['currency'] == 'USD'
    assert result['data']['crypto'] == 'BITCOIN'

def test_price_fetch_unknown_crypto(mock_requests):
    """Test price fetch for unknown cryptocurrency."""
    action = PriceFetchAction()
    action.initialize({})
    
    result = action.execute("What's the current price of UNKNOWN_COIN?")
    
    assert result['status'] == 'error'
    assert 'message' in result
    assert 'Unable to fetch price' in result['message']

def test_price_fetch_malformed_request():
    """Test price fetch with malformed request."""
    action = PriceFetchAction()
    action.initialize({})
    
    result = action.execute("Invalid request without price information")
    
    assert result['status'] == 'error'
    assert 'message' in result