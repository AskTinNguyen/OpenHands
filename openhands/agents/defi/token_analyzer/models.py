from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from decimal import Decimal

@dataclass
class DistributionMetrics:
    """Token distribution metrics."""
    total_supply: Decimal
    circulating_supply: Decimal
    holder_count: int
    top_10_holders_percentage: Decimal
    top_50_holders_percentage: Decimal
    top_100_holders_percentage: Decimal
    liquidity_pool_percentage: Decimal
    team_wallet_percentage: Decimal
    staking_locked_percentage: Decimal
    gini_coefficient: Decimal
    holder_concentration: Decimal
    liquidity_ratio: Decimal

@dataclass
class WalletAnalysis:
    """Analysis of specific wallet patterns."""
    address: str
    balance: Decimal
    percentage_held: Decimal
    transaction_count: int
    first_transaction_date: datetime
    last_transaction_date: datetime
    is_contract: bool
    is_marked_suspicious: bool
    risk_factors: List[str]
    interaction_patterns: List[str]

@dataclass
class LiquidityAnalysis:
    """Liquidity pool analysis."""
    total_liquidity_usd: Decimal
    liquidity_pairs: List[str]
    largest_pool_share: Decimal
    liquidity_provider_count: int
    is_liquidity_locked: bool
    lock_expiry_date: Optional[datetime]
    recent_large_removals: List[Dict]
    liquidity_concentration: Decimal
    slippage_impact: Decimal

@dataclass
class ContractAnalysis:
    """Smart contract security analysis."""
    is_verified: bool
    compiler_version: str
    audit_reports: List[str]
    security_score: Decimal
    owner_privileges: List[str]
    has_proxy: bool
    can_mint: bool
    can_blacklist: bool
    risk_functions: List[str]
    security_issues: List[str]

@dataclass
class RiskAssessment:
    """Overall risk assessment."""
    concentration_risk: str  # Low/Medium/High
    liquidity_risk: str
    contract_risk: str
    manipulation_risk: str
    regulatory_risk: str
    overall_risk_score: Decimal
    risk_factors: List[str]
    recommendations: List[str]
    warning_flags: List[str]

@dataclass
class MarketMetrics:
    """Market-related metrics."""
    price_usd: Decimal
    market_cap_usd: Decimal
    volume_24h_usd: Decimal
    price_change_24h: Decimal
    volume_change_24h: Decimal
    volatility_30d: Decimal
    correlation_with_eth: Decimal
    correlation_with_btc: Decimal

@dataclass
class TokenAnalysis:
    """Complete token analysis results."""
    # Basic Information
    token_name: str
    token_symbol: str
    contract_address: str
    blockchain: str
    token_type: str
    creation_date: datetime
    analysis_date: datetime
    
    # Detailed Analysis Components
    distribution: DistributionMetrics
    top_wallets: List[WalletAnalysis]
    liquidity: LiquidityAnalysis
    contract: ContractAnalysis
    risk: RiskAssessment
    market: MarketMetrics
    
    # Historical Data
    price_history: List[Dict]
    volume_history: List[Dict]
    holder_history: List[Dict]
    
    # Additional Information
    social_metrics: Dict
    development_activity: Dict
    news_sentiment: Dict
    
    # Analysis Summary
    summary: str
    recommendations: List[str]
    red_flags: List[str]
    
    def to_dict(self) -> Dict:
        """Convert analysis to dictionary format."""
        # Implementation for serialization
        pass
    
    def to_json(self) -> str:
        """Convert analysis to JSON format."""
        # Implementation for JSON serialization
        pass
    
    def generate_report(self) -> str:
        """Generate a formatted analysis report."""
        # Implementation for report generation
        pass
    
    def get_risk_score(self) -> Decimal:
        """Calculate overall risk score."""
        # Implementation for risk scoring
        pass