"""Enhanced news collection with multiple sources: NewsAPI, RSS, Reddit."""

import os
import time
import feedparser
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config import Config


class NewsAPICollector:
    """Collect news from NewsAPI.org."""
    
    def __init__(self):
        """Initialize NewsAPI collector."""
        self.api_key = Config.NEWSAPI_KEY if hasattr(Config, 'NEWSAPI_KEY') else None
        self.base_url = "https://newsapi.org/v2"
    
    def collect(self, category: str, language: str = 'en', max_results: int = 10) -> List[Dict]:
        """
        Collect news from NewsAPI.
        
        Args:
            category: Category (sports, business, technology, etc.)
            language: Language code (en, pt, es, fr, de)
            max_results: Maximum number of articles
        """
        if not self.api_key:
            print("⚠️  NewsAPI key not configured")
            return []
        
        # Map categories to NewsAPI categories
        category_map = {
            'sports': 'sports',
            'politics': 'general',
            'finance': 'business',
            'technology': 'technology',
            'health': 'health',
            'science': 'science',
            'entertainment': 'entertainment'
        }
        
        newsapi_category = category_map.get(category, 'general')
        
        try:
            print(f"📰 Fetching from NewsAPI: {category}")
            
            response = requests.get(
                f"{self.base_url}/top-headlines",
                params={
                    'apiKey': self.api_key,
                    'category': newsapi_category,
                    'language': language,
                    'pageSize': max_results
                },
                timeout=10
            )
            
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'ok':
                print(f"❌ NewsAPI error: {data.get('message', 'Unknown error')}")
                return []
            
            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', ''),
                    'content': article.get('content', article.get('description', '')),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'NewsAPI'),
                    'published_at': article.get('publishedAt', ''),
                    'category': category,
                    'collected_at': datetime.now().isoformat()
                })
            
            print(f"✓ Collected {len(articles)} articles from NewsAPI")
            return articles
            
        except Exception as e:
            print(f"❌ NewsAPI error: {str(e)}")
            return []


class RSSFeedCollector:
    """Collect news from RSS feeds."""
    
    # Popular RSS feeds by category
    RSS_FEEDS = {
        'sports': [
            'http://rss.cnn.com/rss/edition_sport.rss',
            'https://www.espn.com/espn/rss/news',
            'https://sports.yahoo.com/rss/',
        ],
        'politics': [
            'http://rss.cnn.com/rss/edition_world.rss',
            'https://feeds.bbci.co.uk/news/world/rss.xml',
            'https://www.politico.com/rss/politics08.xml',
        ],
        'finance': [
            'https://feeds.finance.yahoo.com/rss/2.0/headline',
            'https://www.cnbc.com/id/100003114/device/rss/rss.html',
            'https://www.bloomberg.com/feed/podcast/etf-report.xml',
        ],
        'technology': [
            'http://rss.cnn.com/rss/edition_technology.rss',
            'https://www.theverge.com/rss/index.xml',
            'https://techcrunch.com/feed/',
        ],
        'health': [
            'http://rss.cnn.com/rss/edition_health.rss',
            'https://feeds.bbci.co.uk/news/health/rss.xml',
        ],
    }
    
    def collect(self, category: str, max_per_feed: int = 5) -> List[Dict]:
        """
        Collect news from RSS feeds.
        
        Args:
            category: News category
            max_per_feed: Maximum articles per feed
        """
        feeds = self.RSS_FEEDS.get(category, [])
        
        if not feeds:
            print(f"⚠️  No RSS feeds configured for {category}")
            return []
        
        articles = []
        
        for feed_url in feeds:
            try:
                print(f"📡 Fetching RSS: {feed_url}")
                
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:max_per_feed]:
                    articles.append({
                        'title': entry.get('title', ''),
                        'content': entry.get('summary', entry.get('description', '')),
                        'url': entry.get('link', ''),
                        'source': feed.feed.get('title', 'RSS Feed'),
                        'published_at': entry.get('published', ''),
                        'category': category,
                        'collected_at': datetime.now().isoformat()
                    })
                
                time.sleep(1)  # Be nice to servers
                
            except Exception as e:
                print(f"❌ RSS error for {feed_url}: {str(e)}")
                continue
        
        print(f"✓ Collected {len(articles)} articles from RSS feeds")
        return articles


