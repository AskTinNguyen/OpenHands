from smolagents import tool
from typing import Dict

class CityData:
    """Helper class to store city-specific data"""
    
    @staticmethod
    def get_city_data(city: str) -> Dict:
        """Get travel data for a specific city"""
        city_data = {
            "Paris": {
                "locations": {
                    "Eiffel Tower": "Open 9:00-00:45 in summer. Iconic iron tower with city views. Best visited early morning or sunset.",
                    "Louvre": "Open Wed-Mon 9:00-18:00. World's largest art museum, home to the Mona Lisa. Closed Tuesdays.",
                    "Montmartre": "Historic district on a hill, famous for Sacré-Cœur basilica and artist square. Best in morning or late afternoon.",
                    "Notre-Dame": "Cathedral under reconstruction. Plaza and exterior viewable 24/7.",
                    "Versailles": "Palace open Tue-Sun 9:00-18:30. Closed Mondays. Plan at least half day for palace and gardens."
                },
                "travel_times": {
                    ("Eiffel Tower", "Louvre"): "25 minutes by Metro line 9",
                    ("Louvre", "Montmartre"): "20 minutes by Metro line 12",
                    ("Montmartre", "Notre-Dame"): "30 minutes by Metro line 12 and 4",
                    ("Notre-Dame", "Versailles"): "1 hour by RER C",
                    ("Eiffel Tower", "Versailles"): "45 minutes by RER C"
                }
            },
            "Ho Chi Minh City": {
                "locations": {
                    "Ben Thanh Market": "Open 6:00-24:00. Famous market for local goods, souvenirs, and street food. Best for shopping and experiencing local culture.",
                    "War Remnants Museum": "Open 7:30-18:00 daily. Powerful museum displaying artifacts and photographs from the Vietnam War. Plan 1-2 hours for visit.",
                    "Notre-Dame Cathedral": "Open for viewing 8:00-17:00 daily. Historic cathedral from French colonial period. Note: Currently under renovation but exterior still viewable.",
                    "Central Post Office": "Open 7:00-19:00 daily. Beautiful French colonial architecture, still functioning as a post office. Free entrance.",
                    "Independence Palace": "Open 7:30-11:00, 13:00-16:00 daily. Historic palace from the Vietnam War era.",
                    "Bitexco Tower": "Observation deck open 9:30-21:30. City's iconic skyscraper with observation deck on 49th floor.",
                    "Nguyen Hue Walking Street": "Best visited evening/weekend. Pedestrian street with fountains, street performances, and cafes.",
                    "Cho Lon": "Open all day. Historic Chinatown district with Binh Tay Market and pagodas. Best in morning for market activity.",
                    "Cu Chi Tunnels": "Open 7:00-17:00 daily. Historic tunnel network from Vietnam War. Located 70km from city center."
                },
                "travel_times": {
                    ("Ben Thanh Market", "War Remnants Museum"): "15 minutes by bus route 1 or taxi",
                    ("War Remnants Museum", "Notre-Dame Cathedral"): "10 minutes by taxi or 20 minutes walking",
                    ("Notre-Dame Cathedral", "Central Post Office"): "2 minutes walking",
                    ("Central Post Office", "Independence Palace"): "10 minutes walking",
                    ("Independence Palace", "Ben Thanh Market"): "15 minutes walking or 5 minutes by taxi",
                    ("Ben Thanh Market", "Bitexco Tower"): "10 minutes walking",
                    ("Bitexco Tower", "Nguyen Hue Walking Street"): "5 minutes walking",
                    ("Ben Thanh Market", "Cho Lon"): "25 minutes by bus route 1 or 15 minutes by taxi",
                    ("War Remnants Museum", "Cu Chi Tunnels"): "1.5 hours by bus or 1 hour by taxi"
                }
            }
        }
        return city_data.get(city, {})

@tool
def get_travel_time(city: str, from_location: str, to_location: str) -> str:
    """
    Get the estimated travel time between two locations in a city using public transport.
    
    Args:
        city: Name of the city
        from_location: Starting location in the city
        to_location: Destination in the city
    """
    city_data = CityData.get_city_data(city)
    if not city_data:
        return f"Travel time information not available for {city}"
    
    travel_times = city_data.get("travel_times", {})
    
    # Try both directions since our dictionary only stores one direction
    try:
        return travel_times[(from_location, to_location)]
    except KeyError:
        try:
            return travel_times[(to_location, from_location)]
        except KeyError:
            return "20-30 minutes by public transport (estimated)"

@tool
def get_location_info(city: str, location: str) -> str:
    """
    Get information about a location in a specific city.
    
    Args:
        city: Name of the city
        location: Name of the location in the city
    """
    city_data = CityData.get_city_data(city)
    if not city_data:
        return f"Location information not available for {city}"
    
    locations = city_data.get("locations", {})
    return locations.get(location, f"Information not available for {location} in {city}")