import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
from collections import deque
from typing import Set, List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLFrontier:
    """Manages the URL queue and visited URLs"""
    
    def __init__(self):
        self.queue = deque()
        self.visited = set()
    
    def add(self, url: str):
        """Add URL to queue if not visited"""
        if url not in self.visited:
            self.queue.append(url)
            self.visited.add(url)
    
    def has_next(self) -> bool:
        """Check if queue has URLs"""
        return len(self.queue) > 0
    
    def get_next(self) -> Optional[str]:
        """Get next URL from queue (FIFO - BFS)"""
        if self.has_next():
            return self.queue.popleft()
        return None


class HTMLParser:
    """Extracts title, text, and links from HTML"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
    
    def parse(self, html: str) -> Dict:
        """Parse HTML and extract content"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else "No title"
            
            # Extract text content
            text = self._extract_text(soup)
            
            # Extract internal links
            links = self._extract_links(soup)
            
            return {
                'title': title,
                'text': text,
                'links': links
            }
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return {'title': '', 'text': '', 'links': []}
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract and clean text from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text
    
    def _extract_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract only internal links"""
        links = []
        for link in soup.find_all('a', href=True):
            url = link['href']
            # Convert relative URLs to absolute
            absolute_url = urljoin(self.base_url, url)
            
            # Remove fragments
            absolute_url = absolute_url.split('#')[0]
            
            # Keep only internal links (same domain)
            if self._is_internal_link(absolute_url):
                links.append(absolute_url)
        
        return list(set(links))  # Remove duplicates
    
    def _is_internal_link(self, url: str) -> bool:
        """Check if URL is internal (same domain)"""
        try:
            parsed = urlparse(url)
            return parsed.netloc == self.domain
        except:
            return False


class WebCrawler:
    """Main crawler engine"""
    
    def __init__(self, seed_url: str, max_pages: int = 100, delay: float = 2.0):
        """
        Initialize crawler
        
        Args:
            seed_url: Starting URL (e.g., http://quotes.toscrape.com)
            max_pages: Maximum pages to crawl
            delay: Delay between requests (in seconds)
        """
        self.seed_url = seed_url
        self.max_pages = max_pages
        self.delay = delay
        self.frontier = URLFrontier()
        self.parser = HTMLParser(seed_url)
        self.crawled_pages = []
        
        # Headers to mimic a browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def crawl(self) -> List[Dict]:
        """Start crawling"""
        self.frontier.add(self.seed_url)
        page_count = 0
        
        while self.frontier.has_next() and page_count < self.max_pages:
            url = self.frontier.get_next()
            
            try:
                logger.info(f"Crawling ({page_count + 1}/{self.max_pages}): {url}")
                
                # Fetch page
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # Parse page
                parsed = self.parser.parse(response.text)
                
                # Store page data
                page_data = {
                    'url': url,
                    'title': parsed['title'],
                    'text': parsed['text'],
                }
                self.crawled_pages.append(page_data)
                
                # Add new links to frontier
                for link in parsed['links']:
                    self.frontier.add(link)
                
                page_count += 1
                
                # Politeness delay
                time.sleep(self.delay)
                
            except requests.RequestException as e:
                logger.error(f"Error fetching {url}: {e}")
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
        
        logger.info(f"Crawling complete! Total pages: {len(self.crawled_pages)}")
        return self.crawled_pages
    
    def save_to_json(self, filepath: str):
        """Save crawled data to JSON"""
        with open(filepath, 'w') as f:
            json.dump(self.crawled_pages, f, indent=2)
        logger.info(f"Data saved to {filepath}")


if __name__ == "__main__":
    # Example usage
    crawler = WebCrawler(
        seed_url="http://quotes.toscrape.com",
        max_pages=20,
        delay=2
    )
    pages = crawler.crawl()
    crawler.save_to_json("crawled_data.json")
