"""Base tool interface for all research tools."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):
    """Abstract base class for all research tools."""
    
    def __init__(self):
        """Initialize the tool."""
        self.name = self._get_name()
        self.description = self._get_description()
        self.available = self._check_availability()
    
    @abstractmethod
    def _get_name(self) -> str:
        """Get the tool name."""
        pass
    
    @abstractmethod
    def _get_description(self) -> str:
        """Get the tool description."""
        pass
    
    @abstractmethod
    def _check_availability(self) -> bool:
        """Check if the tool is available and properly configured."""
        pass
    
    @abstractmethod
    def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute the tool with the given query.
        
        Args:
            query: The search query or expression
            **kwargs: Additional parameters specific to each tool
            
        Returns:
            Dict with keys:
                - success: bool
                - message: str
                - results: list (for search tools)
                - result: any (for calculator)
                - metadata: list (optional)
        """
        pass
    
    def is_available(self) -> bool:
        """Check if the tool is available for use."""
        return self.available
