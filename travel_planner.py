from smolagents import MultiStepAgent, tool, HfApiModel
from dotenv import load_dotenv
from huggingface_hub import login
import os

# Custom tool for getting travel time between locations
@tool
def get_travel_time(from_location: str, to_location: str) -> str:
    """
    Get the estimated travel time between two locations in Ho Chi Minh City using public transport.
    This is a simplified simulation.
    
    Args:
        from_location: Starting location in Ho Chi Minh City
        to_location: Destination in Ho Chi Minh City
    """
    # This is a dummy implementation - in a real scenario, you'd call a transit API
    travel_times = {
        ("Ben Thanh Market", "War Remnants Museum"): "15 minutes by bus route 1 or taxi",
        ("War Remnants Museum", "Notre-Dame Cathedral"): "10 minutes by taxi or 20 minutes walking",
        ("Notre-Dame Cathedral", "Central Post Office"): "2 minutes walking",
        ("Central Post Office", "Independence Palace"): "10 minutes walking",
        ("Independence Palace", "Ben Thanh Market"): "15 minutes walking or 5 minutes by taxi",
        ("Ben Thanh Market", "Bitexco Tower"): "10 minutes walking",
        ("Bitexco Tower", "Nguyen Hue Walking Street"): "5 minutes walking",
        ("Ben Thanh Market", "Cho Lon"): "25 minutes by bus route 1 or 15 minutes by taxi",
        ("War Remnants Museum", "Cu Chi Tunnels"): "1.5 hours by bus or 1 hour by taxi",
    }
    
    # Try both directions since our dictionary only stores one direction
    try:
        return travel_times[(from_location, to_location)]
    except KeyError:
        try:
            return travel_times[(to_location, from_location)]
        except KeyError:
            return "20-30 minutes by taxi or Grab bike (estimated)"

# Custom tool for getting location information
@tool
def get_location_info(location: str) -> str:
    """
    Get information about a location in Ho Chi Minh City.
    
    Args:
        location: Name of the location in Ho Chi Minh City
    """
    locations = {
        "Ben Thanh Market": "Open 6:00-24:00. Famous market for local goods, souvenirs, and street food. Best for shopping and experiencing local culture. More expensive than other markets but great for first-time visitors.",
        "War Remnants Museum": "Open 7:30-18:00 daily. Powerful museum displaying artifacts and photographs from the Vietnam War. Plan 1-2 hours for visit. Entrance fee: 40,000 VND.",
        "Notre-Dame Cathedral": "Open for viewing 8:00-17:00 daily. Historic cathedral from French colonial period. Note: Currently under renovation but exterior still viewable.",
        "Central Post Office": "Open 7:00-19:00 daily. Beautiful French colonial architecture, still functioning as a post office. Free entrance.",
        "Independence Palace": "Open 7:30-11:00, 13:00-16:00 daily. Historic palace from the Vietnam War era. Entrance fee: 40,000 VND.",
        "Bitexco Tower": "Observation deck open 9:30-21:30. City's iconic skyscraper with observation deck on 49th floor. Entrance fee: 200,000 VND.",
        "Nguyen Hue Walking Street": "Best visited evening/weekend. Pedestrian street with fountains, street performances, and cafes. Free to visit.",
        "Cho Lon": "Open all day. Historic Chinatown district with Binh Tay Market and pagodas. Best in morning for market activity.",
        "Cu Chi Tunnels": "Open 7:00-17:00 daily. Historic tunnel network from Vietnam War. Located 70km from city center. Entrance fee: 110,000 VND. Best to visit early morning to avoid heat."
    }
    return locations.get(location, "Information not available for this location.")

def main():
    # Login to Hugging Face
    login(token=os.getenv("HF_API_KEY"))
    
    # Initialize the agent
    agent = MultiStepAgent(
        tools=[get_travel_time, get_location_info],
        model=HfApiModel(model_id="mistralai/Mixtral-8x7B-Instruct-v0.1"),
        planning_interval=2  # Plan every 2 steps
    )
    
    # Query for Ho Chi Minh City
    result = agent.run(
        "Can you give me a nice one-day trip around Ho Chi Minh City with a few locations and "
        "the times? Could be in the city or outside, but should fit in one day. "
        "I'm travelling via public transportation, taxi, or Grab bike."
    )
    
    print("\nTravel Plan Result:")
    print(result)

if __name__ == "__main__":
    load_dotenv()
    main()