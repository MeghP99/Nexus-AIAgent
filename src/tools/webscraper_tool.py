"""Web scraping tool for extracting content from URLs."""

from typing import Dict, Any, List
import time
from urllib.parse import urlparse, urljoin

from .base_tool import BaseTool


class WebScraperTool(BaseTool):
    """Tool for scraping and extracting content from web URLs."""
    
    def __init__(self):
        """Initialize web scraper tool."""
        super().__init__()
    
    def _get_name(self) -> str:
        """Get the tool name."""
        return "webscraper"
    
    def _get_description(self) -> str:
        """Get the tool description."""
        return "Extract full text content from web pages given their URLs. Useful for getting detailed information from specific websites."
    
    def _check_availability(self) -> bool:
        """Check if required dependencies are available."""
        try:
            import requests
            import bs4
            return True
        except ImportError as e:
            print(f"[WebScraperTool] Warning: Required dependencies not available: {e}")
            print("[WebScraperTool] Please install: pip install requests beautifulsoup4")
            return False
    
    def execute(self, query: str, max_chars: int = 3000) -> Dict[str, Any]:
        """Execute web scraping on provided URLs.
        
        Args:
            query: URL or comma-separated URLs to scrape
            max_chars: Maximum characters per URL to return
            
        Returns:
            Dict containing scraped content and metadata
        """
        if not self.available:
            return {
                "success": False,
                "message": "Web scraper not available - missing dependencies",
                "results": [],
                "metadata": []
            }
        
        # Parse URLs from query
        urls = self._parse_urls(query)
        
        print(f"[WebScraperTool] Parsed {len(urls)} URLs from query: {query[:100]}...")
        for i, url in enumerate(urls, 1):
            print(f"[WebScraperTool]   {i}. {url}")
        
        if not urls:
            return {
                "success": False,
                "message": "No valid URLs found in query",
                "results": [],
                "metadata": []
            }
        
        results = []
        metadata = []
        
        for url in urls[:3]:  # Limit to 3 URLs to avoid long delays
            try:
                content = self._scrape_url(url, max_chars)
                
                if content:
                    results.append({
                        "title": content.get("title", "Web Page"),
                        "url": url,
                        "content": content.get("text", ""),
                        "source": "webscraper"
                    })
                    
                    metadata.append({
                        "title": content.get("title", "Web Page")[:100],
                        "url": url,
                        "source": "webscraper",
                        "content_type": "scraped_web",
                        "char_count": len(content.get("text", "")),
                        "content": content.get("text", ""),  # Include the actual content
                        "success": True
                    })
                else:
                    metadata.append({
                        "title": f"Failed: {url}",
                        "url": url,
                        "source": "webscraper",
                        "content_type": "scraped_web",
                        "char_count": 0,
                        "content": "",  # Empty content for failed scrapes
                        "success": False
                    })
                
                # Be respectful with delays
                time.sleep(1)
                
            except Exception as e:
                error_type = type(e).__name__
                error_msg = str(e)
                
                # Provide more helpful error messages
                helpful_msg = error_msg
                if "timeout" in error_msg.lower():
                    helpful_msg = "Request timeout - site may be slow or blocking requests"
                elif "403" in error_msg or "forbidden" in error_msg.lower():
                    helpful_msg = "Access forbidden - site may be blocking scrapers"
                elif "404" in error_msg:
                    helpful_msg = "Page not found"
                elif "connection" in error_msg.lower():
                    helpful_msg = "Connection failed - site may be down or unreachable"
                elif "ssl" in error_msg.lower() or "certificate" in error_msg.lower():
                    helpful_msg = "SSL/Certificate error"
                
                print(f"[WebScraperTool] Error scraping {url}: {helpful_msg} ({error_type})")
                
                metadata.append({
                    "title": f"Failed: {urlparse(url).netloc}",
                    "url": url,
                    "source": "webscraper",
                    "content_type": "scraped_web",
                    "char_count": 0,
                    "content": f"Scraping failed: {helpful_msg}",
                    "error": helpful_msg,
                    "error_type": error_type,
                    "success": False
                })
        
        success_count = len([r for r in results if r])
        
        return {
            "success": success_count > 0,
            "message": f"Successfully scraped {success_count}/{len(urls)} URLs",
            "results": results,
            "metadata": metadata
        }
    
    def _parse_urls(self, query: str) -> List[str]:
        """Parse URLs from query string.
        
        Args:
            query: String that may contain URLs
            
        Returns:
            List of valid URLs
        """
        import re
        
        # Split by common separators
        parts = re.split(r'[,\s\n]+', query.strip())
        
        urls = []
        for part in parts:
            part = part.strip()
            
            # Clean up URL (remove quotes, commas, and other artifacts)
            part = part.strip('"').strip("'").strip(',')
            part = re.sub(r'["\',]+$', '', part)
            
            # Check if it looks like a URL
            if part.startswith(('http://', 'https://')):
                # Validate URL format
                if self._is_valid_url(part):
                    urls.append(part)
                else:
                    print(f"[WebScraperTool] Skipping malformed URL: {part}")
            elif '.' in part and not part.startswith('.'):
                # Try adding https://
                candidate_url = f"https://{part}"
                if self._is_valid_url(candidate_url):
                    urls.append(candidate_url)
        
        return urls
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if a URL is valid.
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL appears valid, False otherwise
        """
        import re
        
        # Basic URL validation
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(url_pattern, url))
    
    def _scrape_url(self, url: str, max_chars: int) -> Dict[str, str]:
        """Scrape content from a single URL.
        
        Args:
            url: URL to scrape
            max_chars: Maximum characters to return
            
        Returns:
            Dict with title and text content
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            
            # Set realistic headers to avoid bot detection
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }
            
            print(f"[WebScraperTool] Scraping: {url}")
            
            response = requests.get(url, timeout=15, headers=headers)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "Unknown Title"
            
            # Remove unwanted elements more comprehensively
            unwanted_selectors = [
                "script", "style", "nav", "header", "footer", "aside", 
                "advertisement", ".ad", ".ads", ".advertisement", 
                ".cookie", ".popup", ".modal", ".overlay",
                "[class*='ad-']", "[id*='ad-']", "[class*='advertisement']",
                ".social-share", ".comments", ".comment-section"
            ]
            
            for selector in unwanted_selectors:
                for element in soup.select(selector):
                    element.decompose()
            
            # Try multiple strategies to find main content
            main_content = None
            content_strategies = [
                # Semantic HTML5 elements
                'main', 'article', '[role="main"]',
                # Common content class patterns
                '.content', '.main-content', '.post-content', '.article-content',
                '.entry-content', '.page-content', '.body-content',
                # Common ID patterns
                '#content', '#main-content', '#post-content', '#article-content',
                # Specific to analytics/stats sites
                '.stats', '.data', '.table', '.chart-container',
                # Generic containers
                '.container .row', '.wrapper', '.page-wrapper',
                # Fallback to body paragraphs
                'body p', 'body div'
            ]
            
            extracted_text = ""
            strategy_used = "none"
            
            for strategy in content_strategies:
                elements = soup.select(strategy)
                if elements:
                    # Try to get the largest text content
                    candidate_text = ""
                    for element in elements:
                        element_text = element.get_text(separator=' ', strip=True)
                        if len(element_text) > len(candidate_text):
                            candidate_text = element_text
                    
                    if len(candidate_text) > len(extracted_text):
                        extracted_text = candidate_text
                        strategy_used = strategy
                        
                    # If we found substantial content, stop trying
                    if len(extracted_text) > 200:
                        break
            
            # Final fallback - get all text from body
            if len(extracted_text) < 100:
                body = soup.find('body')
                if body:
                    extracted_text = body.get_text(separator=' ', strip=True)
                    strategy_used = "body_fallback"
                else:
                    # Last resort - entire document
                    extracted_text = soup.get_text(separator=' ', strip=True)
                    strategy_used = "full_document"
            
            text = extracted_text
            
            # Clean up whitespace and remove excessive spacing
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Remove any remaining HTML entities and special characters
            import html
            clean_text = html.unescape(clean_text)
            
            # Remove excessive whitespace and normalize
            clean_text = ' '.join(clean_text.split())
            
            # Truncate if needed
            if len(clean_text) > max_chars:
                clean_text = clean_text[:max_chars] + "..."
            
            # Detect potential issues and provide helpful feedback
            extraction_info = f"[WebScraperTool] Extracted {len(clean_text)} characters from {url}"
            if strategy_used:
                extraction_info += f" (strategy: {strategy_used})"
            
            # Check for JavaScript-heavy sites
            if len(clean_text) < 50:
                js_indicators = [
                    'javascript', 'js-', 'data-react', 'ng-app', 'vue-app',
                    'ember-app', 'angular', 'react', 'vue', 'svelte'
                ]
                
                page_html = str(soup).lower()
                js_detected = any(indicator in page_html for indicator in js_indicators)
                
                if js_detected:
                    extraction_info += " ⚠️  JavaScript-heavy site detected - content may be dynamically loaded"
                    clean_text += "\n\n[NOTE: This appears to be a JavaScript-heavy site. Some content may not be accessible through static scraping.]"
                else:
                    extraction_info += " ⚠️  Very little content extracted - site may have anti-scraping measures"
            
            print(extraction_info)
            
            return {
                "title": title,
                "text": clean_text,
                "url": url,
                "strategy_used": strategy_used,
                "char_count": len(clean_text)
            }
            
        except requests.exceptions.RequestException as e:
            # Try alternative approaches for failed requests
            print(f"[WebScraperTool] Primary scraping failed for {url}: {e}")
            
            # For JavaScript-heavy sites, try to extract whatever static content is available
            try:
                import requests
                from bs4 import BeautifulSoup
                
                # Try with minimal headers to see if we can get basic content
                minimal_headers = {'User-Agent': 'curl/7.68.0'}
                response = requests.get(url, timeout=10, headers=minimal_headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Just get basic meta information and any visible text
                    title_tag = soup.find('title')
                    title = title_tag.get_text().strip() if title_tag else "Unknown Title"
                    
                    # Get meta description as fallback content
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    fallback_content = ""
                    
                    if meta_desc and meta_desc.get('content'):
                        fallback_content = meta_desc.get('content').strip()
                    
                    # Add any visible static text
                    body = soup.find('body')
                    if body:
                        static_text = body.get_text(separator=' ', strip=True)
                        # Only use if we got some reasonable content
                        if len(static_text) > len(fallback_content):
                            fallback_content = static_text[:500]
                    
                    if fallback_content:
                        fallback_content += "\n\n[NOTE: Limited content extracted - site may require JavaScript for full content.]"
                        print(f"[WebScraperTool] Fallback extraction: {len(fallback_content)} characters")
                        
                        return {
                            "title": title + " (Limited)",
                            "text": fallback_content,
                            "url": url,
                            "strategy_used": "fallback_minimal",
                            "char_count": len(fallback_content)
                        }
            
            except Exception as fallback_error:
                print(f"[WebScraperTool] Fallback also failed: {fallback_error}")
            
            # If all else fails, re-raise the original exception
            raise e
        
        except Exception as e:
            print(f"[WebScraperTool] Failed to scrape {url}: {e}")
            raise e
