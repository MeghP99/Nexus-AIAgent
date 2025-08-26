"""Standalone agent that uses Brave API as a tool."""
import os
import sys
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Using absolute imports from src directory

load_dotenv()

class BraveSearchTool:
    """Tool wrapper for Brave Search functionality."""
    
    def __init__(self):
        """Initialize Brave search tool."""
        # Import directly from the module to avoid __init__.py dependencies
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'retrievers'))
        from brave import BraveRetriever
        self.retriever = BraveRetriever()
        self.name = "brave_search"
        self.description = "Search the web for current information, research papers, and general knowledge using Brave Search engine."
    
    def execute(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Execute Brave search and return results."""
        try:
            documents, metadata = self.retriever.retrieve(query, max_docs=max_results)
            
            if not documents:
                return {
                    "success": False,
                    "message": "No results found",
                    "results": []
                }
            
            results = []
            for doc, meta in zip(documents, metadata):
                results.append({
                    "title": meta["title"],
                    "url": meta["url"],
                    "content": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                    "source": meta["source"]
                })
            
            return {
                "success": True,
                "message": f"Found {len(results)} results",
                "results": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error during search: {str(e)}",
                "results": []
            }

class CalculatorTool:
    """Simple calculator tool for basic math operations."""
    
    def __init__(self):
        self.name = "calculator"
        self.description = "Perform basic mathematical calculations including arithmetic operations."
    
    def execute(self, expression: str) -> Dict[str, Any]:
        """Execute a mathematical expression safely."""
        try:
            # Basic safety check - only allow specific characters
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return {
                    "success": False,
                    "message": "Invalid characters in expression. Only numbers and basic operators (+, -, *, /, parentheses) are allowed.",
                    "result": None
                }
            
            # Evaluate the expression safely
            result = eval(expression)
            return {
                "success": True,
                "message": f"Calculation completed: {expression} = {result}",
                "result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error in calculation: {str(e)}",
                "result": None
            }

class ResearchAgent:
    """Standalone research agent with Brave search capabilities."""
    
    def __init__(self):
        """Initialize the research agent with tools and LLM."""
        self._setup_llm()
        self._setup_tools()
        self._setup_prompts()
    
    def _setup_llm(self):
        """Set up the Gemini LLM."""
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        self.llm = ChatGoogleGenerativeAI(
            model=gemini_model,
            temperature=0.1,
            max_tokens=None,
            timeout=30,
            max_retries=2,
            google_api_key=google_api_key,
        )
        
        print(f"✅ Initialized Gemini LLM with model: {gemini_model}")
    
    def _setup_tools(self):
        """Set up available tools."""
        self.tools = {
            "brave_search": BraveSearchTool(),
            "calculator": CalculatorTool()
        }
        
        print(f"✅ Initialized {len(self.tools)} tools: {list(self.tools.keys())}")
    
    def _setup_prompts(self):
        """Set up custom prompts for the agent."""
        # Custom system prompt - not using out-of-the-box prompts
        self.system_prompt = """You are a knowledgeable research assistant with access to web search capabilities. Your goal is to provide accurate, helpful, and well-researched responses to user queries.

AVAILABLE TOOLS:
1. brave_search(query, max_results=5): Search the web for current information, research papers, and general knowledge
2. calculator(expression): Perform mathematical calculations

INSTRUCTIONS:
1. Always think step by step about what information you need
2. Use tools when you need current information or specific data that you don't already know
3. For research questions, use brave_search to find recent papers or information
4. For calculations, use the calculator tool
5. Always cite your sources when using search results
6. Be transparent about when you're using tools vs. your own knowledge
7. If search results are not sufficient, try different search terms

RESPONSE FORMAT:
- Start with a brief analysis of what you need to find
- Use tools as needed and explain what you're searching for
- Synthesize the information clearly
- Provide sources for any external information used

Remember: You have access to current web information through Brave search, so you can provide up-to-date information on recent events, research, and developments."""
        
        self.tool_use_prompt = """Based on the user's question, determine if you need to use any tools.

USER QUESTION: {user_question}

AVAILABLE TOOLS:
- brave_search(query, max_results): Search web for current information
- calculator(expression): Perform calculations

Think about what you need:
1. Do you need current/recent information? → Use brave_search
2. Do you need to perform calculations? → Use calculator  
3. Can you answer with existing knowledge? → No tools needed

If you need to use a tool, respond with:
TOOL_USE: tool_name
QUERY/EXPRESSION: what to search for or calculate
REASONING: why you need this tool

If no tools needed, respond with:
NO_TOOLS_NEEDED: I can answer this with existing knowledge"""
        
        self.synthesis_prompt = """You are synthesizing information to answer a user's question.

USER QUESTION: {user_question}

TOOL RESULTS:
{tool_results}

YOUR KNOWLEDGE: You also have general knowledge that you can use alongside the tool results.

INSTRUCTIONS:
1. Combine the tool results with your existing knowledge
2. Provide a comprehensive answer
3. Cite sources from tool results when used
4. Be clear about what comes from external sources vs. your knowledge
5. If tool results are insufficient, acknowledge limitations

Provide a well-structured, informative response:"""

    def _decide_tool_use(self, user_question: str) -> Dict[str, Any]:
        """Decide whether to use tools and which ones."""
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_template(self.tool_use_prompt)
        chain = prompt | self.llm
        
        response = chain.invoke({"user_question": user_question})
        content = response.content if hasattr(response, 'content') else str(response)
        
        # Parse the response
        if "TOOL_USE:" in content:
            lines = content.strip().split('\n')
            tool_name = None
            query_expr = None
            reasoning = None
            
            for line in lines:
                if line.startswith("TOOL_USE:"):
                    tool_name = line.split(":", 1)[1].strip()
                elif line.startswith("QUERY/EXPRESSION:"):
                    query_expr = line.split(":", 1)[1].strip()
                elif line.startswith("REASONING:"):
                    reasoning = line.split(":", 1)[1].strip()
            
            return {
                "use_tool": True,
                "tool_name": tool_name,
                "query_expression": query_expr,
                "reasoning": reasoning
            }
        else:
            return {"use_tool": False}
    
    def _execute_tool(self, tool_name: str, query_expression: str) -> Dict[str, Any]:
        """Execute a specific tool with the given input."""
        if tool_name not in self.tools:
            return {
                "success": False,
                "message": f"Tool '{tool_name}' not available. Available tools: {list(self.tools.keys())}"
            }
        
        tool = self.tools[tool_name]
        
        if tool_name == "brave_search":
            return tool.execute(query_expression)
        elif tool_name == "calculator":
            return tool.execute(query_expression)
        else:
            return {
                "success": False,
                "message": f"Unknown tool execution method for {tool_name}"
            }
    
    def _synthesize_response(self, user_question: str, tool_results: List[Dict[str, Any]]) -> str:
        """Synthesize final response using tool results and existing knowledge."""
        from langchain_core.prompts import ChatPromptTemplate
        
        # Format tool results for the prompt
        tool_results_text = ""
        if tool_results:
            tool_results_text = "\n".join([
                f"Tool: {result.get('tool_name', 'unknown')}\n"
                f"Success: {result.get('success', False)}\n"
                f"Result: {json.dumps(result.get('result', result.get('results', result.get('message', 'No result'))), indent=2)}\n"
                for result in tool_results
            ])
        else:
            tool_results_text = "No tools were used for this response."
        
        prompt = ChatPromptTemplate.from_template(self.synthesis_prompt)
        chain = prompt | self.llm
        
        response = chain.invoke({
            "user_question": user_question,
            "tool_results": tool_results_text
        })
        
        return response.content if hasattr(response, 'content') else str(response)
    
    def chat(self, user_question: str) -> str:
        """Main chat interface for the agent."""
        print(f"\n🤔 User Question: {user_question}")
        print("=" * 60)
        
        # Step 1: Decide if tools are needed
        print("📋 Step 1: Analyzing question and deciding on tool usage...")
        tool_decision = self._decide_tool_use(user_question)
        
        tool_results = []
        
        if tool_decision.get("use_tool", False):
            tool_name = tool_decision.get("tool_name")
            query_expr = tool_decision.get("query_expression")
            reasoning = tool_decision.get("reasoning")
            
            print(f"🔧 Tool needed: {tool_name}")
            print(f"📝 Query/Expression: {query_expr}")
            print(f"💭 Reasoning: {reasoning}")
            
            # Step 2: Execute the tool
            print(f"\n⚡ Step 2: Executing {tool_name}...")
            tool_result = self._execute_tool(tool_name, query_expr)
            tool_result["tool_name"] = tool_name
            tool_results.append(tool_result)
            
            if tool_result.get("success", False):
                print(f"✅ Tool execution successful")
                if tool_name == "brave_search" and tool_result.get("results"):
                    print(f"🔍 Found {len(tool_result['results'])} search results")
                elif tool_name == "calculator":
                    print(f"🧮 Calculation result: {tool_result.get('result')}")
            else:
                print(f"❌ Tool execution failed: {tool_result.get('message')}")
        else:
            print("✅ No tools needed - can answer with existing knowledge")
        
        # Step 3: Synthesize final response
        print(f"\n🧠 Step 3: Synthesizing comprehensive response...")
        final_response = self._synthesize_response(user_question, tool_results)
        
        print("\n" + "=" * 60)
        print("📋 FINAL RESPONSE:")
        print("=" * 60)
        
        return final_response
    
    def interactive_mode(self):
        """Start interactive chat mode."""
        print("\n🤖 Research Agent with Brave Search")
        print("=" * 50)
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Type 'tools' to see available tools")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'tools':
                    print("\n🔧 Available Tools:")
                    for tool_name, tool in self.tools.items():
                        print(f"  • {tool_name}: {tool.description}")
                    continue
                elif not user_input:
                    continue
                
                response = self.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main function to run the agent."""
    print("🚀 Initializing Research Agent with Brave Search...")
    
    try:
        agent = ResearchAgent()
        print("\n✅ Agent initialized successfully!")
        
        # Check if we have command line arguments for direct query
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
            print(f"\n🎯 Direct query mode: {query}")
            response = agent.chat(query)
            print(response)
        else:
            # Start interactive mode
            agent.interactive_mode()
            
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
