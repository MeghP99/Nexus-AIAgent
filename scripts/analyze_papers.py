"""
Analyze papers saved in the data/papers directory.
This helps understand what content ArXiv provides.
"""

import os
import json
import glob

DATA_DIR = "data/papers"

def analyze_saved_papers():
    """Analyze all saved papers and provide statistics."""
    print("📊 ANALYZING SAVED PAPERS")
    print("=" * 80)
    
    # Find all metadata files
    metadata_files = glob.glob(os.path.join(DATA_DIR, "*_metadata.json"))
    
    if not metadata_files:
        print("❌ No papers found in data/papers/")
        print("   Run 'python scripts/test_arxiv.py' first to download papers.")
        return
    
    print(f"Found {len(metadata_files)} papers\n")
    
    total_chars = 0
    full_papers = 0
    abstracts_only = 0
    
    for i, metadata_file in enumerate(metadata_files, 1):
        print(f"📄 Paper {i}:")
        print("-" * 40)
        
        # Load metadata
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Get corresponding files
        base_name = metadata_file.replace("_metadata.json", "")
        content_file = f"{base_name}_content.txt"
        summary_file = f"{base_name}_summary.txt"
        
        print(f"Title: {metadata.get('Title', 'Unknown')[:80]}...")
        print(f"Authors: {metadata.get('Authors', 'Unknown')[:80]}...")
        print(f"Published: {metadata.get('Published', 'Unknown')}")
        print(f"ArXiv URL: {metadata.get('arxiv_url', 'Unknown')}")
        
        # Check content length
        content_length = metadata.get('content_length', 0)
        total_chars += content_length
        print(f"Content Length: {content_length:,} characters")
        
        # Check if full paper
        if os.path.exists(summary_file):
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary_content = f.read()
                if "Likely Full Paper: Yes" in summary_content:
                    print("Status: ✅ FULL PAPER")
                    full_papers += 1
                else:
                    print("Status: ⚠️ ABSTRACT ONLY")
                    abstracts_only += 1
        
        print()
    
    # Overall statistics
    print("\n📈 OVERALL STATISTICS")
    print("=" * 80)
    print(f"Total papers analyzed: {len(metadata_files)}")
    print(f"Full papers: {full_papers}")
    print(f"Abstracts only: {abstracts_only}")
    print(f"Average content length: {total_chars // len(metadata_files):,} characters")
    print(f"Total content: {total_chars:,} characters")
    
    print("\n💡 INSIGHTS:")
    if full_papers > 0:
        print("✅ ArXiv API is returning FULL PAPERS (not just abstracts)")
        print("   This is good for comprehensive RAG applications!")
    else:
        print("⚠️ ArXiv API might be returning only abstracts")
        print("   Consider adjusting the loader parameters or using different sources")
    
    print(f"\n📁 All files saved in: {os.path.abspath(DATA_DIR)}")

if __name__ == "__main__":
    analyze_saved_papers()
