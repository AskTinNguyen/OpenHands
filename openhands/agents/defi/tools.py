from smolagents import tool
from typing import Dict

@tool
def get_eth_yield_strategies() -> str:
    """
    Get current yield strategies available for ETH across major DeFi protocols.
    Returns a list of protocols with their APY and TVL.
    """
    strategies = {
        "Lido": {
            "protocol": "Liquid Staking",
            "apy": "3.8%",
            "tvl": "$19.2B",
            "risk_level": "Low",
            "description": "Liquid staking solution for ETH 2.0. Receive stETH while staking.",
            "min_amount": "0.01 ETH",
            "gas_cost": "Medium",
            "impermanent_loss_risk": "None"
        },
        "Rocket Pool": {
            "protocol": "Liquid Staking",
            "apy": "3.75%",
            "tvl": "$4.1B",
            "risk_level": "Low",
            "description": "Decentralized ETH staking protocol. Receive rETH while staking.",
            "min_amount": "0.01 ETH",
            "gas_cost": "Medium",
            "impermanent_loss_risk": "None"
        },
        "Aave V3": {
            "protocol": "Lending",
            "apy": "1.2% supply + 2.1% rewards",
            "tvl": "$5.8B",
            "risk_level": "Low-Medium",
            "description": "Supply ETH to earn interest and additional rewards in AAVE tokens.",
            "min_amount": "0.001 ETH",
            "gas_cost": "High",
            "impermanent_loss_risk": "None"
        },
        "Curve ETH/stETH": {
            "protocol": "Liquidity Pool",
            "apy": "3.5% + 0.8% fees",
            "tvl": "$1.2B",
            "risk_level": "Medium",
            "description": "Provide liquidity to ETH/stETH pool. Earn trading fees and CRV rewards.",
            "min_amount": "0.01 ETH",
            "gas_cost": "High",
            "impermanent_loss_risk": "Low"
        },
        "Uniswap V3 ETH/USDC": {
            "protocol": "Liquidity Pool",
            "apy": "5-20% (variable)",
            "tvl": "$500M",
            "risk_level": "High",
            "description": "Concentrated liquidity provision. Higher returns but requires active management.",
            "min_amount": "0.1 ETH",
            "gas_cost": "Very High",
            "impermanent_loss_risk": "High"
        }
    }
    
    return "\n".join([
        f"{name}:\n" + "\n".join(f"  {k}: {v}" for k, v in details.items())
        for name, details in strategies.items()
    ])

@tool
def analyze_gas_costs(strategy: str) -> str:
    """
    Analyze the current gas costs for implementing a specific DeFi strategy.
    
    Args:
        strategy: Name of the DeFi strategy/protocol to analyze
    """
    gas_estimates = {
        "Lido": {
            "deposit": "~$30-40",
            "withdrawal": "~$15-20",
            "frequency": "One-time deposit, withdrawal when needed"
        },
        "Rocket Pool": {
            "deposit": "~$35-45",
            "withdrawal": "~$20-25",
            "frequency": "One-time deposit, withdrawal when needed"
        },
        "Aave V3": {
            "deposit": "~$50-70",
            "withdrawal": "~$40-60",
            "frequency": "One-time deposit, withdrawal when needed"
        },
        "Curve ETH/stETH": {
            "deposit": "~$80-100",
            "withdrawal": "~$60-80",
            "frequency": "One-time deposit, withdrawal when needed, harvesting rewards ~weekly"
        },
        "Uniswap V3 ETH/USDC": {
            "deposit": "~$100-150",
            "withdrawal": "~$80-100",
            "frequency": "One-time deposit, position management costs vary"
        }
    }
    
    if strategy not in gas_estimates:
        return f"Gas cost information not available for {strategy}"
    
    info = gas_estimates[strategy]
    return f"Gas costs for {strategy}:\n" + "\n".join(f"- {k}: {v}" for k, v in info.items())