class RedditCollector:
    """Collect trending topics from Reddit."""
    
    SUBREDDITS = {
        'sports': ['sports', 'nba', 'nfl', 'soccer', 'formula1'],
        'politics': ['worldnews', 'politics', 'geopolitics'],
        'finance': ['investing', 'stocks', 'cryptocurrency', 'wallstreetbets'],
        'technology': ['technology', 'programming', 'artificial', 'gadgets'],
        'gaming': ['gaming', 'Games'],
    }
    
    def collect(self, category: str, max_posts: int = 10) -> List[Dict]:
        """
        Collect hot posts from Reddit.
        
        Args:
            category: Category
            max_posts: Maximum posts to collect
        """
        subreddits = self.SUBREDDITS.get(category, [])
        
        if not subreddits:
            print(f"⚠️  No subreddits configured for {category}")
            return []
        
        articles = []
        
        for subreddit in subreddits[:2]:  # Limit to 2 subreddits
            try:
                print(f"🔴 Fetching from r/{subreddit}")
                
                # Use Reddit JSON API (no auth required for public posts)
                response = requests.get(
                    f"https://www.reddit.com/r/{subreddit}/hot.json",
                    headers={'User-Agent': 'Mozilla/5.0'},
                    params={'limit': max_posts},
                    timeout=10
                )
                
                response.raise_for_status()
                data = response.json()
                
                for post in data['data']['children']:
                    post_data = post['data']
                    
                    # Skip pinned posts
                    if post_data.get('stickied'):
                        continue
                    
                    articles.append({
                        'title': post_data.get('title', ''),
                        'content': post_data.get('selftext', '')[:1000],  # Limit length
                        'url': f"https://www.reddit.com{post_data.get('permalink', '')}",
                        'source': f"r/{subreddit}",
                        'published_at': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                        'category': category,
                        'score': post_data.get('score', 0),
                        'collected_at': datetime.now().isoformat()
                    })
                
                time.sleep(2)  # Reddit rate limiting
                
            except Exception as e:
                print(f"❌ Reddit error for r/{subreddit}: {str(e)}")
                continue
        
        # Sort by score (upvotes)
        articles.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        print(f"✓ Collected {len(articles)} posts from Reddit")
        return articles[:max_posts]


class EnhancedNewsCollector:
    """Enhanced collector that aggregates from multiple sources."""
    
    def __init__(self):
        """Initialize all collectors."""
        self.newsapi = NewsAPICollector()
        self.rss = RSSFeedCollector()
        self.reddit = RedditCollector()
    
    def collect_from_all_sources(
        self, 
        category: str, 
        language: str = 'en',
        use_newsapi: bool = True,
        use_rss: bool = True,
        use_reddit: bool = False
    ) -> List[Dict]:
        """
        Collect news from all enabled sources.
        
        Args:
            category: News category
            language: Language code
            use_newsapi: Use NewsAPI
            use_rss: Use RSS feeds
            use_reddit: Use Reddit
        """
        all_articles = []
        
        if use_newsapi:
            articles = self.newsapi.collect(category, language=language, max_results=5)
            all_articles.extend(articles)
        
        if use_rss:
            articles = self.rss.collect(category, max_per_feed=3)
            all_articles.extend(articles)
        
        if use_reddit:
            articles = self.reddit.collect(category, max_posts=5)
            all_articles.extend(articles)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_articles = []
        
        for article in all_articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        print(f"\n📊 Total unique articles collected: {len(unique_articles)}")
        
        return unique_articles

