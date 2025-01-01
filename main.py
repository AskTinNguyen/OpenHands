from smolagents import CodeAgent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def main():
    # Initialize the agent with OpenAI's model
    agent = CodeAgent(
        tools=[],  # We'll start with no custom tools
        model="gpt-3.5-turbo",  # Using OpenAI's model
        add_base_tools=True  # This adds basic Python execution capabilities
    )
    
    # Example task for the agent
    result = agent.run(
        "Create a simple Flask application that displays 'Hello, World!' on the homepage"
    )
    
    print("Agent execution completed!")
    print("Result:", result)

if __name__ == "__main__":
    main()