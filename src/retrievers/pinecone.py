"""Pinecone vector database retriever module."""
import os
from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import traceback

from .base import BaseRetriever


class PineconeRetriever(BaseRetriever):
    """Retriever for Pinecone vector database."""
    
    def __init__(self):
        """Initialize Pinecone vector store."""
        try:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
            
            if not openai_api_key:
                print("[PineconeRetriever] Warning: OPENAI_API_KEY not set")
                self.embeddings = None
                self.vectorstore = None
                return
            
            if not pinecone_index_name:
                print("[PineconeRetriever] Warning: PINECONE_INDEX_NAME not set")
                self.embeddings = None
                self.vectorstore = None
                return
            
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=openai_api_key
            )
            self.vectorstore = PineconeVectorStore(
                index_name=pinecone_index_name,
                embedding=self.embeddings
            )
        except Exception as e:
            print(f"[PineconeRetriever] Error initializing: {e}")
            self.vectorstore = None
    
    def name(self) -> str:
        return "Pinecone Vector DB"
    
    def retrieve(self, query: str, max_docs: int = 5) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """Retrieve documents from Pinecone vector database."""
        if not self.vectorstore:
            print("[PineconeRetriever] Vector store not initialized")
            return [], []
        
        print(f"[PineconeRetriever] Searching for: {query}")
        
        try:
            # Search with scores
            results_with_scores = self.vectorstore.similarity_search_with_score(query, k=max_docs)
            
            if not results_with_scores:
                print("[PineconeRetriever] No results found")
                return [], []
            
            # Filter by confidence threshold
            confidence_threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.8"))
            high_confidence_results = [
                (doc, score) for doc, score in results_with_scores 
                if score >= confidence_threshold
            ]
            
            if not high_confidence_results:
                print(f"[PineconeRetriever] All results below threshold {confidence_threshold}")
                return [], []
            
            documents = [doc for doc, _ in high_confidence_results]
            
            # Extract unique papers and metadata
            unique_papers = {}
            for doc, score in high_confidence_results:
                if 'title' in doc.metadata:
                    title = doc.metadata['title']
                    if title not in unique_papers:
                        unique_papers[title] = (doc.metadata, score)
            
            # Create metadata list
            paper_metadata = []
            for title, (metadata, score) in list(unique_papers.items())[:max_docs]:
                # Extract ArXiv ID
                arxiv_id = ""
                if 'source' in metadata and 'arxiv.org' in metadata.get('source', ''):
                    arxiv_id = metadata['source'].split('/')[-1].replace('.pdf', '')
                
                meta = {
                    'title': title,
                    'arxiv_id': arxiv_id,
                    'authors': metadata.get('authors', 'Unknown'),
                    'published': metadata.get('published', 'Unknown'),
                    'url': f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else metadata.get('source', ''),
                    'source': 'pinecone',
                    'confidence_score': score
                }
                paper_metadata.append(meta)
            
            print(f"[PineconeRetriever] Found {len(documents)} high-confidence results")
            return documents, paper_metadata
            
        except Exception as e:
            print(f"[PineconeRetriever] Error: {e}")
            traceback.print_exc()
            return [], []
