# ArXiv RAG Chatbot

An intelligent Retrieval-Augmented Generation (RAG) chatbot that answers questions about research papers from ArXiv with self-reflection capabilities and real-time progress tracking.

## Features

- 🔍 **Smart Search**: Searches Pinecone vector database first, falls back to ArXiv API and Brave Search
- 🌐 **Multi-Source Retrieval**: Combines ArXiv papers with Brave web search for comprehensive results
- 📄 **Efficient Processing**: Extracts only Abstract, Introduction, and Conclusion sections to reduce token usage
- 🤔 **Self-Reflection**: Uses LLM to evaluate if retrieved information is sufficient before responding
- 🔄 **Iterative Retrieval**: Automatically searches for more papers if initial results aren't comprehensive
- 📊 **Real-time Progress**: Beautiful step-by-step display of the search and synthesis process
- 📚 **Enhanced Indexing**: Stores papers with rich metadata for better retrieval
- 🎯 **High Confidence Threshold**: Avoids false positives with configurable confidence scoring
- 🧩 **Modular Architecture**: Clean separation of retrievers for easy extension and maintenance

## Architecture

The system uses LangGraph to orchestrate a multi-step pipeline:

1. **Vector Database Search**: Queries Pinecone for relevant papers
2. **Relevancy Check**: Uses Gemini to evaluate if information is sufficient
3. **External Source Retrieval**: Searches both ArXiv API and Brave Search (5 papers from each source)
4. **Section Extraction**: Extracts only Abstract, Introduction, and Conclusion from papers
5. **Reflection Loop**: Can iterate up to 3 times to gather comprehensive information
6. **Response Synthesis**: Uses Gemini to create well-structured answers from extracted sections

## Prerequisites

- Python 3.8+
- Google Cloud account with Gemini API access
- OpenAI account for embeddings
- Pinecone account and API key
- `.env` file with the following:

```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name
GEMINI_MODEL=gemini-1.5-flash  # Optional, this is the default
BRAVE_API_KEY=your_brave_api_key  # Optional, for enhanced web search
```

## Installation

1. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Running the Chatbot

```bash
streamlit run app.py
```

The app will open in your browser where you can:
- Ask questions about machine learning, AI, or any research topic
- Watch the real-time progress as it searches and synthesizes information
- See exactly which papers were used to answer your question

### Utility Scripts

#### Clear Pinecone Database
```bash
python scripts/clear_pinecone.py
```
Use this to clear all vectors and force the system to search ArXiv fresh.

#### Inspect Pinecone Contents
```bash
python scripts/inspect_pinecone.py
```
Shows statistics and sample documents stored in your vector database.

#### Pre-populate Database
```bash
python scripts/populate_db.py
```
Fetches papers from ArXiv and indexes them in Pinecone (optional).

## File Structure

```
.
├── app.py                    # Streamlit UI with real-time progress display
├── src/
│   ├── config.py            # Configuration and environment variables
│   ├── graph/
│   │   ├── builder.py       # LangGraph workflow definition
│   │   ├── nodes.py         # Core logic for each step
│   │   └── state.py         # State management for the pipeline
├── scripts/
│   ├── populate_db.py       # Pre-populate vector database
│   ├── clear_pinecone.py    # Clear all vectors from Pinecone
│   └── inspect_pinecone.py  # Inspect database contents
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Key Improvements

### Enhanced Vector Storage
- Chunks papers with 1500 character chunks (200 char overlap)
- Stores rich metadata: title, authors, publication date, summary
- Tracks which query retrieved each paper

### Better Confidence Scoring
- Confidence threshold increased to 0.8 (from 0.5)
- Shows average confidence scores
- Displays number of unique papers found

### Self-Reflection Loop
- Automatically evaluates if information is comprehensive
- Searches for additional papers if needed
- Limited to 3 iterations to prevent infinite loops

### Real-time Progress Display
- Beautiful step-by-step progress box (no duplicates!)
- Color-coded status indicators
- Shows paper titles as they're retrieved
- Displays search iteration count

### Paper Citations
- Displays paper links as beautiful cards at the bottom
- Shows title, authors, publication date
- Direct links to ArXiv papers
- Available for both current and historical messages

### No Hallucination
- Strict prompts to use ONLY retrieved context
- No external knowledge allowed
- Clear message when no relevant information found

## Example Workflow

When you ask "Tell me about machine learning in 2025", the system will:

1. 🔍 Search Pinecone database
2. ❌ If no relevant info found → Search ArXiv
3. 🔬 Retrieve 5+ papers from ArXiv
4. 📄 Display paper titles
5. 🔍 Check if information is sufficient
6. ⚠️ If not sufficient → Search 3 more papers
7. ✅ Once sufficient → Synthesize response
8. 📥 Index papers in Pinecone for future queries

## Powered by

- **Google Gemini** - For relevancy checking and response synthesis
- **OpenAI Embeddings** - For generating text embeddings (to avoid rate limits)
- **Pinecone** - Vector database for semantic search
- **ArXiv API** - Access to research papers
- **LangGraph** - Orchestration of the RAG pipeline
- **Streamlit** - Beautiful web interface

## Utility Scripts

### Test ArXiv Paper Retrieval
```bash
python scripts/test_arxiv.py
```
This script helps debug what data we're getting from ArXiv papers, including:
- Full metadata examination
- Content length analysis
- Checks if we're getting full papers or just abstracts
- ArXiv ID extraction testing
- **Saves papers to `data/papers/` folder for inspection**

### Analyze Downloaded Papers
```bash
python scripts/analyze_papers.py
```
After running test_arxiv.py, use this to:
- Get statistics on all downloaded papers
- Check if papers are full text or abstracts only
- View average content lengths
- Understand what ArXiv provides