@tool
def calculate_roi(amount: float, strategy: str, time_period_months: int) -> str:
    """
    Calculate estimated ROI for a given amount of ETH in a specific strategy.
    
    Args:
        amount: Amount of ETH to invest
        strategy: Name of the DeFi strategy/protocol
        time_period_months: Investment period in months
    """
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
        return f"ROI calculation not available for {strategy}"
    
    data = roi_data[strategy]
    
    # Simple ROI calculation (not compound interest for simplicity)
    base_return = amount * data["base_apy"] * (time_period_months / 12)
    extra_return = amount * data["extra_rewards"] * (time_period_months / 12)
    total_return = base_return + extra_return - data["gas_cost_eth"]
    roi_percentage = (total_return / amount) * 100
    
    return (
        f"ROI Analysis for {strategy} with {amount} ETH over {time_period_months} months:\n"
        f"- Estimated base returns: {base_return:.4f} ETH\n"
        f"- Estimated extra rewards: {extra_return:.4f} ETH\n"
        f"- Estimated gas costs: {data['gas_cost_eth']} ETH\n"
        f"- Net return: {total_return:.4f} ETH\n"
        f"- ROI: {roi_percentage:.2f}%"
    )

@tool
def analyze_risk_score(strategy: str) -> str:
    """
    Analyze the risk level of a specific DeFi strategy and provide a detailed risk breakdown.
    
    Args:
        strategy: Name of the DeFi strategy/protocol to analyze
    """
    risk_scores = {
        "Lido": {
            "smart_contract_risk": 2,  # 1-10 scale
            "centralization_risk": 4,
            "regulatory_risk": 3,
            "market_risk": 2,
            "technical_risk": 2,
            "details": {
                "audits": ["Quantstamp", "Sigma Prime", "Trail of Bits"],
                "insurance_available": True,
                "governance": "DAO",
                "years_active": 3
            }
        },
        "Rocket Pool": {
            "smart_contract_risk": 3,
            "centralization_risk": 2,
            "regulatory_risk": 3,
            "market_risk": 2,
            "technical_risk": 3,
            "details": {
                "audits": ["ConsenSys Diligence", "Trail of Bits"],
                "insurance_available": True,
                "governance": "Decentralized DAO",
                "years_active": 2
            }
        },
        "Aave V3": {
            "smart_contract_risk": 2,
            "centralization_risk": 3,
            "regulatory_risk": 4,
            "market_risk": 3,
            "technical_risk": 2,
            "details": {
                "audits": ["OpenZeppelin", "SigmaPrime", "ABDK"],
                "insurance_available": True,
                "governance": "DAO",
                "years_active": 4
            }
        },
        "Curve ETH/stETH": {
            "smart_contract_risk": 3,
            "centralization_risk": 3,
            "regulatory_risk": 3,
            "market_risk": 4,
            "technical_risk": 3,
            "details": {
                "audits": ["Trail of Bits", "MixBytes"],
                "insurance_available": True,
                "governance": "DAO",
                "years_active": 3
            }
        },
        "Uniswap V3 ETH/USDC": {
            "smart_contract_risk": 3,
            "centralization_risk": 2,
            "regulatory_risk": 4,
            "market_risk": 7,
            "technical_risk": 5,
            "details": {
                "audits": ["Trail of Bits", "ABDK"],
                "insurance_available": True,
                "governance": "DAO",
                "years_active": 2
            }
        }
    }
    
    if strategy not in risk_scores:
        return f"Risk analysis not available for {strategy}"
    
    score = risk_scores[strategy]
    total_risk = sum([
        score["smart_contract_risk"],
        score["centralization_risk"],
        score["regulatory_risk"],
        score["market_risk"],
        score["technical_risk"]
    ]) / 5.0
    
    details = score["details"]
    return (
        f"Risk Analysis for {strategy}:\n"
        f"Overall Risk Score: {total_risk:.1f}/10 (lower is better)\n\n"
        f"Breakdown:\n"
        f"- Smart Contract Risk: {score['smart_contract_risk']}/10\n"
        f"- Centralization Risk: {score['centralization_risk']}/10\n"
        f"- Regulatory Risk: {score['regulatory_risk']}/10\n"
        f"- Market Risk: {score['market_risk']}/10\n"
        f"- Technical Risk: {score['technical_risk']}/10\n\n"
        f"Additional Details:\n"
        f"- Audits: {', '.join(details['audits'])}\n"
        f"- Insurance Available: {'Yes' if details['insurance_available'] else 'No'}\n"
        f"- Governance: {details['governance']}\n"
        f"- Years Active: {details['years_active']}"
    )

