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
                    search_kwargs={"count": 20}  # Default count, will be overridden per search
                )
            except Exception as e:
                print(f"[BraveRetriever] Error initializing: {e}")
                self.search = None
    

    
    def name(self) -> str:
        return "Brave Search"
    
    def retrieve(self, query: str, max_docs: int = 10) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """Retrieve search results from Brave."""
        if not self.search:
            print("[BraveRetriever] Brave search not initialized")
            return [], []
        
        print(f"[BraveRetriever] Searching for: {query}")
        
        try:
            # Use the original query without academic modifications for general web search
            search_query = query
            
            # Update search_kwargs for this specific search
            original_kwargs = None
            if hasattr(self.search, 'search_kwargs'):
                original_kwargs = self.search.search_kwargs.copy()
                self.search.search_kwargs['count'] = max_docs
                print(f"[BraveRetriever] Set count to {max_docs}")
            
            results = self.search.run(search_query)
            
            # Restore original search_kwargs
            if original_kwargs and hasattr(self.search, 'search_kwargs'):
                self.search.search_kwargs = original_kwargs
            
            if not results:
                print("[BraveRetriever] No results found")
                return [], []
            
            # Debug: Print raw results info
            print(f"[BraveRetriever] Raw results length: {len(results)} chars")
            
            # Parse results - Brave API returns JSON-like structure
            documents = []
            paper_metadata = []
            
            import re
            import json
            
            # Try to parse as JSON first (Brave often returns JSON array)
            parsed_results = []
            try:
                # Check if it looks like JSON
                if results.strip().startswith('[') and results.strip().endswith(']'):
                    parsed_results = json.loads(results)
                    print(f"[BraveRetriever] Successfully parsed JSON with {len(parsed_results)} results")
                else:
                    # If not JSON, try to extract JSON objects from the text
                    json_pattern = r'\{"title":[^}]+\}'
                    json_matches = re.findall(json_pattern, results)
                    for match in json_matches:
                        try:
                            parsed_results.append(json.loads(match))
                        except:
                            continue
                    print(f"[BraveRetriever] Extracted {len(parsed_results)} JSON objects from text")
            except json.JSONDecodeError:
                print("[BraveRetriever] Results not in JSON format, using fallback parsing")
            
            # If JSON parsing worked, use structured data
            if parsed_results:
                for i, result in enumerate(parsed_results[:max_docs]):
                    title = result.get("title", f"Web Result {i+1}")
                    url = result.get("link", result.get("url", ""))
                    snippet = result.get("snippet", "")
                    
                    # Clean up URLs (remove quotes and other artifacts)
                    if url:
                        url = url.strip().strip('"').strip("'").strip(',')
                        # Remove any trailing artifacts
                        url = re.sub(r'["\',]+$', '', url)
                    
                    print(f"[BraveRetriever] Entry {i+1}: Title='{title[:50]}...', URL='{url}'")
                    
                    # Create document content
                    content = f"Title: {title}\nURL: {url}\nSnippet: {snippet}"
                    
                    # Create a document from the search result
                    doc = Document(
                        page_content=content,
                        metadata={
                            'source': 'brave_search',
                            'query': query,
                            'result_index': i,
                            'url': url
                        }
                    )
                    documents.append(doc)
                    
                    # Create metadata appropriate for web content
                    meta = {
                        'title': title[:150],
                        'url': url,
                        'source': 'brave_search',
                        'content_type': 'web',
                        'snippet': snippet[:200] + "..." if len(snippet) > 200 else snippet
                    }
                    paper_metadata.append(meta)
            
            else:
                # Fallback to text parsing if JSON parsing failed
                print("[BraveRetriever] Using fallback text parsing")
                
                # Try different splitting strategies
                entries = [entry.strip() for entry in results.split('\n\n') if entry.strip()]
                
                # If that doesn't work, try splitting by title patterns
                if len(entries) <= 1:
                    title_pattern = r'^\d+\.\s*(.+?)(?=\n|$)'
                    matches = re.finditer(title_pattern, results, re.MULTILINE)
                    entries = []
                    for match in matches:
                        start = match.start()
                        next_match = None
                        for next_m in re.finditer(title_pattern, results[start+1:], re.MULTILINE):
                            next_match = next_m
                            break
                        
                        if next_match:
                            end = start + 1 + next_match.start()
                            entries.append(results[start:end].strip())
                        else:
                            entries.append(results[start:].strip())
                
                print(f"[BraveRetriever] Parsed {len(entries)} entries from text")
                
                for i, entry in enumerate(entries[:max_docs]):
                    if not entry.strip():
                        continue
                    
                    # Extract title and URL from the result
                    lines = entry.split('\n')
                    
                    # Try to find a good title (first non-empty line)
                    title = None
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('http'):
                            title = re.sub(r'^\d+\.\s*', '', line)
                            break
                    
                    title = title or f"Web Result {i+1}"
                    
                    # Look for URLs in the content and clean them
                    url = ""
                    for line in lines:
                        url_match = re.search(r'https?://[^\s\'"]+', line)
                        if url_match:
                            url = url_match.group(0)
                            # Clean up URL
                            url = url.strip().strip('"').strip("'").strip(',')
                            url = re.sub(r'["\',]+$', '', url)
                            break
                    
                    print(f"[BraveRetriever] Entry {i+1}: Title='{title[:50]}...', URL='{url}'")
                    
                    # Create a document from the search result
                    doc = Document(
                        page_content=entry,
                        metadata={
                            'source': 'brave_search',
                            'query': query,
                            'result_index': i,
                            'url': url
                        }
                    )
                    documents.append(doc)
                    
                    # Create metadata appropriate for web content
                    meta = {
                        'title': title[:150],
                        'url': url,
                        'source': 'brave_search',
                        'content_type': 'web',
                        'snippet': entry[:200] + "..." if len(entry) > 200 else entry
                    }
                    paper_metadata.append(meta)
            
            print(f"[BraveRetriever] Found {len(documents)} results")
            return documents, paper_metadata
            
        except Exception as e:
            print(f"[BraveRetriever] Error: {e}")
            traceback.print_exc()
            return [], []
