"""Test script for Brave API functionality."""
import os
import sys
from dotenv import load_dotenv

# Using absolute imports from src directory

load_dotenv()

def test_brave_api():
    """Test Brave API functionality with different queries."""
    # Import directly from the module to avoid __init__.py dependencies
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'retrievers'))
    from brave import BraveRetriever
    
    print("=== BRAVE API TEST ===")
    print(f"BRAVE_API_KEY: {'Set' if os.getenv('BRAVE_API_KEY') else 'Not set'}")
    print("=" * 50)
    
    # Initialize Brave retriever
    brave_retriever = BraveRetriever()
    
    if not brave_retriever.search:
        print("❌ Brave API not initialized. Please check your BRAVE_API_KEY.")
        return False
    
    # Test queries
    test_queries = [
        "machine learning transformers attention mechanism",
        "quantum computing algorithms",
        "climate change carbon capture technology",
        "artificial intelligence ethics"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: Searching for '{query}'")
        print("-" * 60)
        
        try:
            documents, paper_metadata = brave_retriever.retrieve(query, max_docs=3)
            
            if documents:
                print(f"✅ Found {len(documents)} results")
                
                for j, (doc, meta) in enumerate(zip(documents, paper_metadata)):
                    print(f"\nResult {j+1}:")
                    print(f"  Title: {meta['title']}")
                    print(f"  URL: {meta['url']}")
                    print(f"  Source: {meta['source']}")
                    print(f"  Content preview: {doc.page_content[:200]}...")
                    print(f"  Metadata: {doc.metadata}")
            else:
                print("❌ No results found")
                
        except Exception as e:
            print(f"❌ Error during search: {e}")
            return False
    
    print("\n" + "=" * 50)
    print("✅ Brave API test completed successfully!")
    return True

def test_brave_with_specific_queries():
    """Test Brave API with specific research-focused queries."""
    # Import directly from the module to avoid __init__.py dependencies
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'retrievers'))
    from brave import BraveRetriever
    
    print("\n=== BRAVE API RESEARCH-FOCUSED TEST ===")
    
    brave_retriever = BraveRetriever()
    
    if not brave_retriever.search:
        print("❌ Brave API not initialized.")
        return False
    
    research_queries = [
        "arxiv machine learning neural networks",
        "scientific paper deep learning transformers",
        "research study computer vision",
        "academic paper natural language processing"
    ]
    
    for query in research_queries:
        print(f"\n🔬 Research Query: '{query}'")
        print("-" * 60)
        
        try:
            documents, paper_metadata = brave_retriever.retrieve(query, max_docs=2)
            
            if documents:
                print(f"✅ Found {len(documents)} research-related results")
                
                for j, meta in enumerate(paper_metadata):
                    print(f"\nPaper {j+1}:")
                    print(f"  Title: {meta['title']}")
                    print(f"  URL: {meta['url']}")
                    print(f"  ArXiv ID: {meta['arxiv_id']}")
                    print(f"  Authors: {meta['authors']}")
                    
                    # Check if it's actually research-related
                    content = documents[j].page_content.lower()
                    research_indicators = ['arxiv', 'paper', 'research', 'study', 'academic', 'journal']
                    found_indicators = [indicator for indicator in research_indicators if indicator in content]
                    print(f"  Research indicators found: {found_indicators}")
            else:
                print("❌ No research results found")
                
        except Exception as e:
            print(f"❌ Error during research search: {e}")
    
    return True

if __name__ == "__main__":
    print("Starting Brave API tests...\n")
    
    # Basic functionality test
    basic_test_passed = test_brave_api()
    
    if basic_test_passed:
        # Research-focused test
        test_brave_with_specific_queries()
    
    print("\n🎉 All tests completed!")
