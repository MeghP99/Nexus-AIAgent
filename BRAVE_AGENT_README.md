# Brave API Agent

A standalone research agent that uses Brave Search API as a tool for web research and information gathering.

## Features

- **Brave Search Integration**: Search the web for current information and research papers
- **Calculator Tool**: Perform basic mathematical calculations
- **Gemini LLM**: Powered by Google's Gemini model
- **Custom Prompts**: Uses custom-designed prompts (no out-of-the-box templates)
- **Modular Design**: Standalone agent that doesn't depend on the main LangGraph pipeline
- **Interactive Mode**: Chat with the agent interactively
- **Tool Decision Making**: Intelligently decides when to use tools vs. existing knowledge

## Files

- `test_brave_api.py` - Test script to verify Brave API functionality
- `brave_agent.py` - Main agent implementation with Brave search tool
- `demo_brave_agent.py` - Demo launcher with various options

## Setup

### 1. Environment Variables

Create a `.env` file in the project root with the following:

```env
GOOGLE_API_KEY=your_google_api_key_here
BRAVE_API_KEY=your_brave_api_key_here
GEMINI_MODEL=gemini-2.5-flash  # optional, defaults to gemini-2.5-flash
```

### 2. Dependencies

All required dependencies are already in `requirements.txt`. Make sure to install them:

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Demo Launcher (Recommended)

```bash
python demo_brave_agent.py
```

This will:
- Check your environment variables
- Give you options to run demos, tests, or interactive mode

### Option 2: Direct Agent Usage

```bash
# Interactive mode
python brave_agent.py

# Direct query mode
python brave_agent.py "What are the latest AI research developments?"
```

### Option 3: Test Brave API Only

```bash
python test_brave_api.py
```

## Agent Capabilities

### Tools Available

1. **Brave Search** (`brave_search`)
   - Search the web for current information
   - Find research papers and academic content
   - Get up-to-date information on any topic

2. **Calculator** (`calculator`)
   - Perform basic mathematical operations
   - Support for arithmetic, parentheses, etc.
   - Safe evaluation of mathematical expressions

### Example Queries

- "What are the latest developments in quantum computing?"
- "Find recent research papers about machine learning interpretability"
- "Calculate the compound interest on $10000 at 5% for 10 years"
- "What is the environmental impact of cryptocurrency mining?"
- "Search for recent AI breakthroughs in 2024"

## Architecture

### Tool Decision Making

The agent uses a custom prompt to analyze user questions and decide:
1. Whether tools are needed
2. Which tool to use
3. What query/expression to use with the tool

### Response Synthesis

After tool execution, the agent synthesizes:
- Tool results
- Its own knowledge
- Properly cited sources
- Comprehensive answers

### Custom Prompts

All prompts are custom-designed following the user's preference for avoiding out-of-the-box solutions:

- **System Prompt**: Defines the agent's role and capabilities
- **Tool Decision Prompt**: Analyzes questions to determine tool usage
- **Synthesis Prompt**: Combines tool results with existing knowledge

## Integration with Existing Project

This agent is designed to be **standalone** and **modular**:

- ✅ No dependencies on the main LangGraph pipeline
- ✅ Uses the existing `BraveRetriever` from `src/retrievers/brave.py`
- ✅ Follows the same configuration pattern (environment variables)
- ✅ Can be used independently or integrated into other systems

## Troubleshooting

### Common Issues

1. **"BRAVE_API_KEY not set"**
   - Make sure you have a `.env` file with `BRAVE_API_KEY=your_key`
   - Get a Brave Search API key from [Brave Search API](https://brave.com/search/api/)

2. **"GOOGLE_API_KEY not found"**
   - Add `GOOGLE_API_KEY=your_key` to your `.env` file
   - Get a Google AI Studio API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. **"No results found"**
   - Try different search terms
   - Check your Brave API key permissions
   - Verify your internet connection

### Getting API Keys

- **Google API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Brave API Key**: Visit [Brave Search API](https://brave.com/search/api/)

## Examples

### Interactive Session Example

```
💬 You: What are the latest developments in AI research?

📋 Step 1: Analyzing question and deciding on tool usage...
🔧 Tool needed: brave_search
📝 Query/Expression: latest AI research developments 2024
💭 Reasoning: Need current information about recent AI developments

⚡ Step 2: Executing brave_search...
✅ Tool execution successful
🔍 Found 5 search results

🧠 Step 3: Synthesizing comprehensive response...

📋 FINAL RESPONSE:
Based on recent search results, here are the latest developments in AI research as of 2024:

[Detailed response with citations...]
```

### Direct Query Example

```bash
python brave_agent.py "Calculate the area of a circle with radius 10"

# Output will show tool decision making and final calculation
```
