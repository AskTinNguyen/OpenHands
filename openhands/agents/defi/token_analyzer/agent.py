from typing import List, Dict, Optional
from datetime import datetime
from decimal import Decimal

from .models import (
    TokenAnalysis, DistributionMetrics, WalletAnalysis,
    LiquidityAnalysis, ContractAnalysis, RiskAssessment,
    MarketMetrics
)
from .data_providers.blockchain import BlockchainClient
from .data_providers.market import MarketDataClient
from .analyzers.security import SecurityAnalyzer

class TokenAnalysisAgent:
    """
    Lightweight Token Analysis Agent for testing.
    
    Features:
    - Basic token information retrieval
    - Holder distribution analysis
    - Simple market metrics
    - Basic security checks
    """
    
    def __init__(
        self,
        blockchain_client: Optional[BlockchainClient] = None,
        market_client: Optional[MarketDataClient] = None,
        security_analyzer: Optional[SecurityAnalyzer] = None,
        config: Optional[Dict] = None
    ):
        """Initialize the token analysis agent."""
        self.blockchain_client = blockchain_client or BlockchainClient()
        self.market_client = market_client or MarketDataClient()
        self.security_analyzer = security_analyzer or SecurityAnalyzer()
        self.config = config or {}
    
    async def analyze_token(
        self,
        contract_address: str,
        blockchain: str = "ethereum"
    ) -> TokenAnalysis:
        """
        Perform basic token analysis.
        
        Args:
            contract_address: Token contract address
            blockchain: Blockchain network
        
        Returns:
            TokenAnalysis object with basic analysis
        """
        # Get basic token info
        token_info = await self.blockchain_client.get_token_info(
            contract_address, blockchain
        )
        
        # Get holder distribution
        distribution = await self._analyze_distribution(
            contract_address, blockchain
        )
        
        # Get market data
        market = await self._get_market_metrics(
            contract_address, blockchain
        )
        
        # Get security analysis
        security = await self.security_analyzer.analyze_contract(
            contract_address, blockchain
        )
        
        # Generate risk assessment
        risk = self._assess_risk(distribution, market, security)
        
        return TokenAnalysis(
            token_name=token_info["name"],
            token_symbol=token_info["symbol"],
            contract_address=contract_address,
            blockchain=blockchain,
            token_type="ERC20",
            creation_date=datetime.utcnow(),  # Mock date for testing
            analysis_date=datetime.utcnow(),
            distribution=distribution,
            top_wallets=[],  # Simplified for testing
            liquidity=None,  # Simplified for testing
            contract=None,  # Simplified for testing
            risk=risk,
            market=market,
            price_history=[],  # Simplified for testing
            volume_history=[],  # Simplified for testing
            holder_history=[],  # Simplified for testing
            social_metrics={},  # Simplified for testing
            development_activity={},  # Simplified for testing
            news_sentiment={},  # Simplified for testing
            summary=self._generate_summary(distribution, risk, market),
            recommendations=self._generate_recommendations(risk),
            red_flags=self._identify_red_flags(distribution, market, security)
        )
    
    async def _analyze_distribution(
        self,
        contract_address: str,
        blockchain: str
    ) -> DistributionMetrics:
        """Analyze token distribution."""
        holder_data = await self.blockchain_client.get_holder_distribution(
            contract_address, blockchain
        )
        
        return DistributionMetrics(
            total_supply=Decimal("1000000000"),  # Mock data for testing
            circulating_supply=Decimal("800000000"),
            holder_count=holder_data["total_holders"],
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
    
    async def _get_market_metrics(
        self,
        contract_address: str,
        blockchain: str
    ) -> MarketMetrics:
        """Get market metrics."""
        price_data = await self.market_client.get_token_price(
            contract_address, blockchain
        )
        
        return MarketMetrics(
            price_usd=price_data["price_usd"],
            market_cap_usd=price_data["price_usd"] * Decimal("1000000000"),
            volume_24h_usd=price_data["volume_24h_usd"],
            price_change_24h=price_data["price_change_24h"],
            volume_change_24h=Decimal("10"),  # Mock data for testing
            volatility_30d=Decimal("0.5"),
            correlation_with_eth=Decimal("0.7"),
            correlation_with_btc=Decimal("0.6")
        )
    
    def _assess_risk(
        self,
        distribution: DistributionMetrics,
        market: MarketMetrics,
        security: Dict
    ) -> RiskAssessment:
        """Basic risk assessment."""
        return RiskAssessment(
            concentration_risk="high" if distribution.holder_concentration > Decimal("0.7") else "medium",
            liquidity_risk="medium",
            contract_risk="low" if security["risk_score"] > 70 else "high",
            manipulation_risk="medium",
            regulatory_risk="medium",
            overall_risk_score=Decimal("65"),
            risk_factors=["High holder concentration", "Above average volatility"],
            recommendations=["Monitor whale movements", "Set strict stop losses"],
            warning_flags=["High concentration in top wallets"]
        )
    
    def _generate_summary(
        self,
        distribution: DistributionMetrics,
        risk: RiskAssessment,
        market: MarketMetrics
    ) -> str:
        """Generate analysis summary."""
        return f"Token shows {risk.overall_risk_score} risk score with {distribution.holder_count} holders"
    
    def _generate_recommendations(
        self,
        risk: RiskAssessment
    ) -> List[str]:
        """Generate recommendations."""
        return risk.recommendations
    
    def _identify_red_flags(
        self,
        distribution: DistributionMetrics,
        market: MarketMetrics,
        security: Dict
    ) -> List[str]:
        """Identify red flags."""
        flags = []
        
        if distribution.holder_concentration > Decimal("0.7"):
            flags.append("High holder concentration")
        
        if market.volatility_30d > Decimal("0.4"):
            flags.append("High volatility")
        
        if security["risk_score"] < Decimal("70"):
            flags.append("Security concerns")
        
        return flags