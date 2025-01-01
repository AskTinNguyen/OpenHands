from typing import Dict, List, Optional
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class YieldStrategy:
    protocol: str
    apy: str
    tvl: str
    risk_level: str
    description: str
    min_amount: str
    gas_cost: str
    impermanent_loss_risk: str

@dataclass
class GasCosts:
    deposit: str
    withdrawal: str
    frequency: str

@dataclass
class RiskDetails:
    audits: List[str]
    insurance_available: bool
    governance: str
    years_active: int

@dataclass
class RiskScore:
    smart_contract_risk: int
    centralization_risk: int
    regulatory_risk: int
    market_risk: int
    technical_risk: int
    details: RiskDetails

@dataclass
class ProtocolData:
    type: str
    apy: float
    tvl_billions: float
    insurance: str
    min_deposit: float
    withdrawal_time: str
    unique_features: List[str]

class DeFiTools:
    """Collection of tools for DeFi analysis and recommendations."""
    
    @staticmethod
    def get_eth_yield_strategies() -> Dict[str, YieldStrategy]:
        """Get current yield strategies available for ETH across major DeFi protocols."""
        return {
            "Lido": YieldStrategy(
                protocol="Liquid Staking",
                apy="3.8%",
                tvl="$19.2B",
                risk_level="Low",
                description="Liquid staking solution for ETH 2.0. Receive stETH while staking.",
                min_amount="0.01 ETH",
                gas_cost="Medium",
                impermanent_loss_risk="None"
            ),
            "Rocket Pool": YieldStrategy(
                protocol="Liquid Staking",
                apy="3.75%",
                tvl="$4.1B",
                risk_level="Low",
                description="Decentralized ETH staking protocol. Receive rETH while staking.",
                min_amount="0.01 ETH",
                gas_cost="Medium",
                impermanent_loss_risk="None"
            ),
            "Aave V3": YieldStrategy(
                protocol="Lending",
                apy="1.2% supply + 2.1% rewards",
                tvl="$5.8B",
                risk_level="Low-Medium",
                description="Supply ETH to earn interest and additional rewards in AAVE tokens.",
                min_amount="0.001 ETH",
                gas_cost="High",
                impermanent_loss_risk="None"
            ),
            "Curve ETH/stETH": YieldStrategy(
                protocol="Liquidity Pool",
                apy="3.5% + 0.8% fees",
                tvl="$1.2B",
                risk_level="Medium",
                description="Provide liquidity to ETH/stETH pool. Earn trading fees and CRV rewards.",
                min_amount="0.01 ETH",
                gas_cost="High",
                impermanent_loss_risk="Low"
            ),
            "Uniswap V3 ETH/USDC": YieldStrategy(
                protocol="Liquidity Pool",
                apy="5-20% (variable)",
                tvl="$500M",
                risk_level="High",
                description="Concentrated liquidity provision. Higher returns but requires active management.",
                min_amount="0.1 ETH",
                gas_cost="Very High",
                impermanent_loss_risk="High"
            )
        }
    
    @staticmethod
    def analyze_gas_costs(strategy: str) -> Optional[GasCosts]:
        """Analyze the current gas costs for implementing a specific DeFi strategy."""
        gas_estimates = {
            "Lido": GasCosts(
                deposit="~$30-40",
                withdrawal="~$15-20",
                frequency="One-time deposit, withdrawal when needed"
            ),
            "Rocket Pool": GasCosts(
                deposit="~$35-45",
                withdrawal="~$20-25",
                frequency="One-time deposit, withdrawal when needed"
            ),
            "Aave V3": GasCosts(
                deposit="~$50-70",
                withdrawal="~$40-60",
                frequency="One-time deposit, withdrawal when needed"
            ),
            "Curve ETH/stETH": GasCosts(
                deposit="~$80-100",
                withdrawal="~$60-80",
                frequency="One-time deposit, withdrawal when needed, harvesting rewards ~weekly"
            ),
            "Uniswap V3 ETH/USDC": GasCosts(
                deposit="~$100-150",
                withdrawal="~$80-100",
                frequency="One-time deposit, position management costs vary"
            )
        }
        return gas_estimates.get(strategy)
    
    @staticmethod
    def calculate_roi(amount: float, strategy: str, time_period_months: int) -> Dict[str, float]:
        """Calculate estimated ROI for a given amount of ETH in a specific strategy."""
        roi_data = {
            "Lido": {
                "base_apy": 0.038,
                "extra_rewards": 0,
                "gas_cost_eth": 0.02,
            },
            "Rocket Pool": {
                "base_apy": 0.0375,
                "extra_rewards": 0,
                "gas_cost_eth": 0.022,
            },
            "Aave V3": {
                "base_apy": 0.012,
                "extra_rewards": 0.021,
                "gas_cost_eth": 0.035,
            },
            "Curve ETH/stETH": {
                "base_apy": 0.035,
                "extra_rewards": 0.008,
                "gas_cost_eth": 0.05,
            },
            "Uniswap V3 ETH/USDC": {
                "base_apy": 0.10,
                "extra_rewards": 0,
                "gas_cost_eth": 0.07,
            }
        }
        
        if strategy not in roi_data:
            return {}
        
        data = roi_data[strategy]
        
        # Calculate returns with compound interest
        base_rate = data["base_apy"] / 12  # Monthly rate
        extra_rate = data["extra_rewards"] / 12  # Monthly rate
        
        # Compound interest formula: A = P(1 + r)^t
        base_return = amount * ((1 + base_rate) ** time_period_months - 1)
        extra_return = amount * ((1 + extra_rate) ** time_period_months - 1)
        total_return = base_return + extra_return - data["gas_cost_eth"]
        roi_percentage = (total_return / amount) * 100
        
        return {
            "base_return": base_return,
            "extra_return": extra_return,
            "gas_cost": data["gas_cost_eth"],
            "total_return": total_return,
            "roi_percentage": roi_percentage
        }
    
    @staticmethod
    def analyze_risk_score(strategy: str) -> Optional[RiskScore]:
        """Analyze the risk level of a specific DeFi strategy."""
        risk_scores = {
            "Lido": RiskScore(
                smart_contract_risk=2,
                centralization_risk=4,
                regulatory_risk=3,
                market_risk=2,
                technical_risk=2,
                details=RiskDetails(
                    audits=["Quantstamp", "Sigma Prime", "Trail of Bits"],
                    insurance_available=True,
                    governance="DAO",
                    years_active=3
                )
            ),
            "Rocket Pool": RiskScore(
                smart_contract_risk=3,
                centralization_risk=2,
                regulatory_risk=3,
                market_risk=2,
                technical_risk=3,
                details=RiskDetails(
                    audits=["ConsenSys Diligence", "Trail of Bits"],
                    insurance_available=True,
                    governance="Decentralized DAO",
                    years_active=2
                )
            ),
            "Aave V3": RiskScore(
                smart_contract_risk=2,
                centralization_risk=3,
                regulatory_risk=4,
                market_risk=3,
                technical_risk=2,
                details=RiskDetails(
                    audits=["OpenZeppelin", "SigmaPrime", "ABDK"],
                    insurance_available=True,
                    governance="DAO",
                    years_active=4
                )
            ),
            "Curve ETH/stETH": RiskScore(
                smart_contract_risk=3,
                centralization_risk=3,
                regulatory_risk=3,
                market_risk=4,
                technical_risk=3,
                details=RiskDetails(
                    audits=["Trail of Bits", "MixBytes"],
                    insurance_available=True,
                    governance="DAO",
                    years_active=3
                )
            ),
            "Uniswap V3 ETH/USDC": RiskScore(
                smart_contract_risk=3,
                centralization_risk=2,
                regulatory_risk=4,
                market_risk=7,
                technical_risk=5,
                details=RiskDetails(
                    audits=["Trail of Bits", "ABDK"],
                    insurance_available=True,
                    governance="DAO",
                    years_active=2
                )
            )
        }
        return risk_scores.get(strategy)
    
    @staticmethod
    def get_protocol_data(protocol: str) -> Optional[ProtocolData]:
        """Get detailed data for a specific protocol."""
        protocol_data = {
            "Lido": ProtocolData(
                type="Liquid Staking",
                apy=3.8,
                tvl_billions=19.2,
                insurance="Yes",
                min_deposit=0.01,
                withdrawal_time="Instant for stETH, variable for ETH",
                unique_features=["No minimum stake", "Liquid staking derivative", "Wide integration"]
            ),
            "Rocket Pool": ProtocolData(
                type="Liquid Staking",
                apy=3.75,
                tvl_billions=4.1,
                insurance="Yes",
                min_deposit=0.01,
                withdrawal_time="Instant for rETH, variable for ETH",
                unique_features=["Decentralized node operators", "Lower minimum stake", "Node operator opportunities"]
            ),
            "Aave V3": ProtocolData(
                type="Lending",
                apy=3.3,
                tvl_billions=5.8,
                insurance="Yes",
                min_deposit=0.001,
                withdrawal_time="Instant",
                unique_features=["Multiple asset types", "Flash loans", "Isolation mode"]
            ),
            "Curve ETH/stETH": ProtocolData(
                type="Liquidity Pool",
                apy=4.3,
                tvl_billions=1.2,
                insurance="Yes",
                min_deposit=0.01,
                withdrawal_time="Instant",
                unique_features=["Low slippage", "CRV rewards", "Stable pair focus"]
            ),
            "Uniswap V3 ETH/USDC": ProtocolData(
                type="Liquidity Pool",
                apy=12.5,  # Using median of 5-20% range
                tvl_billions=0.5,
                insurance="No",
                min_deposit=0.1,
                withdrawal_time="Instant",
                unique_features=["Concentrated liquidity", "Custom fee tiers", "Active management"]
            )
        }
        return protocol_data.get(protocol)