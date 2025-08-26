"""
Agentic Research Assistant - Main Streamlit Application

A modern, intelligent research assistant that automatically selects the best tools
to answer user questions using ArXiv papers, web search, calculations, and more.
"""

import nest_asyncio
# Apply the patch for asyncio - MUST be before any imports that use asyncio
nest_asyncio.apply()

import streamlit as st
import logging
from dotenv import load_dotenv

from src.agent import ResearchAgent
from src.ui import UIComponents

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgenticResearchApp:
    """Main application class for the Agentic Research Assistant."""
    
    def __init__(self):
        """Initialize the application."""
        self.ui = UIComponents()
        self.agent = None
        self._initialize_app()
    
    def _initialize_app(self):
        """Initialize the Streamlit app configuration."""
        self.ui.setup_page_config()
        self.ui.initialize_session_state()
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the research agent."""
        try:
            self.agent = ResearchAgent()
            logger.info("✅ Research agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize research agent: {e}")
            self.agent = None
    
    def run(self):
        """Run the main application."""
        # Render header
        col1, col2 = self.ui.render_header()
        
        # Render agent status in sidebar
        self.ui.render_agent_status(self.agent)
        
        # Render chat history
        self.ui.render_chat_history(st.session_state.messages)
        
        # Handle chat input
        self._handle_chat_input()
    
    def _handle_chat_input(self):
        """Handle user input and generate responses."""
        prompt = st.chat_input(self.ui.get_chat_input_placeholder())
        
        if prompt:
            if not self.agent:
                st.error("❌ Research agent not available. Please check your configuration.")
                return
            
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                self._generate_assistant_response(prompt)
    
    def _generate_assistant_response(self, prompt: str):
        """Generate and display assistant response with real-time step updates.
        
        Args:
            prompt: User's input prompt
        """
        # Create placeholders for real-time updates
        steps_placeholder = st.empty()
        message_placeholder = st.empty()
        
        # Track accumulated steps for real-time display
        accumulated_steps = []
        
        try:
            # Execute the research process with streaming
            for update in self.agent.research_stream(prompt):
                if update["type"] == "step":
                    # Add step to accumulated list
                    step = update["step"]
                    accumulated_steps.append(step)
                    
                    # Update steps display in real-time
                    steps_html = self.ui.display_steps_container(accumulated_steps)
                    steps_placeholder.markdown(steps_html, unsafe_allow_html=True)
                    
                elif update["type"] == "final":
                    # Extract final results
                    research_result = update["result"]
                    final_response = research_result.get("final_response", 
                                                        "Sorry, I couldn't find an answer to your query.")
                    retrieved_context = research_result.get("context", [])
                    paper_metadata = research_result.get("paper_metadata", [])
                    step_messages = research_result.get("step_messages", [])
                    
                    # Display the main response
                    message_placeholder.markdown(final_response)
                    
                    # Display context and paper metadata
                    self.ui.render_context_expander(retrieved_context)
                    self.ui.render_paper_metadata(paper_metadata)
                    
                    # Store message in session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": final_response,
                        "steps": step_messages,
                        "context": retrieved_context,
                        "paper_metadata": paper_metadata
                    })
                    break
        
        except Exception as e:
            error_message = self.ui.render_error_message(e)
            message_placeholder.markdown(error_message)
            logger.error(f"Error in research process: {e}", exc_info=True)
            
            # Store error message
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_message
            })


def main():
    """Main entry point for the application."""
    try:
        app = AgenticResearchApp()
        app.run()
    except Exception as e:
        st.error(f"Failed to start application: {e}")
        logger.error(f"Application startup failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()