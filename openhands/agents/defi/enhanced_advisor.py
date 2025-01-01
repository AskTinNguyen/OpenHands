from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from decimal import Decimal

from openhands.agents.defi.tools.defi_tools import DeFiTools
from openhands.agents.defi.tools.web_verifier import DeFiWebVerifier

@dataclass
class StrategyRecommendation:
    protocol: str
    expected_roi: float
    risk_level: str
    gas_costs: Dict[str, str]
    pros: List[str]
    cons: List[str]
    recommendation_strength: str  # "Strong", "Moderate", "Weak"
    additional_notes: str
    verification_data: Dict[str, Any]  # Contains verification sources and confidence scores
    references: Dict[str, List[str]]  # Contains reference links by category

class EnhancedDeFiAdvisor:
    """
    Enhanced DeFi Advisor Agent with sophisticated analysis capabilities.
    
    Features:
    - Comprehensive yield strategy analysis
    - Risk-adjusted return calculations
    - Gas cost optimization
    - Protocol comparison and ranking
    - Portfolio allocation recommendations
    - Risk assessment and mitigation strategies
    """
    
    def __init__(self):
        """Initialize the Enhanced DeFi Advisor."""
        self.tools = DeFiTools()
    
    def get_strategy_recommendations(
        self,
        amount: float,
        time_horizon_months: int = 6,
        risk_preference: str = "medium",
        specific_protocols: Optional[List[str]] = None,
        min_apy: Optional[float] = None,
        max_gas_cost: Optional[float] = None
    ) -> List[StrategyRecommendation]:
        """
        Get comprehensive strategy recommendations based on user preferences.
        
        Args:
            amount: Amount of ETH to invest
            time_horizon_months: Investment time horizon in months
            risk_preference: Risk preference ("low", "medium", or "high")
            specific_protocols: Optional list of specific protocols to analyze
            min_apy: Minimum acceptable APY
            max_gas_cost: Maximum acceptable gas cost in ETH
        
        Returns:
            List of strategy recommendations sorted by suitability
        """
        recommendations = []
        strategies = self.tools.get_eth_yield_strategies()
        
        # Filter protocols if specific ones are requested
        if specific_protocols:
            strategies = {k: v for k, v in strategies.items() if k in specific_protocols}
        
        for protocol_name, strategy in strategies.items():
            # Get detailed protocol data
            protocol_data = self.tools.get_protocol_data(protocol_name)
            if not protocol_data:
                continue
            
            # Calculate ROI
            roi_data = self.tools.calculate_roi(amount, protocol_name, time_horizon_months)
            if not roi_data:
                continue
            
            # Get risk score
            risk_score = self.tools.analyze_risk_score(protocol_name)
            if not risk_score:
                continue
            
            # Get gas costs
            gas_costs = self.tools.analyze_gas_costs(protocol_name)
            if not gas_costs:
                continue
            
            # Calculate risk-adjusted metrics
            total_risk_score = (
                risk_score.smart_contract_risk +
                risk_score.centralization_risk +
                risk_score.regulatory_risk +
                risk_score.market_risk +
                risk_score.technical_risk
            ) / 5.0
            
            # Skip if doesn't meet minimum APY requirement
            if min_apy and protocol_data.apy < min_apy:
                continue
            
            # Skip if gas costs are too high
            if max_gas_cost and roi_data["gas_cost"] > max_gas_cost:
                continue
            
            # Determine if strategy matches risk preference
            risk_match = self._evaluate_risk_match(total_risk_score, risk_preference)
            if not risk_match:
                continue
            
            # Generate pros and cons
            pros, cons = self._analyze_pros_cons(
                protocol_data,
                roi_data,
                risk_score,
                gas_costs,
                amount
            )
            
            # Determine recommendation strength
            strength = self._calculate_recommendation_strength(
                risk_match,
                roi_data["roi_percentage"],
                total_risk_score,
                protocol_data.tvl_billions
            )
            
            # Get verification data
            apy_verification = DeFiWebVerifier.verify_apy_data(
                protocol_name, 
                protocol_data.apy
            )
            risk_verification = DeFiWebVerifier.verify_risk_assessment(
                protocol_name, 
                self._risk_score_to_level(total_risk_score)
            )
            tvl_verification = DeFiWebVerifier.verify_tvl_data(
                protocol_name, 
                protocol_data.tvl_billions
            )
            
            # Get reference links
            references = DeFiWebVerifier.get_protocol_references(protocol_name)
            
            # Get verification summary
            verification_summary = DeFiWebVerifier.get_verification_summary(protocol_name)
            
            verification_data = {
                "apy": {
                    "value": protocol_data.apy,
                    "confidence": apy_verification.confidence_score,
                    "sources": [s.url for s in apy_verification.sources]
                },
                "risk": {
                    "value": self._risk_score_to_level(total_risk_score),
                    "confidence": risk_verification.confidence_score,
                    "sources": [s.url for s in risk_verification.sources]
                },
                "tvl": {
                    "value": protocol_data.tvl_billions,
                    "confidence": tvl_verification.confidence_score,
                    "sources": [s.url for s in tvl_verification.sources]
                },
                "overall": verification_summary
            }
            
            recommendations.append(StrategyRecommendation(
                protocol=protocol_name,
                expected_roi=roi_data["roi_percentage"],
                risk_level=self._risk_score_to_level(total_risk_score),
                gas_costs={"deposit": gas_costs.deposit, "withdrawal": gas_costs.withdrawal},
                pros=pros,
                cons=cons,
                recommendation_strength=strength,
                additional_notes=self._generate_additional_notes(
                    protocol_data,
                    risk_score,
                    time_horizon_months
                ),
                verification_data=verification_data,
                references=references
            ))
        
        # Sort recommendations by suitability
        return sorted(
            recommendations,
            key=lambda x: (
                self._strength_to_score(x.recommendation_strength),
                x.expected_roi
            ),
            reverse=True
        )
    
    def analyze_portfolio_allocation(
        self,
        amount: float,
        risk_preference: str,
        time_horizon_months: int
    ) -> Dict[str, float]:
        """
        Generate optimal portfolio allocation across different protocols.
        
        Args:
            amount: Total amount of ETH to allocate
            risk_preference: Risk preference ("low", "medium", or "high")
            time_horizon_months: Investment time horizon in months
        
        Returns:
            Dictionary mapping protocols to allocation percentages
        """
        recommendations = self.get_strategy_recommendations(
            amount=amount,
            time_horizon_months=time_horizon_months,
            risk_preference=risk_preference
        )
        
        # Define allocation weights based on recommendation strength
        weights = {
            "Strong": 0.4,
            "Moderate": 0.3,
            "Weak": 0.2
        }
        
        # Calculate initial allocations
        total_weight = sum(weights[r.recommendation_strength] for r in recommendations[:3])
        allocations = {}
        
        for rec in recommendations[:3]:  # Consider top 3 recommendations
            allocation = (weights[rec.recommendation_strength] / total_weight) * 100
            allocations[rec.protocol] = round(allocation, 2)
        
        return allocations
    
    def _evaluate_risk_match(self, risk_score: float, preference: str) -> bool:
        """Evaluate if a strategy's risk matches user preference."""
        risk_ranges = {
            "low": (0, 4),
            "medium": (3, 6),
            "high": (5, 10)
        }
        min_score, max_score = risk_ranges[preference.lower()]
        return min_score <= risk_score <= max_score
    
    def _risk_score_to_level(self, score: float) -> str:
        """Convert numerical risk score to risk level."""
        if score < 3:
            return "Low"
        elif score < 5:
            return "Medium"
        else:
            return "High"
    
    def _analyze_pros_cons(
        self,
        protocol_data: Any,
        roi_data: Dict[str, float],
        risk_score: Any,
        gas_costs: Any,
        amount: float
    ) -> tuple[List[str], List[str]]:
        """Analyze pros and cons of a strategy."""
        pros = []
        cons = []
        
        # Analyze returns
        if roi_data["roi_percentage"] > 5:
            pros.append(f"High potential returns ({roi_data['roi_percentage']:.1f}% ROI)")
        elif roi_data["roi_percentage"] < 2:
            cons.append(f"Low potential returns ({roi_data['roi_percentage']:.1f}% ROI)")
        
        # Analyze risks
        if risk_score.smart_contract_risk < 3:
            pros.append("Low smart contract risk")
        elif risk_score.smart_contract_risk > 5:
            cons.append("High smart contract risk")
        
        # Analyze gas costs
        gas_cost_percentage = (roi_data["gas_cost"] * 100) / amount
        if gas_cost_percentage < 1:
            pros.append("Low gas costs relative to investment")
        elif gas_cost_percentage > 3:
            cons.append("High gas costs relative to investment")
        
        # Analyze protocol characteristics
        if protocol_data.insurance == "Yes":
            pros.append("Insurance available")
        else:
            cons.append("No insurance coverage")
        
        if protocol_data.tvl_billions > 5:
            pros.append(f"Large TVL (${protocol_data.tvl_billions}B)")
        elif protocol_data.tvl_billions < 1:
            cons.append(f"Small TVL (${protocol_data.tvl_billions}B)")
        
        return pros, cons
    
    def _calculate_recommendation_strength(
        self,
        risk_match: bool,
        roi_percentage: float,
        risk_score: float,
        tvl_billions: float
    ) -> str:
        """Calculate the strength of a recommendation."""
        if not risk_match:
            return "Weak"
        
        points = 0
        
        # ROI points
        if roi_percentage > 10:
            points += 3
        elif roi_percentage > 5:
            points += 2
        elif roi_percentage > 2:
            points += 1
        
        # Risk points
        if risk_score < 3:
            points += 3
        elif risk_score < 5:
            points += 2
        elif risk_score < 7:
            points += 1
        
        # TVL points
        if tvl_billions > 10:
            points += 3
        elif tvl_billions > 5:
            points += 2
        elif tvl_billions > 1:
            points += 1
        
        if points >= 7:
            return "Strong"
        elif points >= 4:
            return "Moderate"
        else:
            return "Weak"
    
    def _strength_to_score(self, strength: str) -> int:
        """Convert recommendation strength to numerical score for sorting."""
        return {"Strong": 3, "Moderate": 2, "Weak": 1}[strength]
    
    def _generate_additional_notes(
        self,
        protocol_data: Any,
        risk_score: Any,
        time_horizon_months: int
    ) -> str:
        """Generate additional notes about a strategy."""
        notes = []
        
        # Add time horizon specific notes
        if time_horizon_months < 3:
            notes.append(
                "Short time horizon: Consider gas costs impact on overall returns."
            )
        elif time_horizon_months > 12:
            notes.append(
                "Long time horizon: Consider protocol's track record and governance structure."
            )
        
        # Add protocol specific notes
        if protocol_data.type == "Liquid Staking":
            notes.append(
                "Liquid staking tokens can be used in other DeFi protocols for additional yield."
            )
        elif protocol_data.type == "Liquidity Pool":
            notes.append(
                "Monitor impermanent loss and consider active position management."
            )
        
        # Add risk specific notes
        if risk_score.technical_risk > 5:
            notes.append(
                "Higher technical complexity: Ensure understanding of protocol mechanics."
            )
        
        if risk_score.regulatory_risk > 5:
            notes.append(
                "Consider potential regulatory impacts on protocol operations."
            )
        
        return " ".join(notes)