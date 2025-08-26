"""ArXiv search tool implementation."""

from typing import Dict, Any, List, Tuple
from langchain_core.documents import Document

from .base_tool import BaseTool


class ArxivSearchTool(BaseTool):
    """Tool for searching ArXiv academic papers."""
    
    def __init__(self):
        """Initialize ArXiv search tool."""
        self.retriever = None
        super().__init__()
    
    def _get_name(self) -> str:
        """Get the tool name."""
        return "arxiv_search"
    
    def _get_description(self) -> str:
        """Get the tool description."""
        return "Search ArXiv for academic papers and research on AI, ML, physics, math, and other scientific domains."
    
    def _check_availability(self) -> bool:
        """Check if ArXiv retriever is available."""
        try:
            from src.retrievers.arxiv import ArxivRetriever
            self.retriever = ArxivRetriever()
            return True
        except Exception as e:
            print(f"[ArxivSearchTool] Warning: Could not initialize ArXiv retriever: {e}")
            return False
    
    def execute(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Execute ArXiv search and return results.
        
        Args:
            query: Search query for ArXiv papers
            max_results: Maximum number of results to return
            
        Returns:
            Dict containing search results and metadata
        """
        if not self.available:
            return {
                "success": False,
                "message": "ArXiv search not available",
                "results": [],
                "metadata": []
            }
        
        try:
            documents, metadata = self.retriever.retrieve(query, max_docs=max_results)
            
            if not documents:
                return {
                    "success": False,
                    "message": "No ArXiv papers found",
                    "results": [],
                    "metadata": []
                }
            
            results = []
            for doc, meta in zip(documents, metadata):
                results.append({
                    "title": meta["title"],
                    "authors": meta["authors"],
                    "url": meta["url"],
                    "published": meta["published"],
                    "content": self._truncate_content(doc.page_content, 800),
                    "source": meta["source"]
                })
            
            return {
                "success": True,
                "message": f"Found {len(results)} ArXiv papers",
                "results": results,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error during ArXiv search: {str(e)}",
                "results": [],
                "metadata": []
            }
    
    def _truncate_content(self, content: str, max_length: int) -> str:
        """Truncate content to specified length."""
        if len(content) <= max_length:
            return content
        return content[:max_length] + "..."
