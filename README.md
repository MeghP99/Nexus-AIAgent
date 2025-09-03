# 🧠 Agentic Research Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://langchain.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini--2.5--Flash-orange.svg)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **An intelligent research assistant that automatically selects the best tools to answer complex questions using ArXiv papers, web search, mathematical calculations, and vector databases.**

## 🌟 **Project Highlights**

This project showcases advanced **AI agent architecture** with sophisticated **tool selection**, **multi-step reasoning**, and **intelligent synthesis** capabilities. 

### 🎯 **Key Achievements**

- **🤖 Intelligent Agent System**: LLM-powered decision engine that automatically selects optimal tools
- **🧠 Multi-Modal Research**: Seamlessly combines academic papers, web search, and calculations

---
## 🚀 **Core Features**

### **🔍 Intelligent Tool Selection**
The agent analyzes each query and automatically determines the best approach:
- **Academic Research** → ArXiv + PubMed + Vector Database
- **Current Events** → Brave Web Search + News APIs  
- **Mathematical Problems** → Safe Expression Evaluator
- **Hybrid Queries** → Multi-tool coordination and synthesis

### **🧠 Advanced Reasoning Pipeline**
```
User Query → Intent Analysis → Tool Selection → Parallel Execution → Intelligent Synthesis → Response
```


---

## 🏗️ **Architecture Overview**

### **Modular Design Pattern**
```
├── 🎯 Agent System (Intelligence Layer)
│   ├── ResearchAgent     # Main orchestrator
│   ├── ToolManager       # Tool coordination  
│   └── PromptManager     # Custom prompt templates
├── 🔧 Tools (Execution Layer)
│   ├── ArxivSearchTool   # Academic paper search
│   ├── BraveSearchTool   # Web search engine
│   ├── CalculatorTool    # Mathematical operations
│   └── PineconeSearchTool # Vector database search
├── 🎨 UI Components (Presentation Layer)
│   ├── StyleManager      # CSS & theming
│   └── UIComponents      # Reusable Streamlit components
└── 📊 Data Layer
    ├── Vector Store      # Pinecone embeddings
    └── Paper Cache       # Local document storage
```

### **Technology Stack**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI Engine** | Google Gemini 2.5 Flash | Natural language processing & reasoning |
| **Web Framework** | Streamlit | Interactive web application |
| **Vector Database** | Pinecone | Semantic document search |
| **Web Search** | Brave Search API | Current information retrieval |
| **Academic Search** | ArXiv API | Research paper access |
| **Embeddings** | OpenAI text-embedding-3-small | Document vectorization |

---

## 🎯 **Intelligent Agent Capabilities**

### **🔄 Multi-Step Reasoning Process**

1. **Intent Analysis**: Understands query type and complexity
2. **Strategy Planning**: Determines single vs. multi-tool approach  
3. **Tool Orchestration**: Executes tools in optimal sequence
4. **Result Synthesis**: Combines information from multiple sources
5. **Quality Assurance**: Validates results and handles errors

### **🎭 Example Agent Decisions**

| Query Type | Agent Strategy | Tools Used |
|------------|---------------|------------|
| *"Latest transformer architecture improvements"* | Academic + Current | ArXiv → Brave Search |
| *"Calculate ROI for ML model deployment"* | Mathematical | Calculator Only |
| *"Quantum computing progress in 2024"* | Hybrid Research | ArXiv + Web + Vector DB |
| *"Explain attention mechanisms"* | Knowledge-based | Existing Knowledge |

---

## 📊 **Performance Metrics**

### **Code Quality Improvements**
- **85% reduction** in main application complexity (772 → 149 lines)
- **100% type-annotated** codebase with comprehensive documentation
- **Zero circular dependencies** with clean module separation
- **Modular architecture** enabling easy testing and maintenance

### **User Experience**
- **Real-time feedback** with live processing steps
- **Multi-source synthesis** for comprehensive answers  
- **Error recovery** with graceful fallback mechanisms
- **Mobile-responsive** design for all devices

---

## 🛠️ **Installation & Setup**

### **Prerequisites**
```bash
Python 3.8+
Virtual Environment (recommended)
```

### **Quick Start**
```bash
# Clone repository
git clone <repository-url>
cd agentic-research-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Launch application
streamlit run app.py
```

### **Environment Configuration**
```bash
# Required API Keys
GOOGLE_API_KEY=your_gemini_api_key
BRAVE_API_KEY=your_brave_search_key

# Optional (for vector database)
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=your_index_name

# Model Configuration
GEMINI_MODEL=gemini-2.5-flash
CONFIDENCE_THRESHOLD=0.8
```

---

## 🎮 **Usage Examples**

### **Academic Research**
```
💬 "What are the latest developments in multimodal transformers?"

🤖 Agent Process:
   🔍 Analyzing query → Academic research needed
   📚 Searching ArXiv → Found 5 recent papers
   🌐 Web search → Latest news and tutorials  
   🧠 Synthesizing → Comprehensive overview with citations
```

### **Mathematical Problem Solving**
```
💬 "Calculate the compound annual growth rate for 150% growth over 3 years"

🤖 Agent Process:
   🔍 Analyzing query → Mathematical calculation needed
   🧮 Calculator → ((2.5)^(1/3) - 1) * 100 = 35.72%
   📊 Result → 35.72% CAGR with explanation
```
```

---


## 🚀 **Future Enhancements**

### **Phase 1: Enhanced Intelligence**
- [ ] **Multi-agent collaboration** for complex research tasks
- [ ] **Memory persistence** across conversations
- [ ] **Learning from user feedback** to improve tool selection

### **Phase 2: Advanced Integrations**
- [ ] **PDF document upload** and analysis
- [ ] **Citation network analysis** for paper recommendations
- [ ] **Collaborative filtering** for personalized results

### **Phase 3: Enterprise Features**
- [ ] **User authentication** and workspace management
- [ ] **API endpoints** for programmatic access
- [ ] **Advanced analytics** dashboard

---

## 🏆 **Technical Achievements**

### **Software Engineering Excellence**
- ✅ **SOLID Principles**: Single responsibility, open/closed, dependency inversion
- ✅ **Design Patterns**: Factory, Strategy, Observer patterns implemented
- ✅ **Clean Architecture**: Clear separation between layers
- ✅ **Type Safety**: Full type annotations with mypy compatibility

### **AI/ML Engineering**
- ✅ **Agent Architecture**: Sophisticated reasoning and tool orchestration
- ✅ **Prompt Engineering**: Custom prompts optimized for each use case
- ✅ **Multi-Modal Integration**: Seamless text, web, and calculation synthesis
- ✅ **Vector Search**: Semantic similarity with confidence thresholding

### **Production Readiness**
- ✅ **Error Handling**: Comprehensive exception management
- ✅ **Logging**: Structured logging for debugging and monitoring
- ✅ **Configuration**: Environment-based configuration management
- ✅ **Documentation**: Complete API documentation and architecture guides

---

## 📈 **Project Impact**

This project demonstrates expertise in:

- **🤖 AI Agent Development**: Building intelligent systems that reason and act
- **🏗️ Software Architecture**: Designing scalable, maintainable systems  
- **🔧 Tool Integration**: Combining multiple APIs and services seamlessly
- **🎨 User Experience**: Creating intuitive interfaces for complex functionality
- **📊 Data Engineering**: Managing vector databases and information retrieval
