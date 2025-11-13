"""
Social Media Scraper Module

This module handles scraping stock ticker mentions from various social media platforms
including Reddit and Twitter (X). It aggregates mentions and returns the most frequently
mentioned tickers.
"""

import re
from collections import Counter
from typing import List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocialMediaScraper:
    """
    A class to scrape and aggregate stock ticker mentions from social media platforms.
    
    Attributes:
        ticker_pattern (str): Regex pattern to identify stock tickers (e.g., $TSLA)
        excluded_words (set): Common words that might be mistaken for tickers
    """
    
    def __init__(self):
        """Initialize the scraper with ticker pattern and excluded words."""
        self.ticker_pattern = r'\$([A-Z]{1,5})\b'
        self.excluded_words = {
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 
            'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 
            'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WHO', 
            'BOY', 'DID', 'HIS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE',
            'A', 'I'
        }
    
    def get_reddit_mentions(self, subreddits: List[str] = None, limit: int = 100) -> List[str]:
        """
        Scrape Reddit for stock mentions using PRAW.
        
        Args:
            subreddits (List[str]): List of subreddit names to scrape
            limit (int): Maximum number of posts to scrape per subreddit
            
        Returns:
            List[str]: List of ticker symbols found
            
        Note:
            Currently returns demo data. To use real Reddit data:
            1. Install PRAW: pip install praw
            2. Set up Reddit API credentials in .env
            3. Uncomment the real implementation below
        """
        if subreddits is None:
            subreddits = ['wallstreetbets', 'stocks', 'investing']
        
        tickers = []
        
        try:
            # Demo data for testing
            # TODO: Replace with real Reddit API implementation
            demo_posts = [
                "TSLA to the moon! $TSLA looking bullish",
                "What do you think about $AAPL earnings?",
                "$MSFT and $GOOGL are my top picks",
                "AMD stock discussion - $AMD analysis",
                "$NVDA breaking resistance levels",
                "$SPY calls printing money",
                "Discussion on $META and social media stocks",
                "$AMZN showing strong fundamentals",
                "$TSLA breaking out today",
                "$AAPL new iPhone launch impact",
                "Bullish on $NVDA AI chips",
                "$SPY hitting new highs",
                "$MSFT cloud revenue impressive",
                "$GOOGL search dominance continues",
                "$META VR investments paying off",
                "$AMD Ryzen sales strong"
            ]
            
            for post in demo_posts:
                found_tickers = re.findall(self.ticker_pattern, post)
                tickers.extend([
                    ticker for ticker in found_tickers 
                    if ticker not in self.excluded_words
                ])
            
            logger.info(f"Found {len(tickers)} ticker mentions from Reddit")
            
            # Real Reddit implementation (uncomment when API is configured):
            """
            import praw
            import os
            from dotenv import load_dotenv
            
            load_dotenv()
            
            reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent=os.getenv('REDDIT_USER_AGENT')
            )
            
            for subreddit_name in subreddits:
                subreddit = reddit.subreddit(subreddit_name)
                for post in subreddit.hot(limit=limit):
                    # Search in title and selftext
                    text = f"{post.title} {post.selftext}"
                    found_tickers = re.findall(self.ticker_pattern, text)
                    tickers.extend([
                        ticker for ticker in found_tickers 
                        if ticker not in self.excluded_words
                    ])
                    
                    # Also check top comments
                    post.comments.replace_more(limit=0)
                    for comment in post.comments.list()[:10]:
                        found_tickers = re.findall(self.ticker_pattern, comment.body)
                        tickers.extend([
                            ticker for ticker in found_tickers 
                            if ticker not in self.excluded_words
                        ])
            """
                
        except Exception as e:
            logger.error(f"Reddit scraping error: {e}")
        
        return tickers
    
    def get_twitter_mentions(self) -> List[str]:
        """
        Scrape Twitter (X) for stock mentions.
        
        Returns:
            List[str]: List of ticker symbols found
            
        Note:
            Currently returns demo data. To use real Twitter data:
            1. Get Twitter API v2 access
            2. Set up credentials in .env
            3. Implement using tweepy or requests
        """
        tickers = []
        
        try:
            # Demo data for testing
            # TODO: Replace with real Twitter API implementation
            demo_tweets = [
                "$TSLA breaking out of consolidation pattern",
                "Bullish on $AAPL ahead of earnings",
                "$MSFT cloud growth impressive",
                "$NVDA AI narrative strong",
                "$SPY weekly calls looking good",
                "$AMZN e-commerce recovery play",
                "$META social media king",
                "$GOOGL advertising revenue up",
                "$AMD chip sales beating expectations",
                "$TSLA delivery numbers strong"
            ]
            
            for tweet in demo_tweets:
                found_tickers = re.findall(self.ticker_pattern, tweet)
                tickers.extend([
                    ticker for ticker in found_tickers 
                    if ticker not in self.excluded_words
                ])
            
            logger.info(f"Found {len(tickers)} ticker mentions from Twitter")
            
            # Real Twitter implementation (uncomment when API is configured):
            """
            import os
            from dotenv import load_dotenv
            
            load_dotenv()
            
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            # Use tweepy or requests to fetch tweets
            # Example with requests:
            import requests
            
            headers = {'Authorization': f'Bearer {bearer_token}'}
            params = {
                'query': '($AAPL OR $TSLA OR $MSFT OR $GOOGL OR $AMZN) lang:en',
                'max_results': 100,
                'tweet.fields': 'created_at,public_metrics'
            }
            
            response = requests.get(
                'https://api.twitter.com/2/tweets/search/recent',
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                tweets = response.json().get('data', [])
                for tweet in tweets:
                    found_tickers = re.findall(self.ticker_pattern, tweet['text'])
                    tickers.extend([
                        ticker for ticker in found_tickers 
                        if ticker not in self.excluded_words
                    ])
            """
                
        except Exception as e:
            logger.error(f"Twitter scraping error: {e}")
        
        return tickers
    
    def get_stocktwits_mentions(self) -> List[str]:
        """
        Scrape StockTwits for stock mentions (placeholder for future implementation).
        
        Returns:
            List[str]: List of ticker symbols found
        """
        # TODO: Implement StockTwits scraping
        return []
    
    def aggregate_mentions(self, top_n: int = 20) -> List[Tuple[str, int]]:
        """
        Aggregate mentions from all sources and return top mentioned tickers.
        
        Args:
            top_n (int): Number of top tickers to return
            
        Returns:
            List[Tuple[str, int]]: List of (ticker, count) tuples sorted by frequency
        """
        all_tickers = []
        
        # Get mentions from different sources
        logger.info("Aggregating mentions from social media...")
        
        reddit_tickers = self.get_reddit_mentions()
        twitter_tickers = self.get_twitter_mentions()
        
        all_tickers.extend(reddit_tickers)
        all_tickers.extend(twitter_tickers)
        
        # Count mentions and return sorted list
        ticker_counts = Counter(all_tickers)
        most_common = ticker_counts.most_common(top_n)
        
        logger.info(f"Found {len(ticker_counts)} unique tickers, returning top {top_n}")
        
        return most_common
    
    def filter_valid_tickers(self, tickers: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Filter out invalid or fake ticker symbols.
        
        Args:
            tickers (List[Tuple[str, int]]): List of (ticker, count) tuples
            
        Returns:
            List[Tuple[str, int]]: Filtered list of valid tickers
        """
        # Basic validation - could be enhanced with a real ticker database
        valid_tickers = []
        
        for ticker, count in tickers:
            # Basic checks
            if len(ticker) >= 1 and len(ticker) <= 5:
                if ticker.isupper() and ticker.isalpha():
                    valid_tickers.append((ticker, count))
        
        return valid_tickers