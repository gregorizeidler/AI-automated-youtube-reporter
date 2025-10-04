"""News collection module using Google Search and content extraction."""

import re
import time
from typing import List, Dict
from datetime import datetime, timedelta
from urllib.parse import urlparse, unquote
import requests
from googlesearch import search
from config import Config


class NewsCollector:
    """Collects news from Google Search and extracts full content."""
    
    def __init__(self):
        """Initialize the news collector."""
        # Define search queries for each category
        self.search_queries = {
            "sports": [
                "latest sports news",
                "breaking sports",
                "championship tournament",
                "sports highlights today"
            ],
            "politics": [
                "breaking political news",
                "election news",
                "government policy",
                "political developments"
            ],
            "finance": [
                "stock market news",
                "economy news",
                "financial markets",
                "business news today"
            ]
        }
        
        # Domains to ignore (social media, etc)
        self.ignored_domains = [
            'facebook.com', 'twitter.com', 'instagram.com',
            'youtube.com', 'linkedin.com', 'tiktok.com',
            'reddit.com', 'pinterest.com'
        ]
    
    def search_news(self, query: str, num_results: int = 10, days_back: int = 1) -> List[str]:
        """
        Search for news using Google Search.
        
        Args:
            query: Search query
            num_results: Number of results to retrieve
            days_back: How many days back to search
            
        Returns:
            List of URLs
        """
        today = datetime.now().date()
        date_from = today - timedelta(days=days_back)
        
        print(f"Searching news from last {days_back} day(s) for '{query}'...")
        
        results = []
        try:
            # Add "after:" to limit by date
            query_with_date = f"{query} after:{date_from.strftime('%Y-%m-%d')}"
            
            # Use googlesearch-python library
            for url in search(query_with_date, num_results=num_results, lang="en"):
                # Filter out social media and non-news sites
                if not any(domain in url for domain in self.ignored_domains):
                    results.append(url)
                    print(f"  Found: {url}")
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
            
            return results
        except Exception as e:
            print(f"Error searching '{query}': {e}")
            return []
    
    def extract_page_content(self, url: str) -> Dict[str, str]:
        """
        Extract full content from a news page.
        
        Args:
            url: URL of the news article
            
        Returns:
            Dictionary with 'title', 'content', 'url'
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            
            # Increase timeout for slower sites
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            html = response.text
            
            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else self._extract_title_from_url(url)
            
            # Clean title (remove site name suffixes)
            title = re.sub(r'\s*[-|]\s*[^-|]+$', '', title).strip()
            
            # Step 1: Clean HTML of non-relevant elements
            html_clean = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
            html_clean = re.sub(r'<style[^>]*>.*?</style>', ' ', html_clean, flags=re.DOTALL | re.IGNORECASE)
            html_clean = re.sub(r'<!--.*?-->', ' ', html_clean, flags=re.DOTALL)
            html_clean = re.sub(r'<nav[^>]*>.*?</nav>', ' ', html_clean, flags=re.DOTALL | re.IGNORECASE)
            html_clean = re.sub(r'<header[^>]*>.*?</header>', ' ', html_clean, flags=re.DOTALL | re.IGNORECASE)
            html_clean = re.sub(r'<footer[^>]*>.*?</footer>', ' ', html_clean, flags=re.DOTALL | re.IGNORECASE)
            html_clean = re.sub(r'<aside[^>]*>.*?</aside>', ' ', html_clean, flags=re.DOTALL | re.IGNORECASE)
            html_clean = re.sub(r'<iframe[^>]*>.*?</iframe>', ' ', html_clean, flags=re.DOTALL | re.IGNORECASE)
            
            # Step 2: Try to identify main content
            content = ""
            
            # Patterns to find main content in news sites
            content_patterns = [
                r'<article[^>]*>(.*?)</article>',
                r'<div[^>]*class="[^"]*(?:content|article|post|news|story|text|entry|body|main)[^"]*"[^>]*>(.*?)</div>',
                r'<div[^>]*id="[^"]*(?:content|article|post|news|story|text|entry|body|main)[^"]*"[^>]*>(.*?)</div>',
                r'<main[^>]*>(.*?)</main>',
                r'<section[^>]*class="[^"]*(?:content|article|post|news|story)[^"]*"[^>]*>(.*?)</section>'
            ]
            
            # Try each pattern until finding significant content
            for pattern in content_patterns:
                matches = re.findall(pattern, html_clean, re.DOTALL | re.IGNORECASE)
                
                if matches:
                    for match in matches:
                        if len(match) > 500:  # At least 500 characters
                            content = match
                            break
                    
                    if content:
                        break
            
            # Strategy 2: If no content found by pattern, extract all <p> tags
            if not content or len(content) < 500:
                paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_clean, re.DOTALL | re.IGNORECASE)
                content = ' '.join([p for p in paragraphs if len(p) > 30])
            
            # Step 3: Clean extracted content
            content_clean = re.sub(r'<[^>]+>', ' ', content)
            content_clean = re.sub(r'\s+', ' ', content_clean).strip()
            
            # Convert HTML entities to characters
            content_clean = content_clean.replace('&nbsp;', ' ')
            content_clean = content_clean.replace('&amp;', '&')
            content_clean = content_clean.replace('&lt;', '<')
            content_clean = content_clean.replace('&gt;', '>')
            content_clean = content_clean.replace('&quot;', '"')
            content_clean = content_clean.replace('&#39;', "'")
            content_clean = content_clean.replace('&rsquo;', "'")
            content_clean = content_clean.replace('&lsquo;', "'")
            content_clean = content_clean.replace('&rdquo;', '"')
            content_clean = content_clean.replace('&ldquo;', '"')
            content_clean = content_clean.replace('&mdash;', '—')
            content_clean = content_clean.replace('&ndash;', '–')
            
            # If content is too large, limit size
            if len(content_clean) > 15000:
                content_clean = content_clean[:15000] + "..."
            
            print(f"  Extracted content size: {len(content_clean)} characters")
            
            return {
                "title": title,
                "content": content_clean,
                "url": url
            }
            
        except Exception as e:
            print(f"  Error extracting content from {url}: {e}")
            return {
                "title": self._extract_title_from_url(url),
                "content": "",
                "url": url
            }
    
    def _extract_title_from_url(self, url: str) -> str:
        """Extract title from URL as fallback."""
        parse_result = urlparse(url)
        path = parse_result.path
        
        # Get last segment of URL and replace hyphens with spaces
        title = unquote(path.split('/')[-1].replace('-', ' ').replace('_', ' '))
        
        # Capitalize words
        title = ' '.join(word.capitalize() for word in title.split())
        
        return title if title else "Untitled Article"
    
    def collect_category_news(self, category: str, articles_per_query: int = 3) -> List[Dict]:
        """
        Collect news for a specific category.
        
        Args:
            category: Category to collect (sports, politics, finance)
            articles_per_query: Number of articles per search query
            
        Returns:
            List of article dictionaries with title, content, url
        """
        category = category.strip().lower()
        
        if category not in self.search_queries:
            print(f"Unknown category: {category}")
            return []
        
        all_articles = []
        seen_urls = set()
        
        queries = self.search_queries[category]
        
        for query in queries:
            print(f"\nSearching: {query}")
            
            # Search for news
            urls = self.search_news(query, num_results=articles_per_query, days_back=2)
            
            # Extract content from each URL
            for url in urls:
                if url in seen_urls:
                    continue
                
                seen_urls.add(url)
                
                article = self.extract_page_content(url)
                
                # Only add if we got meaningful content
                if article['content'] and len(article['content']) > 200:
                    article['category'] = category
                    article['collected_at'] = datetime.now().isoformat()
                    all_articles.append(article)
                    print(f"  ✓ Added: {article['title'][:60]}...")
                else:
                    print(f"  ✗ Skipped (insufficient content): {url}")
            
            # Small delay between queries
            time.sleep(2)
            
            # Stop if we have enough articles
            if len(all_articles) >= 5:
                break
        
        print(f"\nCollected {len(all_articles)} articles for {category}")
        return all_articles
    
    def collect_all_categories(self) -> Dict[str, List[Dict]]:
        """
        Collect news from all configured categories.
        
        Returns:
            Dictionary mapping categories to their articles
        """
        all_news = {}
        
        for category in Config.CATEGORIES:
            category = category.strip().lower()
            print(f"\n{'='*60}")
            print(f"COLLECTING NEWS FOR: {category.upper()}")
            print(f"{'='*60}")
            
            articles = self.collect_category_news(category)
            all_news[category] = articles
        
        return all_news
