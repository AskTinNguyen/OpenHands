import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict

@pytest.fixture
def mock_token_info() -> Dict:
    """Mock token basic information."""
    return {
        "name": "Test Token",
        "symbol": "TEST",
        "type": "ERC20",
        "creation_date": datetime.utcnow() - timedelta(days=90),
        "total_supply": Decimal("1000000000"),
        "decimals": 18
    }

@pytest.fixture
def mock_holder_distribution() -> Dict:
    """Mock token holder distribution data."""
    return {
        "total_holders": 1000,
        "holders": [
            {
                "address": "0x1234...5678",
                "balance": Decimal("100000000"),
                "percentage": Decimal("10"),
                "rank": 1
            },
            {
                "address": "0x2345...6789",
                "balance": Decimal("50000000"),
                "percentage": Decimal("5"),
                "rank": 2
            }
        ],
        "distribution_stats": {
            "gini_coefficient": Decimal("0.85"),
            "top_10_percentage": Decimal("60"),
            "top_50_percentage": Decimal("80"),
            "top_100_percentage": Decimal("90")
        }
    }

@pytest.fixture
def mock_market_data() -> Dict:
    """Mock market data."""
    return {
        "price_usd": Decimal("1.23"),
        "market_cap_usd": Decimal("123000000"),
        "volume_24h_usd": Decimal("5000000"),
        "price_change_24h": Decimal("5.5"),
        "volume_change_24h": Decimal("10.2"),
        "liquidity_usd": Decimal("2000000"),
        "pairs": [
            {
                "dex": "uniswap_v2",
                "pair_address": "0x3456...7890",
                "liquidity_usd": Decimal("1500000"),
                "volume_24h_usd": Decimal("3000000")
            },
            {
                "dex": "sushiswap",
                "pair_address": "0x4567...8901",
                "liquidity_usd": Decimal("500000"),
                "volume_24h_usd": Decimal("2000000")
            }
        ]
    }

@pytest.fixture
def mock_contract_data() -> Dict:
    """Mock contract analysis data."""
    return {
        "is_verified": True,
        "compiler_version": "v0.8.17+commit.8df45f5f",
        "optimization_used": True,
        "runs": 200,
        "constructor_arguments": "0x",
        "source_code": "// SPDX-License-Identifier: MIT...",
        "abi": "[...]",
        "security_analysis": {
            "score": 85,
            "issues": [
                {
                    "severity": "medium",
                    "title": "Centralization Risk",
                    "description": "Owner has significant privileges"
                }
            ],
            "audit_reports": [
                {
                    "auditor": "CertiK",
                    "date": "2023-12-01",
                    "score": 90
                }
            ]
        }
    }

@pytest.fixture
def mock_transaction_history() -> Dict:
    """Mock transaction history data."""
    return {
        "transactions": [
            {
                "hash": "0x5678...9012",
                "timestamp": datetime.utcnow() - timedelta(hours=1),
                "from": "0x6789...0123",
                "to": "0x7890...1234",
                "value": Decimal("1000000"),
                "gas_used": 150000,
                "gas_price": 50000000000
            }
        ],
        "transfer_events": [
            {
                "hash": "0x8901...2345",
                "timestamp": datetime.utcnow() - timedelta(hours=2),
                "from": "0x9012...3456",
                "to": "0x0123...4567",
                "value": Decimal("500000")
            }
        ]
    }

@pytest.fixture
def mock_social_metrics() -> Dict:
    """Mock social metrics data."""
    return {
        "twitter": {
            "followers": 10000,
            "engagement_rate": Decimal("2.5"),
            "sentiment_score": Decimal("0.75")
        },
        "telegram": {
            "members": 5000,
            "active_members": 1000,
            "messages_24h": 500
        },
        "github": {
            "stars": 150,
            "forks": 30,
            "contributors": 10,
            "commits_7d": 25
        }
    }

@pytest.fixture
def mock_risk_metrics() -> Dict:
    """Mock risk metrics data."""
    return {
        "overall_risk_score": Decimal("65"),
        "risk_factors": {
            "centralization_risk": "medium",
            "liquidity_risk": "low",
            "volatility_risk": "high",
            "contract_risk": "low"
        },
        "warning_flags": [
            "High concentration in top wallets",
            "Above average volatility"
        ],
        "recommendations": [
            "Monitor whale movements",
            "Set strict stop losses"
        ]
    }