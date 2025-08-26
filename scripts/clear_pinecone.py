"""
Script to clear all vectors from Pinecone index.
This allows testing the ArXiv API search functionality.
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone
import sys

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

if not PINECONE_API_KEY or not PINECONE_INDEX_NAME:
    print("❌ Error: PINECONE_API_KEY and PINECONE_INDEX_NAME must be set in .env file")
    sys.exit(1)

print(f"🔄 Connecting to Pinecone index: {PINECONE_INDEX_NAME}")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Get index stats
stats = index.describe_index_stats()
print(f"📊 Current index stats: {stats}")

# Clear all vectors
print("🗑️ Clearing all vectors from index...")
try:
    index.delete(delete_all=True)
    print("✅ Successfully cleared all vectors from Pinecone index!")
    
    # Verify deletion
    stats_after = index.describe_index_stats()
    print(f"📊 Index stats after clearing: {stats_after}")
except Exception as e:
    print(f"❌ Error clearing index: {e}")
