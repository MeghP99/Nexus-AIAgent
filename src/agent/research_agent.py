"""Main research agent with intelligent tool selection and reasoning."""

import os
import logging
from typing import Dict, List, Any, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from .tool_manager import ToolManager
from .prompts import PromptManager


class ResearchAgent:
    """Intelligent research agent with tool selection and reasoning capabilities."""
    
    def __init__(self):
        """Initialize the research agent."""
        self.logger = logging.getLogger(__name__)
        self._step_messages: List[Dict[str, str]] = []
        self._step_callback = None
        
        self._setup_llm()
        self._setup_tools()
        self._setup_prompts()
    
    def _setup_llm(self):
        """Set up the Gemini LLM."""
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
        
        self.logger.info(f"✅ Initialized Gemini LLM with model: {gemini_model}")
    
    def _setup_tools(self):
        """Set up the tool manager."""
        self.tool_manager = ToolManager()
        available_tools = self.tool_manager.get_available_tools()
        self.logger.info(f"✅ Initialized {len(available_tools)} tools: {available_tools}")
    
    def _setup_prompts(self):
        """Set up the prompt manager."""
        available_tools = self.tool_manager.get_available_tools()
        self.prompt_manager = PromptManager(available_tools)
        self.logger.info("✅ Initialized prompt manager")
    
    def get_step_messages(self) -> List[Dict[str, str]]:
        """Get current step messages for UI display."""
        return self._step_messages.copy()
    
    def add_step_message(self, status: str, message: str):
        """Add a step message for UI display."""
        step = {"status": status, "message": message}
        self._step_messages.append(step)
        self.logger.info(f"[{status.upper()}] {message}")
        
        # Call callback if set (for real-time updates)
        if self._step_callback:
            self._step_callback(step)
    
    def clear_step_messages(self):
        """Clear step messages for new query."""
        self._step_messages = []
    
    def _decide_tool_use(self, user_question: str) -> Dict[str, Any]:
        """Decide whether to use tools and which ones."""
        self.add_step_message("searching", "🤔 Analyzing question and determining tool strategy...")
        
        available_tools_desc = "\n".join([
            f"- {name}: {desc}" 
            for name, desc in self.tool_manager.get_tool_descriptions().items()
        ])
        
        prompt = ChatPromptTemplate.from_template(
            self.prompt_manager.get_tool_decision_prompt()
        )
        chain = prompt | self.llm
        
        response = chain.invoke({
            "user_question": user_question,
            "available_tools": available_tools_desc
        })
        content = response.content if hasattr(response, 'content') else str(response)
        
        return self._parse_tool_decision(content)
    
    def _parse_tool_decision(self, content: str) -> Dict[str, Any]:
        """Parse the LLM's tool decision response."""
        lines = content.strip().split('\n')
        
        if "MULTI_TOOL_USE:" in content:
            return self._parse_multi_tool_decision(lines)
        elif "TOOL_USE:" in content:
            return self._parse_single_tool_decision(lines)
        else:
            return self._parse_no_tools_decision(lines)
    
    def _parse_multi_tool_decision(self, lines: List[str]) -> Dict[str, Any]:
        """Parse multi-tool decision."""
        tools = None
        queries = {}
        reasoning = None
        
        for line in lines:
            if line.startswith("MULTI_TOOL_USE:"):
                tools = [t.strip() for t in line.split(":", 1)[1].strip().split(',')]
            elif line.startswith("QUERY1:") and tools:
                queries[tools[0]] = line.split(":", 1)[1].strip()
            elif line.startswith("QUERY2:") and tools and len(tools) > 1:
                queries[tools[1]] = line.split(":", 1)[1].strip()
            elif line.startswith("REASONING:"):
                reasoning = line.split(":", 1)[1].strip()
        
        return {
            "use_tools": True,
            "multi_tool": True,
            "tools": tools or [],
            "queries": queries,
            "reasoning": reasoning or "Multi-tool strategy selected"
        }
    
    def _parse_single_tool_decision(self, lines: List[str]) -> Dict[str, Any]:
        """Parse single tool decision."""
        tool_name = None
        query = None
        reasoning = None
        
        for line in lines:
            if line.startswith("TOOL_USE:"):
                tool_name = line.split(":", 1)[1].strip()
            elif line.startswith("QUERY:"):
                query = line.split(":", 1)[1].strip()
            elif line.startswith("REASONING:"):
                reasoning = line.split(":", 1)[1].strip()
        
        return {
            "use_tools": True,
            "multi_tool": False,
            "tool_name": tool_name,
            "query": query,
            "reasoning": reasoning or "Single tool strategy selected"
        }
    
    def _parse_no_tools_decision(self, lines: List[str]) -> Dict[str, Any]:
        """Parse no tools decision."""
        reasoning = None
        for line in lines:
            if line.startswith("REASONING:"):
                reasoning = line.split(":", 1)[1].strip()
        
        return {
            "use_tools": False,
            "reasoning": reasoning or "Can answer with existing knowledge"
        }
    
    def _execute_tools(self, tool_decision: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute tools based on the decision."""
        tool_results = []
        
        if tool_decision.get("multi_tool", False):
            tools = tool_decision.get("tools", [])
            queries = tool_decision.get("queries", {})
            
            for tool_name in tools:
                if tool_name in queries and self.tool_manager.is_tool_available(tool_name):
                    query = queries[tool_name]
                    result = self._execute_single_tool(tool_name, query)
                    tool_results.append(result)
        else:
            tool_name = tool_decision.get("tool_name")
            query = tool_decision.get("query")
            
            if tool_name and query:
                result = self._execute_single_tool(tool_name, query)
                tool_results.append(result)
        
        return tool_results
    
    def _execute_single_tool(self, tool_name: str, query: str) -> Dict[str, Any]:
        """Execute a single tool and log the result."""
        self.add_step_message("searching", f"🔍 Executing {tool_name}: {query}")
        
        result = self.tool_manager.execute_tool(tool_name, query)
        
        if result.get("success", False):
            if tool_name == "calculator":
                self.add_step_message("found", f"✅ Calculation completed: {result.get('result')}")
            else:
                count = len(result.get("results", []))
                self.add_step_message("found", f"✅ Found {count} results from {tool_name}")
        else:
            self.add_step_message("error", f"❌ {tool_name} failed: {result.get('message')}")
        
        return result
    
    def _synthesize_response(self, user_question: str, tool_results: List[Dict[str, Any]]) -> str:
        """Synthesize final response using tool results and existing knowledge."""
        self.add_step_message("synthesizing", "🧠 Synthesizing comprehensive response from all sources...")
        
        tool_results_text = self._format_tool_results(tool_results)
        
        prompt = ChatPromptTemplate.from_template(
            self.prompt_manager.get_synthesis_prompt()
        )
        chain = prompt | self.llm
        
        response = chain.invoke({
            "user_question": user_question,
            "tool_results": tool_results_text
        })
        
        self.add_step_message("completed", "✅ Response synthesized successfully!")
        
        return response.content if hasattr(response, 'content') else str(response)
    
    def _format_tool_results(self, tool_results: List[Dict[str, Any]]) -> str:
        """Format tool results for the synthesis prompt."""
        if not tool_results:
            return "No tools were used for this response."
        
        formatted_text = ""
        for result in tool_results:
            tool_name = result.get('tool_name', 'unknown')
            success = result.get('success', False)
            
            if success:
                if tool_name == "calculator":
                    formatted_text += f"\n=== {tool_name.upper()} RESULT ===\n"
                    formatted_text += f"Calculation: {result.get('result')}\n"
                else:
                    formatted_text += f"\n=== {tool_name.upper()} RESULTS ===\n"
                    results = result.get('results', [])
                    for i, res in enumerate(results[:3], 1):  # Limit to top 3
                        formatted_text += f"\nResult {i}:\n"
                        formatted_text += f"Title: {res.get('title', 'N/A')}\n"
                        if 'authors' in res:
                            formatted_text += f"Authors: {res.get('authors', 'N/A')}\n"
                        if 'url' in res:
                            formatted_text += f"URL: {res.get('url', 'N/A')}\n"
                        formatted_text += f"Content: {res.get('content', 'N/A')}\n"
            else:
                formatted_text += f"\n=== {tool_name.upper()} ERROR ===\n"
                formatted_text += f"Error: {result.get('message', 'Unknown error')}\n"
        
        return formatted_text
    
    def _extract_context_from_results(self, tool_results: List[Dict[str, Any]]) -> List[str]:
        """Extract context strings from tool results for UI display."""
        context = []
        for result in tool_results:
            if result.get("success") and "results" in result:
                for res in result["results"]:
                    if "content" in res:
                        context.append(res["content"])
        return context
    
    def _extract_metadata_from_results(self, tool_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract metadata from tool results for UI display."""
        all_metadata = []
        for result in tool_results:
            if result.get("success") and "metadata" in result:
                all_metadata.extend(result["metadata"])
        return all_metadata
    
    def research(self, user_question: str) -> Dict[str, Any]:
        """Main research method that orchestrates the entire agentic process.
        
        Args:
            user_question: The user's research question
            
        Returns:
            Dict containing the research results and metadata
        """
        # Clear previous step messages
        self.clear_step_messages()
        
        # Step 1: Analyze question and decide on tool usage
        self.add_step_message("checking", "🚀 Starting intelligent research process...")
        tool_decision = self._decide_tool_use(user_question)
        
        # Step 2: Execute tools if needed
        tool_results = []
        if tool_decision.get("use_tools", False):
            reasoning = tool_decision.get("reasoning", "")
            self.add_step_message("checking", f"💭 Strategy: {reasoning}")
            tool_results = self._execute_tools(tool_decision)
        else:
            reasoning = tool_decision.get("reasoning", "")
            self.add_step_message("completed", f"✅ Using existing knowledge: {reasoning}")
        
        # Step 3: Synthesize final response
        final_response = self._synthesize_response(user_question, tool_results)
        
        return {
            "final_response": final_response,
            "step_messages": self.get_step_messages(),
            "tool_results": tool_results,
            "paper_metadata": self._extract_metadata_from_results(tool_results),
            "context": self._extract_context_from_results(tool_results)
        }
    
    def research_stream(self, user_question: str):
        """Generator version of research that yields step updates in real-time.
        
        Args:
            user_question: The user's research question
            
        Yields:
            Dict containing step updates or final result
        """
        # Clear previous step messages
        self.clear_step_messages()
        
        # Queue to collect yielded steps
        step_queue = []
        
        # Set up callback to collect step updates
        def step_collector(step):
            step_queue.append(step)
        
        self._step_callback = step_collector
        
        try:
            # Step 1: Analyze question and decide on tool usage
            self.add_step_message("checking", "🚀 Starting intelligent research process...")
            # Yield any collected steps
            for step in step_queue:
                yield {"type": "step", "step": step}
            step_queue.clear()
            
            tool_decision = self._decide_tool_use(user_question)
            # Yield any collected steps
            for step in step_queue:
                yield {"type": "step", "step": step}
            step_queue.clear()
            
            # Step 2: Execute tools if needed
            tool_results = []
            if tool_decision.get("use_tools", False):
                reasoning = tool_decision.get("reasoning", "")
                self.add_step_message("checking", f"💭 Strategy: {reasoning}")
                # Yield any collected steps
                for step in step_queue:
                    yield {"type": "step", "step": step}
                step_queue.clear()
                
                tool_results = self._execute_tools(tool_decision)
                # Yield any collected steps
                for step in step_queue:
                    yield {"type": "step", "step": step}
                step_queue.clear()
            else:
                reasoning = tool_decision.get("reasoning", "")
                self.add_step_message("completed", f"✅ Using existing knowledge: {reasoning}")
                # Yield any collected steps
                for step in step_queue:
                    yield {"type": "step", "step": step}
                step_queue.clear()
            
            # Step 3: Synthesize final response
            final_response = self._synthesize_response(user_question, tool_results)
            # Yield any collected steps
            for step in step_queue:
                yield {"type": "step", "step": step}
            step_queue.clear()
            
            # Yield final result
            yield {
                "type": "final",
                "result": {
                    "final_response": final_response,
                    "step_messages": self.get_step_messages(),
                    "tool_results": tool_results,
                    "paper_metadata": self._extract_metadata_from_results(tool_results),
                    "context": self._extract_context_from_results(tool_results)
                }
            }
            
        finally:
            # Clean up callback
            self._step_callback = None
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools."""
        return self.tool_manager.get_available_tools()
    
    def get_tool_count(self) -> int:
        """Get the number of available tools."""
        return self.tool_manager.get_tool_count()
