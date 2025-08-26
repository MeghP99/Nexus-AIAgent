"""Brave search retriever module."""
from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document
from langchain_community.utilities import BraveSearchWrapper
import os
import traceback

try:
    from .base import BaseRetriever
except ImportError:
    # Handle direct import case
    from base import BaseRetriever


class BraveRetriever(BaseRetriever):
    """Retriever for Brave search results."""
    
    def __init__(self):
        """Initialize Brave search wrapper."""
        # Check for Brave API key
        self.api_key = os.getenv("BRAVE_API_KEY")
        if not self.api_key:
            print("[BraveRetriever] Warning: BRAVE_API_KEY not set in environment")
            self.search = None
        else:
            try:
                # Initialize with search_kwargs to control result count
                self.search = BraveSearchWrapper(
                    api_key=self.api_key,
                    search_kwargs={"count": 10}  # Default count, will be overridden per search
                )
            except Exception as e:
                print(f"[BraveRetriever] Error initializing: {e}")
                self.search = None
    
    def name(self) -> str:
        return "Brave Search"
    
    def retrieve(self, query: str, max_docs: int = 5) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """Retrieve search results from Brave."""
        if not self.search:
            print("[BraveRetriever] Brave search not initialized")
            return [], []
        
        print(f"[BraveRetriever] Searching for: {query}")
        
        try:
            # Add arxiv or research paper keywords to improve results
            enhanced_query = f"{query} arxiv research paper scientific study"
            
            # Update search_kwargs for this specific search
            if hasattr(self.search, 'search_kwargs'):
                original_kwargs = self.search.search_kwargs.copy()
                self.search.search_kwargs['count'] = max_docs
            
            results = self.search.run(enhanced_query)
            
            # Restore original search_kwargs
            if hasattr(self.search, 'search_kwargs'):
                self.search.search_kwargs = original_kwargs
            
            if not results:
                print("[BraveRetriever] No results found")
                return [], []
            
            # Parse results - Brave returns a string of results
            documents = []
            paper_metadata = []
            
            # Split results into individual entries
            entries = results.split('\n\n')
            
            for i, entry in enumerate(entries[:max_docs]):
                if not entry.strip():
                    continue
                
                # Create a document from the search result
                doc = Document(
                    page_content=entry,
                    metadata={
                        'source': 'brave_search',
                        'query': query,
                        'result_index': i
                    }
                )
                documents.append(doc)
                
                # Try to extract title and URL from the result
                lines = entry.split('\n')
                title = lines[0] if lines else f"Search Result {i+1}"
                
                # Look for arxiv URLs in the content
                url = ""
                for line in lines:
                    if 'arxiv.org' in line.lower():
                        # Try to extract the URL
                        import re
                        url_match = re.search(r'https?://[^\s]+arxiv[^\s]+', line)
                        if url_match:
                            url = url_match.group(0)
                            break
                
                meta = {
                    'title': title[:100],  # Limit title length
                    'url': url,
                    'source': 'brave_search',
                    'arxiv_id': '',  # Brave results might not have arxiv IDs
                    'authors': 'Unknown',
                    'published': 'Unknown'
                }
                paper_metadata.append(meta)
            
            print(f"[BraveRetriever] Found {len(documents)} results")
            return documents, paper_metadata
            
        except Exception as e:
            print(f"[BraveRetriever] Error: {e}")
            traceback.print_exc()
            return [], []
