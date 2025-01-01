import pytest
from decimal import Decimal
from typing import List, Dict

from ..enhanced_advisor import EnhancedDeFiAdvisor, StrategyRecommendation

@pytest.fixture
def advisor():
    return EnhancedDeFiAdvisor()

def test_get_strategy_recommendations_basic(advisor):
    """Test basic strategy recommendations."""
    recommendations = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=6,
        risk_preference="low"
    )
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    assert all(isinstance(r, StrategyRecommendation) for r in recommendations)

def test_get_strategy_recommendations_specific_protocols(advisor):
    """Test strategy recommendations for specific protocols."""
    specific_protocols = ["Lido", "Rocket Pool"]
    recommendations = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=6,
        risk_preference="low",
        specific_protocols=specific_protocols
    )
    
    assert len(recommendations) <= len(specific_protocols)
    assert all(r.protocol in specific_protocols for r in recommendations)

def test_get_strategy_recommendations_min_apy(advisor):
    """Test strategy recommendations with minimum APY filter."""
    min_apy = 5.0
    recommendations = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=6,
        risk_preference="medium",
        min_apy=min_apy
    )
    
    assert all(r.expected_roi > min_apy for r in recommendations)

def test_analyze_portfolio_allocation(advisor):
    """Test portfolio allocation analysis."""
    allocations = advisor.analyze_portfolio_allocation(
        amount=10.0,
        risk_preference="medium",
        time_horizon_months=6
    )
    
    assert isinstance(allocations, dict)
    assert len(allocations) > 0
    assert sum(allocations.values()) == pytest.approx(100.0)
    assert all(0 <= v <= 100 for v in allocations.values())

def test_risk_preference_filtering(advisor):
    """Test that risk preference properly filters recommendations."""
    low_risk_recs = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=6,
        risk_preference="low"
    )
    
    high_risk_recs = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=6,
        risk_preference="high"
    )
    
    # Low risk recommendations should not include high risk protocols
    low_risk_protocols = {r.protocol for r in low_risk_recs}
    assert "Uniswap V3 ETH/USDC" not in low_risk_protocols
    
    # High risk recommendations should include more volatile protocols
    high_risk_protocols = {r.protocol for r in high_risk_recs}
    assert any(p for p in high_risk_protocols if "Uniswap" in p or "Curve" in p)

def test_recommendation_sorting(advisor):
    """Test that recommendations are properly sorted."""
    recommendations = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=6,
        risk_preference="medium"
    )
    
    # Check that recommendations are sorted by strength and ROI
    for i in range(len(recommendations) - 1):
        current = recommendations[i]
        next_rec = recommendations[i + 1]
        
        current_score = advisor._strength_to_score(current.recommendation_strength)
        next_score = advisor._strength_to_score(next_rec.recommendation_strength)
        
        # If same strength, ROI should be higher or equal
        if current_score == next_score:
            assert current.expected_roi >= next_rec.expected_roi
        else:
            assert current_score > next_score

def test_pros_cons_analysis(advisor):
    """Test that pros and cons are properly analyzed."""
    recommendations = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=6,
        risk_preference="medium"
    )
    
    for rec in recommendations:
        assert len(rec.pros) > 0
        assert len(rec.cons) > 0
        assert isinstance(rec.pros, list)
        assert isinstance(rec.cons, list)
        assert all(isinstance(p, str) for p in rec.pros)
        assert all(isinstance(c, str) for c in rec.cons)

def test_additional_notes_generation(advisor):
    """Test that additional notes are properly generated."""
    # Test short time horizon
    short_term_recs = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=2,
        risk_preference="medium"
    )
    
    assert any("Short time horizon" in rec.additional_notes 
              for rec in short_term_recs)
    
    # Test long time horizon
    long_term_recs = advisor.get_strategy_recommendations(
        amount=10.0,
        time_horizon_months=24,
        risk_preference="medium"
    )
    
    assert any("Long time horizon" in rec.additional_notes 
              for rec in long_term_recs)

def test_gas_cost_impact(advisor):
    """Test that gas costs properly impact recommendations."""
    small_amount = advisor.get_strategy_recommendations(
        amount=0.1,  # Small amount where gas costs are significant
        time_horizon_months=6,
        risk_preference="medium"
    )
    
    large_amount = advisor.get_strategy_recommendations(
        amount=100.0,  # Large amount where gas costs are less significant
        time_horizon_months=6,
        risk_preference="medium"
    )
    
    # High gas cost protocols should rank lower for small amounts
    small_amount_ranks = {r.protocol: i for i, r in enumerate(small_amount)}
    large_amount_ranks = {r.protocol: i for i, r in enumerate(large_amount)}
    
    high_gas_protocols = ["Uniswap V3 ETH/USDC", "Curve ETH/stETH"]
    for protocol in high_gas_protocols:
        if protocol in small_amount_ranks and protocol in large_amount_ranks:
            assert small_amount_ranks[protocol] > large_amount_ranks[protocol]