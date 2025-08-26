"""UI components for the Streamlit application."""

import streamlit as st
import time
from typing import List, Dict, Any, Optional

from .styles import StyleManager


class UIComponents:
    """UI component utilities for the research assistant."""
    
    def __init__(self):
        """Initialize UI components."""
        self.style_manager = StyleManager()
    
    def setup_page_config(self):
        """Set up Streamlit page configuration."""
        st.set_page_config(
            page_title="Agentic Research Assistant",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="auto",
        )
        
        # Apply custom styles
        self.style_manager.apply_custom_styles()
    
    def render_header(self):
        """Render the main application header."""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.title("🧠 Agentic Research Assistant")
            st.write("Intelligent research assistant that automatically selects the best tools to answer your questions - ArXiv papers, web search, calculations, and more!")
        
        return col1, col2
    
    def render_agent_status(self, agent=None):
        """Render agent status in sidebar.
        
        Args:
            agent: Research agent instance or None if failed to initialize
        """
        if agent:
            st.sidebar.success("🤖 Agentic Research System Active!")
            tool_names = agent.get_available_tools()
            tool_count = len(tool_names)
            st.sidebar.info(f"🔧 {tool_count} Tools Available: {', '.join(tool_names)}")
            
            # Add tool details
            with st.sidebar.expander("🔍 Tool Details", expanded=False):
                for tool_name in tool_names:
                    if tool_name == "arxiv_search":
                        st.write("📚 **ArXiv Search**: Academic papers and research")
                    elif tool_name == "brave_search":
                        st.write("🌐 **Brave Search**: Current web information")
                    elif tool_name == "calculator":
                        st.write("🧮 **Calculator**: Mathematical calculations")
                    elif tool_name == "pinecone_search":
                        st.write("🗄️ **Vector Database**: Stored documents")
                    elif tool_name == "webscraper":
                        st.write("📄 **Web Scraper**: Extract full content from URLs")
        else:
            st.sidebar.error("❌ Agent initialization failed!")
            st.sidebar.warning("Please check your configuration and environment variables.")
    
    def display_step_message(self, step: Dict[str, str]) -> str:
        """Generate simple text for a single step message.
        
        Args:
            step: Step dictionary with 'status' and 'message' keys
            
        Returns:
            Simple formatted text for the step
        """
        status = step.get("status", "")
        message = step.get("message", "")
        
        # Status-based emojis and prefixes
        status_prefixes = {
            "checking": "🔍",
            "searching": "🔎", 
            "found": "✅",
            "error": "❌",
            "synthesizing": "🧠",
            "completed": "✅"
        }
        
        prefix = status_prefixes.get(status, "📝")
        return f"{prefix} {message}"
    
    def display_steps_container(self, steps: List[Dict[str, str]]) -> str:
        """Generate simple markdown for all steps.
        
        Args:
            steps: List of step dictionaries
            
        Returns:
            Markdown string for the steps
        """
        if not steps:
            return ""
        
        steps_text = "**🔄 Processing Steps**\n\n"
        
        for step in steps:
            step_text = self.display_step_message(step)
            steps_text += f"- {step_text}\n"
        
        return steps_text
    
    def display_tool_result_dropdown(self, tool_result: Dict[str, Any]):
        """Display tool result as a Streamlit expander (no HTML).
        
        Args:
            tool_result: Tool result dictionary
        """
        tool_name = tool_result.get("tool_name", "Unknown")
        success = tool_result.get("success", False)
        message = tool_result.get("message", "No message")
        results = tool_result.get("results", [])
        
        # Determine status icon
        status_icon = "✅" if success else "❌"
        summary = f"{status_icon} {tool_name}: {message}"
        
        with st.expander(f"🔍 {summary}", expanded=False):
            if success and results:
                result_count = len(results)
                st.write(f"**Found {result_count} results:**")
                
                # Show preview of results
                for i, result in enumerate(results[:3], 1):
                    title = result.get("title", "No title")
                    content = result.get("content", "")
                    url = result.get("url", "")
                    
                    st.markdown(f"**{i}. {title[:100]}{'...' if len(title) > 100 else ''}**")
                    
                    if url:
                        st.markdown(f"🔗 **URL:** {url[:80]}{'...' if len(url) > 80 else ''}")
                    
                    if content:
                        preview_content = content[:200] + "..." if len(content) > 200 else content
                        # Create unique key using tool name, index, content hash, and timestamp
                        unique_key = f"preview_{tool_name}_{i}_{hash(content[:50])}_{int(time.time() * 1000000)}"
                        st.text_area("Content Preview:", preview_content, height=60, disabled=True, key=unique_key)
                    
                    if i < min(len(results), 3):
                        st.divider()
                
                if result_count > 3:
                    st.write(f"*... and {result_count - 3} more results*")
            
            elif success and tool_name == "calculator":
                calc_result = tool_result.get("result", "No result")
                st.code(f"Result: {calc_result}")
            
            elif not success:
                st.error(f"**Error:** {message}")
            
            else:
                st.info("No results to display")
    
    def render_context_expander(self, context: List[str], tool_results: List[Dict] = None, synthesis_reasoning: str = None):
        """Render context information and LLM reasoning in an expander.
        
        Args:
            context: List of context strings
            tool_results: List of tool results used
            synthesis_reasoning: LLM's reasoning process (if available)
        """
        if not context and not tool_results:
            return
        
        with st.expander("🧠 View Retrieved Context & LLM Reasoning", expanded=False):
            # LLM Reasoning Section
            if synthesis_reasoning:
                st.markdown("### 🤔 LLM Reasoning Process:")
                st.info(synthesis_reasoning)
                st.markdown("---")
            
            # Tool Summary Section
            if tool_results:
                st.markdown("### 🔧 Tools Used:")
                for tool_result in tool_results:
                    tool_name = tool_result.get("tool_name", "Unknown")
                    success = tool_result.get("success", False)
                    message = tool_result.get("message", "")
                    
                    if success:
                        st.success(f"✅ **{tool_name}**: {message}")
                    else:
                        st.error(f"❌ **{tool_name}**: {message}")
                st.markdown("---")
            
            # Context Section
            if context:
                st.markdown("### 📄 Retrieved Content Excerpts:")
                for i, context_item in enumerate(context[:5], 1):
                    st.markdown(f"**Excerpt {i}:**")
                    display_context = context_item[:800] + "..." if len(context_item) > 800 else context_item
                    
                    # Use a code block for better formatting
                    st.code(display_context, language=None)
                    if i < min(len(context), 5):  # Don't add separator after last item
                        st.markdown("---")
                
                st.markdown(f"**📊 Total context chunks:** {len(context)}")
            
            # Synthesis Note
            st.markdown("### 💡 Synthesis Note:")
            st.info("🎯 The LLM carefully analyzed the above information from multiple sources to create a comprehensive, factual response. All claims are backed by the retrieved data.")
    
    def render_paper_metadata(self, paper_metadata: List[Dict[str, Any]]):
        """Render metadata as cards - papers or web results.
        
        Args:
            paper_metadata: List of metadata dictionaries
        """
        if not paper_metadata:
            return
        
        # Separate academic papers from web results and scraped content
        academic_papers = [item for item in paper_metadata if item.get('content_type') not in ['web', 'scraped_web']]
        web_results = [item for item in paper_metadata if item.get('content_type') == 'web']
        scraped_results = [item for item in paper_metadata if item.get('content_type') == 'scraped_web']
        
        # Render academic papers section
        if academic_papers:
            st.markdown("### 📚 Referenced Papers")
            cols = st.columns(min(len(academic_papers), 3))
            for idx, paper in enumerate(academic_papers):
                col_idx = idx % 3
                with cols[col_idx]:
                    paper_html = self.style_manager.get_paper_card_html(paper)
                    st.markdown(paper_html, unsafe_allow_html=True)
        
        # Render web results section
        if web_results:
            st.markdown("### 🌐 Web Sources")
            st.markdown("*Search results from Brave Search*")
            st.markdown("---")
            for result in web_results[:5]:  # Limit to top 5 web results
                self._render_web_result_card(result)
        
        # Render scraped content section
        if scraped_results:
            st.markdown("### 📄 Scraped Content")
            st.markdown("*Full articles extracted from web pages*")
            st.markdown("---")
            for result in scraped_results:
                self._render_scraped_result_card(result)
    
    def _render_web_result_card(self, result: Dict[str, Any]):
        """Render a single web result card.
        
        Args:
            result: Web result metadata dictionary
        """
        title = result.get('title', 'Web Result')
        url = result.get('url', '')
        snippet = result.get('snippet', '')
        
        # Create a nice card layout with border
        with st.container():
            # Use a colored container to make it look like a card
            col1, col2 = st.columns([1, 10])
            with col1:
                st.markdown("🔗")
            with col2:
                st.markdown(f"**{title[:100]}{'...' if len(title) > 100 else ''}**")
                
                if snippet:
                    st.write(snippet)
                
                if url:
                    st.markdown(f"🌐 **Source:** [{url}]({url})")
                else:
                    st.write("*No URL available*")
            
            st.markdown("---")
    
    def _render_scraped_result_card(self, result: Dict[str, Any]):
        """Render a single scraped content card with content preview.
        
        Args:
            result: Scraped content metadata dictionary
        """
        title = result.get('title', 'Scraped Content')
        url = result.get('url', '')
        char_count = result.get('char_count', 0)
        success = result.get('success', True)
        
        # Get the actual content from the result
        content = ""
        if 'content' in result:
            content = result['content']
        elif 'text' in result:
            content = result['text']
        
        icon = "✅" if success else "❌"
        
        with st.expander(f"{icon} {title[:80]}{'...' if len(title) > 80 else ''}", expanded=False):
            if success:
                st.success(f"✅ Successfully scraped {char_count:,} characters")
                
                if url:
                    st.markdown(f"**🌐 Source:** [{url}]({url})")
                
                # Show content preview
                if content:
                    preview_content = content[:500] + "..." if len(content) > 500 else content
                    st.markdown("**📄 Content Preview:**")
                    unique_scraped_key = f"scraped_preview_{hash(url)}_{int(time.time() * 1000000)}"
                    st.text_area("Content Preview", preview_content, height=150, disabled=True, key=unique_scraped_key, label_visibility="collapsed")
                else:
                    st.warning("⚠️ No content preview available")
                
                st.info("✨ Full content was extracted and analyzed by the AI")
            else:
                error = result.get('error', 'Unknown error')
                st.error(f"❌ Failed to scrape: {error}")
                
                if url:
                    st.markdown(f"**🌐 Source:** [{url}]({url})")
            
            st.markdown("---")
    
    def render_chat_history(self, messages: List[Dict[str, Any]]):
        """Render chat history with proper formatting.
        
        Args:
            messages: List of message dictionaries
        """
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display steps if they exist
                if message["role"] == "assistant" and "steps" in message:
                    steps_text = self.display_steps_container(message["steps"])
                    if steps_text:
                        st.markdown(steps_text)
                
                # Display tool results if they exist
                if message["role"] == "assistant" and "tool_results" in message:
                    tool_results = message["tool_results"]
                    if tool_results:
                        for result in tool_results:
                            self.display_tool_result_dropdown(result)
                
                # Display context expander for previous messages
                if message["role"] == "assistant" and "context" in message and message["context"]:
                    tool_results = message.get("tool_results", [])
                    self.render_context_expander(
                        message["context"], 
                        tool_results, 
                        "Previous analysis of search results and tool outputs."
                    )
                
                # Display paper links for previous messages
                if message["role"] == "assistant" and "paper_metadata" in message and message["paper_metadata"]:
                    self.render_paper_metadata(message["paper_metadata"])
    
    def get_chat_input_placeholder(self) -> str:
        """Get placeholder text for chat input."""
        return "Ask me anything - research questions, current events, calculations, or general knowledge!"
    
    def render_error_message(self, error: Exception) -> str:
        """Generate error message HTML.
        
        Args:
            error: Exception that occurred
            
        Returns:
            Formatted error message
        """
        return f"🚨 Agentic system error: {str(error)}"
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
