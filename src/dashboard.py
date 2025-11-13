import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import requests
import re
from collections import Counter
import threading
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import praw
from textblob import TextBlob

class SocialMediaScraper:
    def __init__(self):
        # Common stock ticker patterns
        self.ticker_pattern = r'\$([A-Z]{1,5})\b'
        self.excluded_words = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WHO', 'BOY', 'DID', 'HIS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE'}
    
    def get_reddit_mentions(self, subreddits=['wallstreetbets', 'stocks', 'investing'], limit=100):
        """Scrape Reddit for stock mentions using PRAW (requires Reddit API credentials)"""
        tickers = []
        try:
            # Note: You'll need to set up Reddit API credentials
            # reddit = praw.Reddit(client_id='your_client_id',
            #                     client_secret='your_client_secret',
            #                     user_agent='stock_scraper')
            # 
            # For demo purposes, simulating Reddit data
            demo_posts = [
                "TSLA to the moon! $TSLA looking bullish",
                "What do you think about $AAPL earnings?",
                "$MSFT and $GOOGL are my top picks",
                "AMD stock discussion - $AMD analysis",
                "$NVDA breaking resistance levels",
                "$SPY calls printing money",
                "Discussion on $META and social media stocks",
                "$AMZN showing strong fundamentals"
            ]
            
            for post in demo_posts:
                found_tickers = re.findall(self.ticker_pattern, post)
                tickers.extend([ticker for ticker in found_tickers if ticker not in self.excluded_words])
                
        except Exception as e:
            print(f"Reddit scraping error: {e}")
        
        return tickers
    
    def get_twitter_mentions(self):
        """Simulate Twitter mentions (Twitter API requires authentication)"""
        # Simulated Twitter data for demo
        demo_tweets = [
            "$TSLA breaking out of consolidation pattern",
            "Bullish on $AAPL ahead of earnings",
            "$MSFT cloud growth impressive",
            "$NVDA AI narrative strong",
            "$SPY weekly calls looking good",
            "$AMZN e-commerce recovery play"
        ]
        
        tickers = []
        for tweet in demo_tweets:
            found_tickers = re.findall(self.ticker_pattern, tweet)
            tickers.extend([ticker for ticker in found_tickers if ticker not in self.excluded_words])
        
        return tickers
    
    def aggregate_mentions(self):
        """Aggregate mentions from all sources"""
        all_tickers = []
        
        # Get mentions from different sources
        reddit_tickers = self.get_reddit_mentions()
        twitter_tickers = self.get_twitter_mentions()
        
        all_tickers.extend(reddit_tickers)
        all_tickers.extend(twitter_tickers)
        
        # Count mentions and return sorted list
        ticker_counts = Counter(all_tickers)
        return ticker_counts.most_common(20)

