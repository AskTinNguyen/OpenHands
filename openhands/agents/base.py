from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseAgent(ABC):
    """Base class for all OpenHands agents."""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the agent with configuration."""
        pass
    
    @abstractmethod
    def process_request(self, request: str) -> Dict[str, Any]:
        """Process a user request and return a response."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return a list of agent capabilities."""
        pass