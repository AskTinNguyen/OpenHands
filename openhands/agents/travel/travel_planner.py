from smolagents import MultiStepAgent, HfApiModel
from .tools import get_travel_time, get_location_info

class TravelPlannerAgent:
    """
    An AI agent specialized in creating detailed travel itineraries.
    
    This agent helps plan city tours by:
    - Suggesting optimal routes between attractions
    - Providing information about locations
    - Estimating travel times
    - Creating time-optimized itineraries
    
    The agent considers factors like:
    - Opening hours
    - Travel times between locations
    - Best times to visit specific attractions
    - Public transportation options
    """
    
    def __init__(self, model_id: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
        """
        Initialize the Travel Planner Agent.
        
        Args:
            model_id: The ID of the language model to use for planning
        """
        self.agent = MultiStepAgent(
            tools=[get_travel_time, get_location_info],
            model=HfApiModel(model_id=model_id),
            planning_interval=2
        )
    
    def plan_city_tour(
        self,
        city: str,
        duration_days: int = 1,
        preferences: str = None,
        transportation: str = "public"
    ) -> str:
        """
        Create a detailed city tour itinerary.
        
        Args:
            city: Name of the city to visit
            duration_days: Number of days for the tour
            preferences: Optional string describing preferences (e.g., "cultural", "historical")
            transportation: Preferred mode of transportation
        
        Returns:
            A detailed itinerary string
        """
        # Build the query based on parameters
        query = (
            f"Can you give me a nice {duration_days}-day trip around {city} "
            f"with locations and times? "
        )
        
        if preferences:
            query += f"I'm particularly interested in {preferences}. "
        
        query += f"I'm travelling via {transportation} transportation."
        
        return self.agent.run(query)
    
    def get_location_details(self, city: str, location: str) -> str:
        """
        Get detailed information about a specific location.
        
        Args:
            city: Name of the city
            location: Name of the location
        
        Returns:
            Detailed information about the location
        """
        query = (
            f"Please provide detailed information about {location} in {city}, "
            "including opening hours, best times to visit, and any special considerations."
        )
        
        return self.agent.run(query)
    
    def optimize_route(
        self,
        city: str,
        locations: list,
        start_time: str,
        transportation: str = "public"
    ) -> str:
        """
        Optimize a route between multiple locations.
        
        Args:
            city: Name of the city
            locations: List of locations to visit
            start_time: Starting time for the tour
            transportation: Preferred mode of transportation
        
        Returns:
            An optimized route with timing details
        """
        locations_str = ", ".join(locations)
        query = (
            f"Please help me optimize a route in {city} to visit these locations: "
            f"{locations_str}. I'll start at {start_time} and use {transportation} "
            "transportation. Please consider opening hours and travel times."
        )
        
        return self.agent.run(query)
    
    def estimate_travel_time(
        self,
        city: str,
        from_location: str,
        to_location: str,
        transportation: str = "public"
    ) -> str:
        """
        Estimate travel time between two locations.
        
        Args:
            city: Name of the city
            from_location: Starting location
            to_location: Destination location
            transportation: Preferred mode of transportation
        
        Returns:
            Estimated travel time and route details
        """
        query = (
            f"How long would it take to travel from {from_location} to {to_location} "
            f"in {city} using {transportation} transportation? Please provide route details."
        )
        
        return self.agent.run(query)