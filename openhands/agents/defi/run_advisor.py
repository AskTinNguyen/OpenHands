from openhands.agents.defi.enhanced_advisor import EnhancedDeFiAdvisor

def format_recommendation(rec):
    """Format a single recommendation for display."""
    # Format verification data
    verification_info = []
    for data_type, data in rec.verification_data.items():
        if data_type != "overall":
            verification_info.append(f"{data_type.upper()}:")
            verification_info.append(f"- Confidence Score: {data['confidence']:.2f}")
            verification_info.append("- Verification Sources:")
            for source in data['sources']:
                verification_info.append(f"  * {source}")
            verification_info.append("")

    # Format references
    reference_info = []
    for ref_type, links in rec.references.items():
        if isinstance(links, str):
            reference_info.append(f"{ref_type.replace('_', ' ').title()}: {links}")
        else:
            reference_info.append(f"{ref_type.replace('_', ' ').title()}:")
            for link in links:
                reference_info.append(f"- {link}")
            reference_info.append("")

    return f"""
{'='*80}
Protocol: {rec.protocol} ({rec.recommendation_strength} Recommendation)
{'='*80}
Expected ROI: {rec.expected_roi:.2f}%
Risk Level: {rec.risk_level}

Gas Costs:
- Deposit: {rec.gas_costs['deposit']}
- Withdrawal: {rec.gas_costs['withdrawal']}

Pros:
{chr(10).join('- ' + pro for pro in rec.pros)}

Cons:
{chr(10).join('- ' + con for con in rec.cons)}

Additional Notes:
{rec.additional_notes}

Data Verification:
{chr(10).join(verification_info)}

References:
{chr(10).join(reference_info)}

Overall Verification Confidence: {rec.verification_data['overall']['overall_confidence']:.2f}
Last Updated: {rec.verification_data['overall']['last_updated']}
"""

def main():
    # Initialize the advisor
    advisor = EnhancedDeFiAdvisor()
    
    print("DeFi Advisor Analysis")
    print("="*80)
    
    # Get recommendations for different scenarios
    print("\n1. Conservative Strategy (10 ETH, 6 months, low risk)")
    print("-"*80)
    conservative_recs = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=6,
        risk_preference="low"
    )
    for rec in conservative_recs[:2]:  # Show top 2 recommendations
        print(format_recommendation(rec))
    
    print("\n2. Balanced Strategy (10 ETH, 12 months, medium risk)")
    print("-"*80)
    balanced_recs = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=12,
        risk_preference="medium"
    )
    for rec in balanced_recs[:2]:  # Show top 2 recommendations
        print(format_recommendation(rec))
    
    print("\n3. Aggressive Strategy (10 ETH, 24 months, high risk)")
    print("-"*80)
    aggressive_recs = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=24,
        risk_preference="high"
    )
    for rec in aggressive_recs[:2]:  # Show top 2 recommendations
        print(format_recommendation(rec))
    
    print("\n4. Portfolio Allocation Recommendation (10 ETH, balanced)")
    print("-"*80)
    allocations = advisor.analyze_portfolio_allocation(
        amount=10.0,
        risk_preference="medium",
        time_horizon_months=12
    )
    print("\nRecommended Portfolio Allocation:")
    for protocol, percentage in allocations.items():
        print(f"- {protocol}: {percentage:.1f}%")
    
    print("\n5. Specific Protocol Analysis (Lido vs Rocket Pool)")
    print("-"*80)
    specific_recs = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=6,
        risk_preference="medium",
        specific_protocols=["Lido", "Rocket Pool"]
    )
    for rec in specific_recs:
        print(format_recommendation(rec))

if __name__ == "__main__":
    main()