"""Setup configuration for Stock Trading Dashboard."""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
try:
    long_description = (this_directory / "README.md").read_text(encoding='utf-8')
except FileNotFoundError:
    long_description = "A stock trading dashboard"

setup(
    name="stock-trading-dashboard",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A stock trading dashboard that analyzes social media mentions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        'yfinance>=0.2.32',
        'pandas>=2.0.0',
        'requests>=2.31.0',
        'matplotlib>=3.7.0',
        'praw>=7.7.0',
        'textblob>=0.17.0',
        'python-dotenv>=1.0.0',
        'PyYAML>=6.0',
        'numpy>=1.24.0'
    ],
    entry_points={
        "console_scripts": [
            "stock-dashboard=src.main:main",
        ],
    },
)
