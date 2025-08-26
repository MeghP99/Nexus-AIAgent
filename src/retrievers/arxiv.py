"""Arxiv API retriever module."""
from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document
from langchain_community.document_loaders import ArxivLoader
import traceback

from .base import BaseRetriever


class ArxivRetriever(BaseRetriever):
    """Retriever for ArXiv papers."""
    
    def name(self) -> str:
        return "ArXiv"
    
    def retrieve(self, query: str, max_docs: int = 5) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """Retrieve papers from ArXiv API."""
        print(f"[ArxivRetriever] Searching for: {query}")
        
        try:
            loader = ArxivLoader(query=query, load_max_docs=max_docs)
            documents = loader.load()
            
            if not documents:
                print("[ArxivRetriever] No documents found")
                return [], []
            
            # Deduplicate papers by title
            unique_documents = []
            seen_titles = set()
            
            for doc in documents:
                title = doc.metadata.get('Title', '')
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    unique_documents.append(doc)
                elif not title:
                    # If no title, check content similarity
                    is_duplicate = False
                    for existing_doc in unique_documents:
                        if doc.page_content[:200] == existing_doc.page_content[:200]:
                            is_duplicate = True
                            break
                    if not is_duplicate:
                        unique_documents.append(doc)
            
            documents = unique_documents
            print(f"[ArxivRetriever] Found {len(documents)} unique documents")
            
            # Extract metadata
            paper_metadata = []
            for doc in documents:
                # Extract ArXiv ID from entry_id
                entry_id = doc.metadata.get('entry_id', '')
                arxiv_id = ''
                if 'arxiv.org' in entry_id:
                    arxiv_id = entry_id.split('/abs/')[-1].split('v')[0]
                elif entry_id:
                    arxiv_id = entry_id.split('/')[-1]
                
                meta = {
                    'title': doc.metadata.get('Title', 'Unknown'),
                    'arxiv_id': arxiv_id,
                    'authors': doc.metadata.get('Authors', 'Unknown'),
                    'published': doc.metadata.get('Published', 'Unknown'),
                    'url': f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else "",
                    'source': 'arxiv'
                }
                paper_metadata.append(meta)
            
            return documents, paper_metadata
            
        except AttributeError as e:
            if "fitz" in str(e) and "FileDataError" in str(e):
                print(f"[ArxivRetriever] PyMuPDF version compatibility issue: {e}")
                print("[ArxivRetriever] Please install PyMuPDF==1.23.28 to fix this issue")
                print("[ArxivRetriever] Run: pip install PyMuPDF==1.23.28")
                return [], []
            else:
                print(f"[ArxivRetriever] AttributeError: {e}")
                traceback.print_exc()
                return [], []
        except Exception as e:
            print(f"[ArxivRetriever] Error: {e}")
            traceback.print_exc()
            return [], []
