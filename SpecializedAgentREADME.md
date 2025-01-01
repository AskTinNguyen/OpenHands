# SmolaGents Demo Implementation

This repository demonstrates the implementation of SmolaGents, a framework for building AI agents.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
- Create a `.env` file
- Add your Hugging Face API key:
```
HF_API_KEY=your_hugging_face_api_key_here
```

## Examples

### Basic Example (main.py)
Demonstrates a simple CodeAgent that can create a Flask application.

```bash
python main.py
```

### Advanced Example (advanced_example.py)
Shows how to:
- Create custom tools
- Use planning capabilities
- Handle multi-step tasks
- Save outputs to files

```bash
python advanced_example.py
```

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .env
├── main.py
└── advanced_example.py
```

## Custom Tools

The advanced example includes two custom tools:
1. `fetch_weather`: Simulates fetching weather data
2. `save_to_file`: Saves content to a file

## Key Features Demonstrated

1. Agent Initialization
2. Custom Tool Creation
3. Environment Configuration
4. Planning Capabilities
5. Multi-step Task Execution

## Notes

- The weather API implementation is a dummy example
- Make sure to replace the Hugging Face API key with your own
- The planning_interval parameter helps the agent break down complex tasks