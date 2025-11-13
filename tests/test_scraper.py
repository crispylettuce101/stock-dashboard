"""
Unit tests for the SocialMediaScraper class.
"""

import unittest
from src.scraper import SocialMediaScraper


class TestSocialMediaScraper(unittest.TestCase):
    """Test cases for SocialMediaScraper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = SocialMediaScraper()
    
    def test_initialization(self):
        """Test scraper initialization."""
        self.assertIsNotNone(self.scraper.ticker_pattern)
        self.assertIsInstance(self.scraper.excluded_words, set)
        self.assertGreater(len(self.scraper.excluded_words), 0)
    
    def test_reddit_mentions_returns_list(self):
        """Test that get_reddit_mentions returns a list."""
        result = self.scraper.get_reddit_mentions()
        self.assertIsInstance(result, list)
    
    def test_twitter_mentions_returns_list(self):
        """Test that get_twitter_mentions returns a list."""
        result = self.scraper.get_twitter_mentions()
        self.assertIsInstance(result, list)
    
    def test_aggregate_mentions_returns_tuples(self):
        """Test that aggregate_mentions returns list of tuples."""
        result = self.scraper.aggregate_mentions(top_n=5)
        self.assertIsInstance(result, list)
        
        if len(result) > 0:
            self.assertIsInstance(result[0], tuple)
            self.assertEqual(len(result[0]), 2)
            self.assertIsInstance(result[0][0], str)  # ticker
            self.assertIsInstance(result[0][1], int)  # count
    
    def test_aggregate_mentions_top_n(self):
        """Test that aggregate_mentions respects top_n parameter."""
        result = self.scraper.aggregate_mentions(top_n=3)
        self.assertLessEqual(len(result), 3)
    
    def test_filter_valid_tickers(self):
        """Test ticker validation."""
        test_data = [
            ('AAPL', 10),
            ('TSLA', 8),
            ('A', 5),
            ('TOOLONG', 3),
            ('123', 2)
        ]
        
        result = self.scraper.filter_valid_tickers(test_data)
        
        # Should keep AAPL, TSLA, A
        # Should filter out TOOLONG (too long) and 123 (not alpha)
        valid_tickers = [ticker for ticker, _ in result]
        self.assertIn('AAPL', valid_tickers)
        self.assertIn('TSLA', valid_tickers)
        self.assertIn('A', valid_tickers)
        self.assertNotIn('TOOLONG', valid_tickers)
        self.assertNotIn('123', valid_tickers)
    
    def test_excluded_words_filtered(self):
        """Test that excluded words are properly filtered."""
        mentions = self.scraper.aggregate_mentions()
        tickers = [ticker for ticker, _ in mentions]
        
        for ticker in tickers:
            self.assertNotIn(ticker, self.scraper.excluded_words)
    
    def test_aggregate_mentions_sorts_by_count(self):
        """Test that results are sorted by mention count."""
        result = self.scraper.aggregate_mentions()
        
        if len(result) > 1:
            counts = [count for _, count in result]
            # Check if sorted in descending order
            self.assertEqual(counts, sorted(counts, reverse=True))


class TestTickerPatternMatching(unittest.TestCase):
    """Test cases for ticker pattern matching."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = SocialMediaScraper()
    
    def test_ticker_pattern_matches_valid_tickers(self):
        """Test regex pattern matches valid ticker formats."""
        import re
        
        test_strings = [
            "$AAPL is looking good",
            "Bought some $TSLA today",
            "$MSFT earnings beat",
            "Check out $AMD and $NVDA"
        ]
        
        for text in test_strings:
            matches = re.findall(self.scraper.ticker_pattern, text)
            self.assertGreater(len(matches), 0)
    
    def test_ticker_pattern_ignores_invalid_formats(self):
        """Test regex pattern ignores invalid formats."""
        import re
        
        test_strings = [
            "Price is $100",
            "Costs $50.00",
            "No tickers here"
        ]
        
        for text in test_strings:
            matches = re.findall(self.scraper.ticker_pattern, text)
            # Should not match price patterns
            self.assertEqual(len(matches), 0)


if __name__ == '__main__':
    unittest.main()