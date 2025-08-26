"""
Script to recreate Pinecone index with new dimensions for OpenAI embeddings.
This is needed when switching from Gemini (768 dims) to OpenAI (1536 dims).
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import sys
import time

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")

# OpenAI embeddings dimension
NEW_DIMENSION = 1536

if not PINECONE_API_KEY or not PINECONE_INDEX_NAME:
    print("❌ Error: PINECONE_API_KEY and PINECONE_INDEX_NAME must be set in .env file")
    sys.exit(1)

print(f"🔄 Recreating Pinecone index '{PINECONE_INDEX_NAME}' with new dimensions...")
print(f"   Old dimension: 768 (Gemini)")
print(f"   New dimension: {NEW_DIMENSION} (OpenAI)")
print("=" * 80)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Step 1: Check if index exists and delete it
try:
    existing_indexes = pc.list_indexes()
    index_names = [idx.name for idx in existing_indexes]
    
    if PINECONE_INDEX_NAME in index_names:
        print(f"📍 Found existing index '{PINECONE_INDEX_NAME}'")
        
        # Get current stats before deletion
        try:
            index = pc.Index(PINECONE_INDEX_NAME)
            stats = index.describe_index_stats()
            print(f"   Current vectors: {stats.get('total_vector_count', 0)}")
            print(f"   Current dimension: {stats.get('dimension', 'Unknown')}")
        except:
            pass
        
        # Delete the index
        print(f"🗑️  Deleting old index...")
        pc.delete_index(PINECONE_INDEX_NAME)
        print("✅ Old index deleted successfully")
        
        # Wait a bit for deletion to complete
        print("⏳ Waiting for deletion to complete...")
        time.sleep(5)
    else:
        print(f"ℹ️  Index '{PINECONE_INDEX_NAME}' does not exist")
        
except Exception as e:
    print(f"⚠️  Error checking/deleting index: {e}")
    print("   You may need to delete it manually from Pinecone console")

# Step 2: Create new index with updated dimensions
print(f"\n📦 Creating new index with {NEW_DIMENSION} dimensions...")
try:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=NEW_DIMENSION,
        metric='cosine',
        spec=ServerlessSpec(
            cloud=PINECONE_CLOUD,
            region=PINECONE_REGION
        )
    )
    print("✅ New index created successfully!")
    
    # Wait for index to be ready
    print("⏳ Waiting for index to be ready...")
    time.sleep(10)
    
    # Verify the new index
    index = pc.Index(PINECONE_INDEX_NAME)
    stats = index.describe_index_stats()
    print(f"\n📊 New index stats:")
    print(f"   Dimension: {stats.get('dimension', 'Unknown')}")
    print(f"   Total vectors: {stats.get('total_vector_count', 0)}")
    
    print("\n✅ Success! Your Pinecone index has been recreated with OpenAI embedding dimensions.")
    print("\n🎯 Next steps:")
    print("   1. Run 'python scripts/populate_db.py' to add papers to the new index")
    print("   2. Run 'streamlit run app.py' to use the chatbot")
    
except Exception as e:
    print(f"❌ Error creating new index: {e}")
    print("\nPossible solutions:")
    print("1. Check your Pinecone console to manually delete the old index")
    print("2. Verify your PINECONE_CLOUD and PINECONE_REGION settings")
    print("3. Make sure you have permissions to create indexes")
