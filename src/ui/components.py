"""UI components for the Streamlit application."""

import streamlit as st
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
        else:
            st.sidebar.error("❌ Agent initialization failed!")
            st.sidebar.warning("Please check your configuration and environment variables.")
    
    def display_step_message(self, step: Dict[str, str]) -> str:
        """Generate HTML for a single step message.
        
        Args:
            step: Step dictionary with 'status' and 'message' keys
            
        Returns:
            HTML string for the step
        """
        status = step.get("status", "")
        message = step.get("message", "")
        
        if status == "paper_list":
            return f'<div class="paper-list">{message}</div>'
        else:
            css_class = self.style_manager.get_step_item_class(status)
            return f'<div class="step-item {css_class}"><div class="step-message">{message}</div></div>'
    
    def display_steps_container(self, steps: List[Dict[str, str]]) -> str:
        """Generate HTML for all steps in a container.
        
        Args:
            steps: List of step dictionaries
            
        Returns:
            HTML string for the steps container
        """
        if not steps:
            return ""
        
        steps_html = '<div class="step-container">'
        steps_html += '<h4 style="margin-top: 0; color: #333;">🔄 Processing Steps</h4>'
        
        for step in steps:
            steps_html += self.display_step_message(step)
        
        steps_html += '</div>'
        
        return steps_html
    
    def render_context_expander(self, context: List[str]):
        """Render context information in an expander.
        
        Args:
            context: List of context strings
        """
        if not context:
            return
        
        with st.expander("🔍 View Retrieved Context & LLM Reasoning", expanded=False):
            st.markdown("### Retrieved Research Paper Excerpts:")
            for i, context_item in enumerate(context[:5], 1):
                st.markdown(f"**Excerpt {i}:**")
                display_context = context_item[:1000] + "..." if len(context_item) > 1000 else context_item
                st.text(display_context)
                st.markdown("---")
            
            st.markdown(f"**Total context chunks retrieved:** {len(context)}")
            st.markdown("**Note:** The LLM synthesized the above excerpts to generate the response, using ONLY this information without any external knowledge.")
    
    def render_paper_metadata(self, paper_metadata: List[Dict[str, Any]]):
        """Render paper metadata as cards.
        
        Args:
            paper_metadata: List of paper metadata dictionaries
        """
        if not paper_metadata:
            return
        
        st.markdown("### 📚 Referenced Papers")
        
        # Create columns for paper cards
        cols = st.columns(min(len(paper_metadata), 3))
        
        for idx, paper in enumerate(paper_metadata):
            col_idx = idx % 3
            with cols[col_idx]:
                paper_html = self.style_manager.get_paper_card_html(paper)
                st.markdown(paper_html, unsafe_allow_html=True)
    
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
                    steps_html = self.display_steps_container(message["steps"])
                    if steps_html:
                        st.markdown(steps_html, unsafe_allow_html=True)
                
                # Display context expander for previous messages
                if message["role"] == "assistant" and "context" in message and message["context"]:
                    self.render_context_expander(message["context"])
                
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
