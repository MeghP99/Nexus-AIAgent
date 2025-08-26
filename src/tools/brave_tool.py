"""Brave search tool implementation."""

from typing import Dict, Any, List, Tuple
from langchain_core.documents import Document

from .base_tool import BaseTool


class BraveSearchTool(BaseTool):
    """Tool for searching the web using Brave Search."""
    
    def __init__(self):
        """Initialize Brave search tool."""
        self.retriever = None
        super().__init__()
    
    def _get_name(self) -> str:
        """Get the tool name."""
        return "brave_search"
    
    def _get_description(self) -> str:
        """Get the tool description."""
        return "Search the web for current information, news, and general knowledge using Brave Search engine."
    
    def _check_availability(self) -> bool:
        """Check if Brave retriever is available."""
        try:
            from src.retrievers.brave import BraveRetriever
            self.retriever = BraveRetriever()
            return self.retriever.search is not None
        except Exception as e:
            print(f"[BraveSearchTool] Warning: Could not initialize Brave retriever: {e}")
            return False
    
    def execute(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Execute Brave search and return results.
        
        Args:
            query: Search query for web search
            max_results: Maximum number of results to return
            
        Returns:
            Dict containing search results and metadata
        """
        if not self.available:
            return {
                "success": False,
                "message": "Brave search not available",
                "results": [],
                "metadata": []
            }
        
        try:
            documents, metadata = self.retriever.retrieve(query, max_docs=max_results)
            
            if not documents:
                return {
                    "success": False,
                    "message": "No web results found",
                    "results": [],
                    "metadata": []
                }
            
            results = []
            for doc, meta in zip(documents, metadata):
                results.append({
                    "title": meta["title"],
                    "url": meta["url"],
                    "content": self._truncate_content(doc.page_content, 500),
                    "source": meta["source"]
                })
            
            return {
                "success": True,
                "message": f"Found {len(results)} web results",
                "results": results,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error during web search: {str(e)}",
                "results": [],
                "metadata": []
            }
    
    def _truncate_content(self, content: str, max_length: int) -> str:
        """Truncate content to specified length."""
        if len(content) <= max_length:
            return content
        return content[:max_length] + "..."
