from smolagents import MultiStepAgent, HfApiModel
from .tools.defi_tools import DeFiTools

class DeFiAdvisorAgent:
    """
    An AI agent specialized in providing DeFi yield strategy recommendations.
    
    This agent analyzes various DeFi protocols and provides recommendations based on:
    - Yield rates (APY)
    - Gas costs
    - Risk assessment
    - Protocol comparison
    - ROI calculations
    
    The agent uses multiple specialized tools to gather and analyze data, providing
    comprehensive advice tailored to the user's requirements.
    """
    
    def __init__(self, model_id: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
        """
        Initialize the DeFi Advisor Agent.
        
        Args:
            model_id: The ID of the language model to use for analysis
        """
        self.agent = MultiStepAgent(
            tools=[
                get_eth_yield_strategies,
                analyze_gas_costs,
                calculate_roi,
                analyze_risk_score,
                compare_protocols
            ],
            model=HfApiModel(model_id=model_id),
            planning_interval=2
        )
    
    def get_strategy_recommendation(
        self,
        amount: float,
        time_horizon_months: int = 6,
        risk_preference: str = "medium",
        specific_protocols: list = None
    ) -> str:
        """
        Get a DeFi strategy recommendation based on user preferences.
        
        Args:
            amount: Amount of ETH to invest
            time_horizon_months: Investment time horizon in months
            risk_preference: Risk preference ("low", "medium", or "high")
            specific_protocols: Optional list of specific protocols to analyze
        
        Returns:
            A detailed recommendation string including analysis and comparisons
        """
        # Build the query based on parameters
        query = (
            f"I have {amount} ETH that I want to put to work for yield. "
            f"My time horizon is {time_horizon_months} months and I prefer "
            f"{risk_preference}-risk options. "
        )
        
        if specific_protocols:
            protocols_str = ", ".join(specific_protocols)
            query += f"I'm particularly interested in comparing {protocols_str}, "
            query += "but I'm also open to other options. "
        
        query += (
            "Please provide a detailed analysis of the best options, "
            "including risks, rewards, and gas costs."
        )
        
        return self.agent.run(query)
    
    def compare_specific_protocols(self, protocol1: str, protocol2: str) -> str:
        """
        Get a detailed comparison between two specific protocols.
        
        Args:
            protocol1: Name of the first protocol
            protocol2: Name of the second protocol
        
        Returns:
            A detailed comparison including yields, risks, and costs
        """
        query = (
            f"Please provide a detailed comparison between {protocol1} and {protocol2}, "
            "including their yields, risks, gas costs, and other important factors. "
            "Which one would you recommend and why?"
        )
        
        return self.agent.run(query)
    
    def analyze_protocol_risks(self, protocol: str) -> str:
        """
        Get a detailed risk analysis for a specific protocol.
        
        Args:
            protocol: Name of the protocol to analyze
        
        Returns:
            A detailed risk analysis
        """
        query = (
            f"Please provide a comprehensive risk analysis for {protocol}, "
            "including smart contract risk, centralization risk, and market risk. "
            "What are the main risk factors to consider?"
        )
        
        return self.agent.run(query)
    
    def calculate_strategy_roi(
        self,
        amount: float,
        protocol: str,
        time_horizon_months: int
    ) -> str:
        """
        Calculate the potential ROI for a specific strategy.
        
        Args:
            amount: Amount of ETH to invest
            protocol: Name of the protocol
            time_horizon_months: Investment time horizon in months
        
        Returns:
            A detailed ROI analysis including gas costs and rewards
        """
        query = (
            f"Please calculate and analyze the potential ROI for investing {amount} ETH "
            f"in {protocol} over {time_horizon_months} months. Include gas costs, "
            "rewards, and any other relevant factors in the analysis."
        )
        
        return self.agent.run(query)