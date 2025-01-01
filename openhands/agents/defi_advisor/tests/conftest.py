import pytest
from unittest.mock import MagicMock
import json

@pytest.fixture
def mock_coingecko_price_response():
    return {
        'bitcoin': {'usd': 50000},
        'ethereum': {'usd': 3000},
        'cardano': {'usd': 1.5}
    }

@pytest.fixture
def mock_coingecko_market_chart_response():
    return {
        'prices': [
            [1616432400000, 48000],  # Start price
            [1616436000000, 49000],
            [1616439600000, 50000]   # End price
        ],
        'market_caps': [
            [1616432400000, 900000000000],
            [1616436000000, 910000000000],
            [1616439600000, 920000000000]
        ],
        'total_volumes': [
            [1616432400000, 50000000000],
            [1616436000000, 51000000000],
            [1616439600000, 52000000000]
        ]
    }

@pytest.fixture
def mock_coingecko_coin_response():
    return {
        'id': 'bitcoin',
        'symbol': 'btc',
        'name': 'Bitcoin',
        'market_data': {
            'current_price': {'usd': 50000},
            'market_cap': {'usd': 900000000000},
            'total_volume': {'usd': 50000000000},
            'price_change_percentage_24h': 5.5,
            'market_cap_change_percentage_24h': 2.1,
            'total_volume_change_24h': 10.5
        }
    }

@pytest.fixture
def mock_requests(monkeypatch, mock_coingecko_price_response, 
                 mock_coingecko_market_chart_response, mock_coingecko_coin_response):
    """Mock requests to return predefined responses based on URL."""
    def mock_get(*args, **kwargs):
        mock_response = MagicMock()
        
        url = args[0] if args else kwargs.get('url', '')
        
        if 'simple/price' in url:
            mock_response.json.return_value = mock_coingecko_price_response
        elif 'market_chart' in url:
            mock_response.json.return_value = mock_coingecko_market_chart_response
        elif 'coins/' in url:
            mock_response.json.return_value = mock_coingecko_coin_response
        
        mock_response.status_code = 200
        return mock_response

    monkeypatch.setattr('requests.get', mock_get)
    return mock_get