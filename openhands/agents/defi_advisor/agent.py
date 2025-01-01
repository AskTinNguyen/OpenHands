from typing import Any, Dict, List
import json

from ..base import BaseAgent
from .actions import (
    PriceFetchAction,
    MarketAnalysisAction,
    RiskAssessmentAction,
    PortfolioRecommendationAction
)

class DefiAdvisorAgent(BaseAgent):
    """
    DeFi Advisor Agent that provides cryptocurrency investment advice.
    
    Capabilities:
    - Fetch real-time price data for cryptocurrencies
    - Analyze market trends and indicators
    - Assess investment risks
    - Provide portfolio recommendations
    """
    
    def __init__(self):
        self.price_fetcher = PriceFetchAction()
        self.market_analyzer = MarketAnalysisAction()
        self.risk_assessor = RiskAssessmentAction()
        self.portfolio_advisor = PortfolioRecommendationAction()
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the agent with API keys and configurations."""
        self.config = config
        # Initialize price data sources
        self.price_fetcher.initialize(config.get('price_apis', {}))
        # Initialize market analysis tools
        self.market_analyzer.initialize(config.get('analysis_config', {}))
        # Initialize risk assessment parameters
        self.risk_assessor.initialize(config.get('risk_params', {}))
        
    def process_request(self, request: str) -> Dict[str, Any]:
        """
        Process a user request for DeFi advice.
        
        Example requests:
        - "What's the current price of ETH?"
        - "Analyze the market trend for BTC"
        - "Assess the risk of investing in DeFi tokens"
        - "Recommend a balanced crypto portfolio"
        """
        try:
            # Basic request classification
            if 'price' in request.lower():
                return self.price_fetcher.execute(request)
            elif 'trend' in request.lower() or 'analyze' in request.lower():
                return self.market_analyzer.execute(request)
            elif 'risk' in request.lower():
                return self.risk_assessor.execute(request)
            elif 'portfolio' in request.lower() or 'recommend' in request.lower():
                return self.portfolio_advisor.execute(request)
            else:
                return {
                    'status': 'error',
                    'message': 'Unable to classify request. Please specify if you want price information, market analysis, risk assessment, or portfolio recommendations.'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error processing request: {str(e)}'
            }
    
    def get_capabilities(self) -> List[str]:
        """Return the list of agent capabilities."""
        return [
            "Real-time cryptocurrency price data",
            "Market trend analysis",
            "Risk assessment for DeFi investments",
            "Portfolio recommendations",
            "DeFi protocol analysis"
        ]