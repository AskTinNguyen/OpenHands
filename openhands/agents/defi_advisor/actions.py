from abc import ABC, abstractmethod
from typing import Any, Dict
import requests

class BaseAction(ABC):
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def execute(self, request: str) -> Dict[str, Any]:
        pass

class PriceFetchAction(BaseAction):
    """Action to fetch cryptocurrency prices from various sources."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        self.api_keys = config.get('api_keys', {})
        self.default_currency = config.get('default_currency', 'USD')
    
    def execute(self, request: str) -> Dict[str, Any]:
        # Example implementation using CoinGecko API (free tier)
        try:
            # Extract cryptocurrency from request
            # This is a simple implementation - should be enhanced with NLP
            crypto = request.lower().split('price of ')[-1].split('?')[0].strip().upper()
            
            # CoinGecko API doesn't require API key for basic endpoints
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': crypto.lower(),
                'vs_currencies': self.default_currency.lower()
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                price = data.get(crypto.lower(), {}).get(self.default_currency.lower())
                if price:
                    return {
                        'status': 'success',
                        'data': {
                            'price': price,
                            'currency': self.default_currency,
                            'crypto': crypto
                        }
                    }
            
            return {
                'status': 'error',
                'message': f'Unable to fetch price for {crypto}'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error fetching price: {str(e)}'
            }

class MarketAnalysisAction(BaseAction):
    """Action to analyze market trends and indicators."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        self.analysis_params = config.get('analysis_params', {
            'timeframe': '24h',
            'indicators': ['volume', 'market_cap', 'price_change']
        })
    
    def execute(self, request: str) -> Dict[str, Any]:
        try:
            # Extract cryptocurrency and analysis parameters from request
            # This is a simple implementation - should be enhanced with NLP
            crypto = request.lower().split('trend for ')[-1].split()[0].strip().upper()
            
            # Example implementation using CoinGecko API
            url = f"https://api.coingecko.com/api/v3/coins/{crypto.lower()}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': '1',  # 24h data
                'interval': 'hourly'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                
                # Simple trend analysis
                prices = data.get('prices', [])
                if len(prices) >= 2:
                    start_price = prices[0][1]
                    end_price = prices[-1][1]
                    price_change = ((end_price - start_price) / start_price) * 100
                    
                    trend = 'bullish' if price_change > 0 else 'bearish'
                    
                    return {
                        'status': 'success',
                        'data': {
                            'trend': trend,
                            'price_change_24h': f"{price_change:.2f}%",
                            'analysis': f"The market for {crypto} is showing a {trend} trend with a {price_change:.2f}% price change in the last 24 hours."
                        }
                    }
            
            return {
                'status': 'error',
                'message': f'Unable to analyze market trend for {crypto}'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error analyzing market: {str(e)}'
            }

class RiskAssessmentAction(BaseAction):
    """Action to assess investment risks."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        self.risk_params = config.get('risk_params', {
            'volatility_threshold': 0.1,
            'volume_threshold': 1000000,
            'market_cap_threshold': 10000000
        })
    
    def execute(self, request: str) -> Dict[str, Any]:
        try:
            # Extract asset from request
            # This is a simple implementation - should be enhanced with NLP
            asset = request.lower().split('risk of ')[-1].split()[0].strip().upper()
            
            # Example implementation using CoinGecko API
            url = f"https://api.coingecko.com/api/v3/coins/{asset.lower()}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # Simple risk assessment based on market data
                market_data = data.get('market_data', {})
                price_change_24h = abs(market_data.get('price_change_percentage_24h', 0))
                market_cap = market_data.get('market_cap', {}).get('usd', 0)
                volume = market_data.get('total_volume', {}).get('usd', 0)
                
                risk_factors = []
                risk_level = 'low'
                
                if price_change_24h > self.risk_params['volatility_threshold']:
                    risk_factors.append('high volatility')
                    risk_level = 'high'
                
                if market_cap < self.risk_params['market_cap_threshold']:
                    risk_factors.append('low market cap')
                    risk_level = 'high'
                
                if volume < self.risk_params['volume_threshold']:
                    risk_factors.append('low trading volume')
                    risk_level = 'medium' if risk_level != 'high' else 'high'
                
                return {
                    'status': 'success',
                    'data': {
                        'risk_level': risk_level,
                        'risk_factors': risk_factors,
                        'assessment': f"Investment in {asset} is considered {risk_level} risk due to {', '.join(risk_factors) if risk_factors else 'stable market conditions'}."
                    }
                }
            
            return {
                'status': 'error',
                'message': f'Unable to assess risk for {asset}'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error assessing risk: {str(e)}'
            }

class PortfolioRecommendationAction(BaseAction):
    """Action to provide portfolio recommendations."""
    
    def initialize(self, config: Dict[str, Any]) -> None:
        self.portfolio_params = config.get('portfolio_params', {
            'risk_profiles': {
                'conservative': {'btc': 0.6, 'eth': 0.3, 'stables': 0.1},
                'moderate': {'btc': 0.4, 'eth': 0.3, 'defi': 0.2, 'stables': 0.1},
                'aggressive': {'btc': 0.3, 'eth': 0.3, 'defi': 0.3, 'other': 0.1}
            }
        })
    
    def execute(self, request: str) -> Dict[str, Any]:
        try:
            # Determine risk profile from request
            # This is a simple implementation - should be enhanced with NLP
            risk_profile = 'moderate'  # default
            if 'conservative' in request.lower():
                risk_profile = 'conservative'
            elif 'aggressive' in request.lower():
                risk_profile = 'aggressive'
            
            allocation = self.portfolio_params['risk_profiles'][risk_profile]
            
            return {
                'status': 'success',
                'data': {
                    'risk_profile': risk_profile,
                    'allocation': allocation,
                    'recommendation': f"For a {risk_profile} risk profile, we recommend the following allocation: " + 
                                    ", ".join([f"{int(v*100)}% {k.upper()}" for k, v in allocation.items()])
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error generating portfolio recommendation: {str(e)}'
            }