@tool
def compare_protocols(protocol1: str, protocol2: str) -> str:
    """
    Compare two DeFi protocols across various metrics.
    
    Args:
        protocol1: Name of the first protocol to compare
        protocol2: Name of the second protocol to compare
    """
    def get_protocol_data(name: str) -> Dict:
        protocol_data = {
            "Lido": {
                "type": "Liquid Staking",
                "apy": 3.8,
                "tvl_billions": 19.2,
                "insurance": "Yes",
                "min_deposit": 0.01,
                "withdrawal_time": "Instant for stETH, variable for ETH",
                "unique_features": ["No minimum stake", "Liquid staking derivative", "Wide integration"]
            },
            "Rocket Pool": {
                "type": "Liquid Staking",
                "apy": 3.75,
                "tvl_billions": 4.1,
                "insurance": "Yes",
                "min_deposit": 0.01,
                "withdrawal_time": "Instant for rETH, variable for ETH",
                "unique_features": ["Decentralized node operators", "Lower minimum stake", "Node operator opportunities"]
            },
            "Aave V3": {
                "type": "Lending",
                "apy": 3.3,
                "tvl_billions": 5.8,
                "insurance": "Yes",
                "min_deposit": 0.001,
                "withdrawal_time": "Instant",
                "unique_features": ["Multiple asset types", "Flash loans", "Isolation mode"]
            },
            "Curve ETH/stETH": {
                "type": "Liquidity Pool",
                "apy": 4.3,
                "tvl_billions": 1.2,
                "insurance": "Yes",
                "min_deposit": 0.01,
                "withdrawal_time": "Instant",
                "unique_features": ["Low slippage", "CRV rewards", "Stable pair focus"]
            },
            "Uniswap V3 ETH/USDC": {
                "type": "Liquidity Pool",
                "apy": "5-20",
                "tvl_billions": 0.5,
                "insurance": "No",
                "min_deposit": 0.1,
                "withdrawal_time": "Instant",
                "unique_features": ["Concentrated liquidity", "Custom fee tiers", "Active management"]
            }
        }
        return protocol_data.get(name, {})
    
    p1_data = get_protocol_data(protocol1)
    p2_data = get_protocol_data(protocol2)
    
    if not p1_data or not p2_data:
        return f"Comparison not available for {protocol1} and/or {protocol2}"
    
    return (
        f"Comparison: {protocol1} vs {protocol2}\n\n"
        f"Protocol Type:\n"
        f"- {protocol1}: {p1_data['type']}\n"
        f"- {protocol2}: {p2_data['type']}\n\n"
        f"Current APY:\n"
        f"- {protocol1}: {p1_data['apy']}%\n"
        f"- {protocol2}: {p2_data['apy']}%\n\n"
        f"TVL (Billions):\n"
        f"- {protocol1}: ${p1_data['tvl_billions']}B\n"
        f"- {protocol2}: ${p2_data['tvl_billions']}B\n\n"
        f"Insurance Available:\n"
        f"- {protocol1}: {p1_data['insurance']}\n"
        f"- {protocol2}: {p2_data['insurance']}\n\n"
        f"Minimum Deposit:\n"
        f"- {protocol1}: {p1_data['min_deposit']} ETH\n"
        f"- {protocol2}: {p2_data['min_deposit']} ETH\n\n"
        f"Withdrawal Time:\n"
        f"- {protocol1}: {p1_data['withdrawal_time']}\n"
        f"- {protocol2}: {p2_data['withdrawal_time']}\n\n"
        f"Unique Features:\n"
        f"- {protocol1}: {', '.join(p1_data['unique_features'])}\n"
        f"- {protocol2}: {', '.join(p2_data['unique_features'])}"
    )