"""Tool management and execution for the research agent."""

from typing import Dict, List, Any, Optional
import logging

from src.tools import (
    BaseTool,
    ArxivSearchTool,
    BraveSearchTool,
    CalculatorTool,
    PineconeSearchTool
)


class ToolManager:
    """Manages tool initialization, availability, and execution."""
    
    def __init__(self):
        """Initialize the tool manager."""
        self.tools: Dict[str, BaseTool] = {}
        self.logger = logging.getLogger(__name__)
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize all available tools."""
        tool_classes = [
            ArxivSearchTool,
            BraveSearchTool,
            CalculatorTool,
            PineconeSearchTool
        ]
        
        for tool_class in tool_classes:
            try:
                tool = tool_class()
                if tool.is_available():
                    self.tools[tool.name] = tool
                    self.logger.info(f"✅ Initialized tool: {tool.name}")
                else:
                    self.logger.warning(f"⚠️ Tool not available: {tool.name}")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize {tool_class.__name__}: {e}")
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return list(self.tools.keys())
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """Get descriptions of all available tools."""
        return {name: tool.description for name, tool in self.tools.items()}
    
    def execute_tool(self, tool_name: str, query: str, **kwargs) -> Dict[str, Any]:
        """Execute a specific tool with the given input.
        
        Args:
            tool_name: Name of the tool to execute
            query: Query or expression to execute
            **kwargs: Additional parameters for the tool
            
        Returns:
            Dict containing tool execution results
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "message": f"Tool '{tool_name}' not available. Available tools: {list(self.tools.keys())}",
                "tool_name": tool_name
            }
        
        tool = self.tools[tool_name]
        
        try:
            # Execute tool with appropriate parameters
            if tool_name == "calculator":
                result = tool.execute(query)
            else:
                max_results = kwargs.get("max_results", 5)
                result = tool.execute(query, max_results=max_results)
            
            result["tool_name"] = tool_name
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing {tool_name}: {e}")
            return {
                "success": False,
                "message": f"Error executing {tool_name}: {str(e)}",
                "tool_name": tool_name
            }
    
    def is_tool_available(self, tool_name: str) -> bool:
        """Check if a specific tool is available.
        
        Args:
            tool_name: Name of the tool to check
            
        Returns:
            True if tool is available, False otherwise
        """
        return tool_name in self.tools
    
    def get_tool_count(self) -> int:
        """Get the number of available tools."""
        return len(self.tools)
