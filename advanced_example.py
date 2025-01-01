from smolagents import CodeAgent, HfApiModel, tool
from dotenv import load_dotenv
import os
import requests

# Custom tool example
@tool
def fetch_weather(city: str) -> str:
    """
    Fetch weather information for a given city.
    
    Args:
        city: Name of the city to get weather for
    """
    # This is a dummy implementation
    return f"Weather information for {city}: Sunny, 22°C"

@tool
def save_to_file(content: str, filename: str) -> str:
    """
    Save content to a file.
    
    Args:
        content: The content to save
        filename: Name of the file to save to
    """
    with open(filename, 'w') as f:
        f.write(content)
    return f"Content saved to {filename}"

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize the agent with custom tools
    agent = CodeAgent(
        tools=[fetch_weather, save_to_file],
        model=HfApiModel(
            model_id="Qwen/Qwen2.5-72B-Instruct",
            api_key=os.getenv("HF_API_KEY")
        ),
        add_base_tools=True,
        planning_interval=3  # Enable planning every 3 steps
    )
    
    # Example task using custom tools
    result = agent.run("""
    1. Fetch the weather for London
    2. Create a Python script that prints this weather information
    3. Save this script to weather_report.py
    """)
    
    print("Agent execution completed!")
    print("Result:", result)

if __name__ == "__main__":
    main()