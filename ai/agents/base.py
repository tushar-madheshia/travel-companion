from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAIComponent(ABC):
    def __init__(self, name: str, config: Dict[str, Any] = {}):
        self.name = name
        self.config = config
        self.state = {}

    @abstractmethod
    def initialize(self) -> None:
        """Set up necessary internal state or configuration."""
        pass

    @abstractmethod
    def load(self) -> None:
        """
        Prepare the internal agent/graph/tools. Called once during init.
        """
        pass

    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's logic on the given input and return output.
        This abstracts sync/async processing and underlying models or graphs.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset the component to its initial state."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Gracefully shut down the component."""
        pass

    def info(self) -> Dict[str, Any]:
        """Return metadata or diagnostic information."""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "config": self.config,
            "state": self.state,
        }