class StockAnalyzer:
    def __init__(self):
        pass
    
    def get_stock_info(self, ticker):
        """Get comprehensive stock information from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1mo")
            
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', current_price)
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
            
            return {
                'symbol': ticker,
                'name': info.get('longName', ticker),
                'current_price': current_price,
                'change': change,
                'change_percent': change_percent,
                'volume': hist['Volume'].iloc[-1],
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'beta': info.get('beta', 'N/A'),
                'day_high': hist['High'].iloc[-1],
                'day_low': hist['Low'].iloc[-1],
                'avg_volume': info.get('averageVolume', 'N/A'),
                'history': hist
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

class StockDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Stock Trading Dashboard")
        self.root.geometry("1400x800")
        
        self.scraper = SocialMediaScraper()
        self.analyzer = StockAnalyzer()
        
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for stock list
        left_frame = ttk.LabelFrame(main_frame, text="Most Mentioned Stocks", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(left_frame, text="Refresh Data", command=self.refresh_data)
        refresh_btn.pack(pady=(0, 10))
        
        # Treeview for stock list
        columns = ('Ticker', 'Mentions', 'Price', 'Change %')
        self.tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_stock_select)
        
        # Right panel for stock details
        right_frame = ttk.LabelFrame(main_frame, text="Stock Details", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Stock info frame
        info_frame = ttk.Frame(right_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Stock name and price labels
        self.stock_name_label = ttk.Label(info_frame, text="Select a stock to view details", font=('Arial', 14, 'bold'))
        self.stock_name_label.pack(anchor=tk.W)
        
        self.price_label = ttk.Label(info_frame, text="", font=('Arial', 12))
        self.price_label.pack(anchor=tk.W)
        
        # Details text widget
        details_frame = ttk.LabelFrame(right_frame, text="Key Metrics", padding="5")
        details_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.details_text = tk.Text(details_frame, height=8, wrap=tk.WORD)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Chart frame
        chart_frame = ttk.LabelFrame(right_frame, text="Price Chart (30 Days)", padding="5")
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def refresh_data(self):
        """Refresh social media mentions and stock data"""
        self.status_var.set("Refreshing data...")
        self.root.update()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get mentions in a separate thread to avoid UI freezing
        def update_data():
            try:
                mentions = self.scraper.aggregate_mentions()
                
                for ticker, count in mentions:
                    stock_info = self.analyzer.get_stock_info(ticker)
                    if stock_info:
                        change_color = "green" if stock_info['change'] >= 0 else "red"
                        
                        item = self.tree.insert('', tk.END, values=(
                            ticker,
                            count,
                            f"${stock_info['current_price']:.2f}",
                            f"{stock_info['change_percent']:.2f}%"
                        ))
                        
                        # Color coding for positive/negative changes
                        if stock_info['change'] >= 0:
                            self.tree.set(item, 'Change %', f"+{stock_info['change_percent']:.2f}%")
                
                self.status_var.set(f"Updated {len(mentions)} stocks")
                
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
        
        # Run in thread to prevent UI blocking
        thread = threading.Thread(target=update_data)
        thread.daemon = True
        thread.start()
    
    def on_stock_select(self, event):
        """Handle stock selection from the list"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        ticker = self.tree.item(item)['values'][0]
        
        self.display_stock_details(ticker)
    
    def display_stock_details(self, ticker):
        """Display detailed information for selected stock"""
        self.status_var.set(f"Loading details for {ticker}...")
        
        def load_details():
            stock_info = self.analyzer.get_stock_info(ticker)
            if not stock_info:
                self.status_var.set(f"Could not load data for {ticker}")
                return
            
            # Update labels
            self.stock_name_label.config(text=f"{stock_info['name']} ({ticker})")
            
            change_text = f"${stock_info['current_price']:.2f} "
            if stock_info['change'] >= 0:
                change_text += f"(+${stock_info['change']:.2f}, +{stock_info['change_percent']:.2f}%)"
            else:
                change_text += f"(${stock_info['change']:.2f}, {stock_info['change_percent']:.2f}%)"
            
            self.price_label.config(text=change_text)
            
            # Update details
            self.details_text.delete(1.0, tk.END)
            details = f"""Market Cap: {self.format_market_cap(stock_info['market_cap'])}
Volume: {stock_info['volume']:,}
Average Volume: {self.format_number(stock_info['avg_volume'])}
Day High: ${stock_info['day_high']:.2f}
Day Low: ${stock_info['day_low']:.2f}
P/E Ratio: {self.format_number(stock_info['pe_ratio'])}
Beta: {self.format_number(stock_info['beta'])}
Dividend Yield: {self.format_percentage(stock_info['dividend_yield'])}"""
            
            self.details_text.insert(1.0, details)
            
            # Update chart
            self.update_chart(stock_info)
            
            self.status_var.set(f"Loaded details for {ticker}")
        
        thread = threading.Thread(target=load_details)
        thread.daemon = True
        thread.start()
    
    def update_chart(self, stock_info):
        """Update the price chart"""
        self.ax.clear()
        
        hist = stock_info['history']
        dates = hist.index
        prices = hist['Close']
        
        self.ax.plot(dates, prices, linewidth=2, color='blue')
        self.ax.set_title(f"{stock_info['symbol']} - 30 Day Price Chart")
        self.ax.set_ylabel("Price ($)")
        self.ax.grid(True, alpha=0.3)
        
        # Format x-axis
        self.ax.tick_params(axis='x', rotation=45)
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def format_market_cap(self, market_cap):
        """Format market cap for display"""
        if market_cap == 'N/A' or market_cap is None:
            return 'N/A'
        
        if market_cap >= 1e12:
            return f"${market_cap/1e12:.2f}T"
        elif market_cap >= 1e9:
            return f"${market_cap/1e9:.2f}B"
        elif market_cap >= 1e6:
            return f"${market_cap/1e6:.2f}M"
        else:
            return f"${market_cap:,.0f}"
    
    def format_number(self, num):
        """Format numbers for display"""
        if num == 'N/A' or num is None:
            return 'N/A'
        return f"{num:,.2f}"
    
    def format_percentage(self, pct):
        """Format percentage for display"""
        if pct == 'N/A' or pct is None:
            return 'N/A'
        return f"{pct*100:.2f}%"

def main():
    root = tk.Tk()
    app = StockDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()