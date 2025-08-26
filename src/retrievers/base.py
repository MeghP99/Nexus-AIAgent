"""Base retriever interface for all retrievers."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document


class BaseRetriever(ABC):
    """Abstract base class for all retrievers."""
    
    @abstractmethod
    def retrieve(self, query: str, max_docs: int = 5) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """
        Retrieve documents based on the query.
        
        Args:
            query: The search query
            max_docs: Maximum number of documents to retrieve
            
        Returns:
            Tuple of (documents, metadata) where metadata contains paper information
        """
        pass
    
    @abstractmethod
    def name(self) -> str:
        """Return the name of the retriever."""
        pass
