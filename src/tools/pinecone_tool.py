"""Pinecone vector database search tool implementation."""

from typing import Dict, Any, List, Tuple
from langchain_core.documents import Document

from .base_tool import BaseTool


class PineconeSearchTool(BaseTool):
    """Tool for searching the Pinecone vector database."""
    
    def __init__(self):
        """Initialize Pinecone search tool."""
        self.retriever = None
        super().__init__()
    
    def _get_name(self) -> str:
        """Get the tool name."""
        return "pinecone_search"
    
    def _get_description(self) -> str:
        """Get the tool description."""
        return "Search the vector database for previously stored research papers and documents."
    
    def _check_availability(self) -> bool:
        """Check if Pinecone retriever is available."""
        try:
            from src.retrievers.pinecone import PineconeRetriever
            self.retriever = PineconeRetriever()
            return True
        except Exception as e:
            print(f"[PineconeSearchTool] Warning: Could not initialize Pinecone: {e}")
            return False
    
    def execute(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Execute Pinecone search and return results.
        
        Args:
            query: Search query for vector database
            max_results: Maximum number of results to return
            
        Returns:
            Dict containing search results and metadata
        """
        if not self.available:
            return {
                "success": False,
                "message": "Pinecone search not available",
                "results": [],
                "metadata": []
            }
        
        try:
            documents, metadata = self.retriever.retrieve(query, max_docs=max_results)
            
            if not documents:
                return {
                    "success": False,
                    "message": "No stored documents found",
                    "results": [],
                    "metadata": []
                }
            
            results = []
            for doc, meta in zip(documents, metadata):
                results.append({
                    "title": meta.get("title", "Unknown"),
                    "content": self._truncate_content(doc.page_content, 600),
                    "source": meta.get("source", "vector_db"),
                    "score": meta.get("score", 0.0)
                })
            
            return {
                "success": True,
                "message": f"Found {len(results)} stored documents",
                "results": results,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error during vector search: {str(e)}",
                "results": [],
                "metadata": []
            }
    
    def _truncate_content(self, content: str, max_length: int) -> str:
        """Truncate content to specified length."""
        if len(content) <= max_length:
            return content
        return content[:max_length] + "..."
