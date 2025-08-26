import os
from langchain_community.document_loaders import ArxivLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import pinecone
from pinecone import ServerlessSpec

# Load environment variables from a .env file
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


# --- Configuration ---
# It's recommended to use environment variables for sensitive data and configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD")
PINECONE_REGION = os.getenv("PINECONE_REGION")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "my-personal-index")
# The Google library specifically looks for the GOOGLE_API_KEY environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI's text-embedding-3-small model produces 1536-dimensional vectors
EMBEDDING_DIMENSION = 1536

def populate_vector_database():
    """
    Fetches recent papers from arXiv, processes them, and stores their
    embeddings in a Pinecone vector database. Creates the index if it doesn't exist.
    """
    print("--- Starting Vector Database Population ---")
    
    # Initialize Pinecone client to manage indexes
    print("Initializing Pinecone client...")
    pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

    # Check if the index exists, create it if it doesn't
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        print(f"Index '{PINECONE_INDEX_NAME}' not found. Creating a new one...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",  # Cosine similarity is a good choice for text embeddings
            spec=ServerlessSpec(
                cloud=PINECONE_CLOUD,
                region=PINECONE_REGION
            )
        )
        print("Index created successfully.")
    else:
        print(f"Found existing index '{PINECONE_INDEX_NAME}'.")

    # 1. Fetch Documents from ArXiv
    # Using a broader query to ensure results are found
    print("Fetching recent papers from ArXiv...")
    loader = ArxivLoader(query="machine learning", load_max_docs=3) # Reduced for faster testing
    documents = loader.load()
    if not documents:
        print("No documents found on ArXiv for the query. Exiting.")
        return

    print(f"Loaded {len(documents)} documents from ArXiv.")

    # 2. Split Documents into Chunks
    print("Splitting documents into manageable chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")

    # 3. Initialize Embeddings
    # Initialize OpenAI embeddings
    print("Initializing OpenAI embeddings model...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_KEY
    )

    # 4. Create or Connect to Pinecone Index and Upload Chunks
    print(f"Connecting to Pinecone index for document upload...")
    # This will now use the existing or newly created index.
    PineconeVectorStore.from_documents(
        chunks, embeddings, index_name=PINECONE_INDEX_NAME
    )
    print("--- Vector Database Population Complete ---")
    print(f"Successfully uploaded {len(chunks)} chunks to Pinecone.")


if __name__ == "__main__":
    if not all([PINECONE_API_KEY, PINECONE_INDEX_NAME, GOOGLE_API_KEY, PINECONE_CLOUD, PINECONE_REGION]):
        print("FATAL: Missing required environment variables.")
        print("Please set PINECONE_API_KEY, PINECONE_CLOUD, PINECONE_REGION, PINECONE_INDEX_NAME, and GOOGLE_API_KEY in a .env file.")
    else:
        populate_vector_database()
