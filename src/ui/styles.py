"""CSS styles and theme management for the Streamlit UI."""

import streamlit as st


class StyleManager:
    """Manages CSS styles and themes for the application."""
    
    @staticmethod
    def apply_custom_styles():
        """Apply custom CSS styles to the Streamlit app."""
        st.markdown("""
        <style>
            .step-container {
                background-color: #f0f2f6;
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .step-item {
                display: flex;
                align-items: center;
                margin: 10px 0;
                padding: 10px 15px;
                background-color: white;
                border-radius: 8px;
                border-left: 4px solid #1f77b4;
                transition: all 0.3s ease;
            }
            .step-item.searching { border-left-color: #1f77b4; }
            .step-item.found { border-left-color: #2ca02c; }
            .step-item.not_found { border-left-color: #d62728; }
            .step-item.error { border-left-color: #ff7f0e; }
            .step-item.checking { border-left-color: #9467bd; }
            .step-item.synthesizing { border-left-color: #8c564b; }
            .step-item.completed { border-left-color: #2ca02c; }
            .step-item.insufficient { border-left-color: #ff7f0e; }
            
            .step-message {
                margin-left: 10px;
                font-size: 14px;
                color: #333;
            }
            .paper-list {
                margin-left: 30px;
                font-size: 13px;
                color: #666;
                line-height: 1.6;
            }
            
            .paper-card {
                background-color: #f0f2f6;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 10px;
                border-left: 4px solid #1f77b4;
            }
            
            .paper-title {
                margin-top: 0;
                color: #1f77b4;
                font-weight: bold;
            }
            
            .paper-authors {
                margin: 5px 0;
                color: #555;
            }
            
            .paper-published {
                margin: 5px 0;
                color: #666;
            }
            
            .paper-link {
                color: #1f77b4;
                text-decoration: none;
            }
            
            .tool-status {
                padding: 10px;
                border-radius: 5px;
                margin: 5px 0;
            }
            
            .tool-status.success {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .tool-status.error {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .tool-status.warning {
                background-color: #fff3cd;
                color: #856404;
                border: 1px solid #ffeaa7;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def get_step_item_class(status: str) -> str:
        """Get CSS class for step item based on status.
        
        Args:
            status: Status string
            
        Returns:
            CSS class name
        """
        status_map = {
            "searching": "searching",
            "found": "found",
            "not_found": "not_found",
            "error": "error",
            "checking": "checking",
            "synthesizing": "synthesizing",
            "completed": "completed",
            "insufficient": "insufficient"
        }
        return status_map.get(status, "searching")
    
    @staticmethod
    def get_paper_card_html(paper: dict) -> str:
        """Generate HTML for a paper card.
        
        Args:
            paper: Paper metadata dictionary
            
        Returns:
            HTML string for the paper card
        """
        title = paper.get('title', 'Unknown Title')
        authors = paper.get('authors', 'Unknown Authors')
        published = paper.get('published', 'Unknown Date')
        url = paper.get('url', '#')
        
        # Truncate long titles and authors
        display_title = title[:100] + '...' if len(title) > 100 else title
        display_authors = authors[:100] + '...' if len(authors) > 100 else authors
        
        return f"""
        <div class="paper-card">
            <h4 class="paper-title">{display_title}</h4>
            <p class="paper-authors"><b>Authors:</b> {display_authors}</p>
            <p class="paper-published"><b>Published:</b> {published}</p>
            <a href="{url}" target="_blank" class="paper-link">
                🔗 View on ArXiv
            </a>
        </div>
        """
