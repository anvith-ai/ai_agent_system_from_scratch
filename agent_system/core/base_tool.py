from abc import ABC, abstractmethod

class BaseTool(ABC):
    """Abstract base class for all tools in the agent system."""
    
    @abstractmethod
    def name(self) -> str:
        """Return the name of the tool."""
        pass
    
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the tool does."""
        pass
    
    @abstractmethod
    def use(self, *args, **kwargs):
        """Execute the tool's functionality."""
        pass