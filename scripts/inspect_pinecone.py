"""
Script to inspect the contents of Pinecone index.
Shows statistics and sample documents with their metadata.
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import sys

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not all([PINECONE_API_KEY, PINECONE_INDEX_NAME, OPENAI_API_KEY]):
    print("❌ Error: PINECONE_API_KEY, PINECONE_INDEX_NAME, and OPENAI_API_KEY must be set in .env file")
    sys.exit(1)

print(f"🔄 Connecting to Pinecone index: {PINECONE_INDEX_NAME}")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Get index stats
stats = index.describe_index_stats()
print(f"\n📊 Index Statistics:")
print(f"  Total vectors: {stats.get('total_vector_count', 0)}")
print(f"  Dimensions: {stats.get('dimension', 'Unknown')}")
print(f"  Index fullness: {stats.get('index_fullness', 0):.2%}")

# Initialize embeddings for similarity search
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)
vectorstore = PineconeVectorStore(index_name=PINECONE_INDEX_NAME, embedding=embeddings)

# Sample query to see what's in the database
print("\n🔍 Sampling documents from the index...")
try:
    # Do a simple search to get some documents
    sample_results = vectorstore.similarity_search_with_score(
        "research paper", 
        k=5,
        filter={}  # No filter to get any documents
    )
    
    if sample_results:
        print(f"\n📄 Found {len(sample_results)} sample documents:")
        print("-" * 80)
        
        # Track unique papers
        unique_papers = set()
        
        for i, (doc, score) in enumerate(sample_results, 1):
            print(f"\nDocument {i} (Score: {score:.3f}):")
            
            # Show metadata
            if doc.metadata:
                print("  Metadata:")
                for key, value in doc.metadata.items():
                    if key == 'summary':
                        print(f"    {key}: {value[:100]}..." if len(str(value)) > 100 else f"    {key}: {value}")
                    else:
                        print(f"    {key}: {value}")
                
                if 'title' in doc.metadata:
                    unique_papers.add(doc.metadata['title'])
            
            # Show content preview
            content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            print(f"  Content preview: {content_preview}")
            print("-" * 80)
        
        print(f"\n📚 Unique papers in sample: {len(unique_papers)}")
        for title in unique_papers:
            print(f"  • {title}")
    else:
        print("  No documents found in the index.")
        
except Exception as e:
    print(f"❌ Error sampling documents: {e}")

print("\n✅ Inspection complete!")
