"""
Test script to examine ArXiv API responses and understand the data structure.
This helps us debug what information we're getting from papers.
"""

from langchain_community.document_loaders import ArxivLoader
import json
import os
from datetime import datetime

# Create data directory if it doesn't exist
DATA_DIR = "data/papers"
os.makedirs(DATA_DIR, exist_ok=True)

def save_paper(doc, index, query_name="test"):
    """Save paper content and metadata to files."""
    # Extract ArXiv ID for filename
    entry_id = doc.metadata.get('entry_id', '')
    arxiv_id = 'unknown'
    if 'arxiv.org' in entry_id:
        arxiv_id = entry_id.split('/abs/')[-1].split('v')[0]
    
    # Clean filename
    safe_query = query_name.replace(" ", "_").replace("/", "_")[:50]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{safe_query}_{index}_{arxiv_id}_{timestamp}"
    
    # Save metadata as JSON
    metadata_path = os.path.join(DATA_DIR, f"{base_filename}_metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        # Convert metadata to serializable format
        metadata_dict = dict(doc.metadata)
        metadata_dict['content_length'] = len(doc.page_content)
        metadata_dict['arxiv_url'] = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id != 'unknown' else None
        json.dump(metadata_dict, f, indent=2, ensure_ascii=False)
    
    # Save full content as text
    content_path = os.path.join(DATA_DIR, f"{base_filename}_content.txt")
    with open(content_path, 'w', encoding='utf-8') as f:
        f.write(f"Title: {doc.metadata.get('Title', 'Unknown')}\n")
        f.write(f"Authors: {doc.metadata.get('Authors', 'Unknown')}\n")
        f.write(f"Published: {doc.metadata.get('Published', 'Unknown')}\n")
        f.write(f"ArXiv ID: {arxiv_id}\n")
        f.write(f"ArXiv URL: https://arxiv.org/abs/{arxiv_id}\n")
        f.write("=" * 80 + "\n\n")
        f.write("ABSTRACT/SUMMARY:\n")
        f.write("-" * 40 + "\n")
        f.write(doc.metadata.get('Summary', 'No summary available') + "\n\n")
        f.write("=" * 80 + "\n\n")
        f.write("FULL CONTENT:\n")
        f.write("-" * 40 + "\n")
        f.write(doc.page_content)
    
    # Save a summary file
    summary_path = os.path.join(DATA_DIR, f"{base_filename}_summary.txt")
    with open(summary_path, 'w', encoding='utf-8') as f:
        content_lower = doc.page_content.lower()
        f.write(f"Paper Analysis Summary\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Title: {doc.metadata.get('Title', 'Unknown')}\n")
        f.write(f"ArXiv ID: {arxiv_id}\n")
        f.write(f"Content Length: {len(doc.page_content):,} characters\n\n")
        f.write("Content Sections Found:\n")
        f.write(f"  - Introduction: {'Yes' if 'introduction' in content_lower else 'No'}\n")
        f.write(f"  - Abstract: {'Yes' if 'abstract' in content_lower else 'No'}\n")
        f.write(f"  - Methodology: {'Yes' if 'method' in content_lower else 'No'}\n")
        f.write(f"  - Results: {'Yes' if 'results' in content_lower else 'No'}\n")
        f.write(f"  - Conclusion: {'Yes' if 'conclusion' in content_lower else 'No'}\n")
        f.write(f"  - References: {'Yes' if 'references' in content_lower else 'No'}\n")
        f.write(f"  - Appendix: {'Yes' if 'appendix' in content_lower else 'No'}\n\n")
        
        # Estimate if full paper
        has_multiple_sections = sum([
            'introduction' in content_lower,
            'method' in content_lower,
            'results' in content_lower or 'experiments' in content_lower,
            'conclusion' in content_lower,
            'references' in content_lower
        ]) >= 3
        
        f.write(f"Likely Full Paper: {'Yes' if has_multiple_sections else 'No (possibly abstract only)'}\n")
    
    print(f"  💾 Saved to:")
    print(f"     - {metadata_path}")
    print(f"     - {content_path}")
    print(f"     - {summary_path}")
    
    return metadata_path, content_path, summary_path

def test_arxiv_search(query="transformer architectures", max_docs=2):
    """Test ArXiv search and display the results."""
    print(f"🔍 Searching ArXiv for: '{query}'")
    print(f"   Max documents: {max_docs}")
    print("=" * 80)
    
    try:
        # Load documents from ArXiv
        loader = ArxivLoader(query=query, load_max_docs=max_docs)
        documents = loader.load()
        
        print(f"\n✅ Found {len(documents)} documents\n")
        
        # Examine each document
        for i, doc in enumerate(documents):
            print(f"📄 DOCUMENT {i+1}")
            print("-" * 40)
            
            # Display metadata
            print("METADATA:")
            metadata = doc.metadata
            for key, value in metadata.items():
                if key == 'Summary':
                    print(f"  {key}: {value[:200]}..." if len(str(value)) > 200 else f"  {key}: {value}")
                else:
                    print(f"  {key}: {value}")
            
            # Check for ArXiv ID in different places
            print("\nARXIV ID EXTRACTION:")
            entry_id = metadata.get('entry_id', '')
            print(f"  entry_id: {entry_id}")
            if 'arxiv.org' in entry_id:
                arxiv_id = entry_id.split('/abs/')[-1].split('v')[0]
                print(f"  Extracted ID: {arxiv_id}")
                print(f"  ArXiv URL: https://arxiv.org/abs/{arxiv_id}")
            
            # Display content length and preview
            print(f"\nCONTENT:")
            print(f"  Total length: {len(doc.page_content)} characters")
            print(f"  Preview (first 500 chars):")
            print(f"  {doc.page_content[:500]}...")
            
            # Check if we're getting full paper or just abstract
            print(f"\nCONTENT ANALYSIS:")
            content_lower = doc.page_content.lower()
            has_introduction = "introduction" in content_lower
            has_conclusion = "conclusion" in content_lower
            has_references = "references" in content_lower
            
            print(f"  Has Introduction section: {has_introduction}")
            print(f"  Has Conclusion section: {has_conclusion}")
            print(f"  Has References section: {has_references}")
            
            if has_introduction and has_conclusion:
                print("  ✅ Appears to be FULL PAPER")
            else:
                print("  ⚠️ Might be ABSTRACT ONLY")
            
            # Save the paper
            print("\nSAVING PAPER:")
            save_paper(doc, i+1, query)
            
            print("\n" + "=" * 80 + "\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_specific_paper(arxiv_id="2212.10554"):
    """Test loading a specific paper by ArXiv ID."""
    print(f"\n📎 Testing specific paper: {arxiv_id}")
    print("=" * 80)
    
    try:
        # ArxivLoader can also load by ID
        loader = ArxivLoader(query=arxiv_id, load_max_docs=1, load_all_available_meta=True)
        documents = loader.load()
        
        if documents:
            doc = documents[0]
            print(f"✅ Successfully loaded paper")
            print(f"Title: {doc.metadata.get('Title', 'Unknown')}")
            print(f"Authors: {doc.metadata.get('Authors', 'Unknown')}")
            print(f"Content length: {len(doc.page_content)} characters")
            
            # Save the paper
            print("\nSAVING PAPER:")
            save_paper(doc, 1, f"specific_{arxiv_id}")
        else:
            print("❌ No document found")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print(f"📁 Papers will be saved to: {os.path.abspath(DATA_DIR)}\n")
    
    # Test 1: Search for papers
    print("TEST 1: SEARCH FOR PAPERS")
    print("=" * 80)
    test_arxiv_search("machine learning transformers in 2025", max_docs=2)
    
    # Test 2: Load specific paper
    print("\n\nTEST 2: LOAD SPECIFIC PAPER")
    print("=" * 80)
    test_specific_paper("2212.10554")  # Example: A well-known transformer paper
    
    # Test 3: Different query
    print("\n\nTEST 3: DIFFERENT QUERY")
    print("=" * 80)
    test_arxiv_search("BERT language model", max_docs=1)
    
    # Summary
    print("\n\n📊 SUMMARY")
    print("=" * 80)
    print(f"All papers have been saved to: {os.path.abspath(DATA_DIR)}")
    print("\nFiles saved per paper:")
    print("  - *_metadata.json : Full metadata in JSON format")
    print("  - *_content.txt   : Full paper content as text")
    print("  - *_summary.txt   : Analysis summary (sections found, full paper check)")
    print("\n✅ Check the files to see what ArXiv actually returns!")
