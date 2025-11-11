"""
Stock Market Data Query Script
Fetches and displays stock market data with comprehensive error handling.
Supports both real API (Alpha Vantage, Yahoo Finance) and mock data.
"""

import requests
import sys
import os
import json
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from requests.exceptions import Timeout, ConnectionError, RequestException
from tabulate import tabulate


# Mock Stock Data
MOCK_STOCK_DATA = {
    "AAPL": {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "open": 232.45,
        "close": 235.80,
        "high": 238.50,
        "low": 231.20,
        "volume": 52840000,
        "timestamp": datetime.now().isoformat(),
        "currency": "USD"
    },
    "GOOGL": {
        "symbol": "GOOGL",
        "name": "Alphabet Inc.",
        "open": 138.25,
        "close": 141.50,
        "high": 142.75,
        "low": 137.80,
        "volume": 28540000,
        "timestamp": datetime.now().isoformat(),
        "currency": "USD"
    },
    "MSFT": {
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "open": 420.15,
        "close": 424.30,
        "high": 426.80,
        "low": 418.90,
        "volume": 21230000,
        "timestamp": datetime.now().isoformat(),
        "currency": "USD"
    },
    "TSLA": {
        "symbol": "TSLA",
        "name": "Tesla Inc.",
        "open": 248.50,
        "close": 252.75,
        "high": 255.20,
        "low": 246.80,
        "volume": 156840000,
        "timestamp": datetime.now().isoformat(),
        "currency": "USD"
    },
    "AMZN": {
        "symbol": "AMZN",
        "name": "Amazon.com Inc.",
        "open": 195.80,
        "close": 198.45,
        "high": 200.30,
        "low": 194.50,
        "volume": 45670000,
        "timestamp": datetime.now().isoformat(),
        "currency": "USD"
    }
}

# API Rate Limiting
MAX_REQUESTS_PER_MINUTE = 5
REQUEST_COUNT = {"count": 0, "reset_time": datetime.now()}


class StockAPIClient:
    """Client for querying stock market data."""
    
    # Alpha Vantage API endpoint (free tier)
    BASE_URL = "https://www.alphavantage.co/query"
    
    # Timeout duration in seconds
    TIMEOUT = 10
    
    def __init__(self, api_key: Optional[str] = None, use_mock: bool = True):
        """
        Initialize the StockAPIClient.
        
        Args:
            api_key: Alpha Vantage API key (optional if using mock data)
            use_mock: Whether to use mock data (True) or real API (False)
        """
        self.api_key = api_key
        self.use_mock = use_mock
        self.session = requests.Session()
        self.request_count = 0
        self.rate_limit_reset = datetime.now()
    
    def check_rate_limit(self) -> bool:
        """
        Check if rate limit has been exceeded.
        
        Returns:
            True if under limit, False if limit exceeded
        """
        now = datetime.now()
        
        # Reset counter every minute
        if (now - self.rate_limit_reset).total_seconds() >= 60:
            self.request_count = 0
            self.rate_limit_reset = now
        
        return self.request_count < MAX_REQUESTS_PER_MINUTE
    
    def increment_request_count(self) -> None:
        """Increment the request counter."""
        self.request_count += 1
    
    def get_stock_data(self, ticker_symbol: str) -> Dict[str, Any]:
        """
        Fetch stock data for a given ticker symbol.
        
        Args:
            ticker_symbol: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dictionary containing stock information
            
        Raises:
            Various exceptions for different error scenarios
        """
        # Validate ticker symbol
        if not ticker_symbol or not ticker_symbol.strip():
            raise ValueError("Ticker symbol cannot be empty.")
        
        ticker = ticker_symbol.upper().strip()
        
        # Validate ticker format (1-5 alphanumeric characters)
        if not ticker.isalpha() or len(ticker) > 5 or len(ticker) < 1:
            raise ValueError(
                f"Invalid ticker symbol: '{ticker_symbol}'. "
                "Ticker symbols must be 1-5 alphabetic characters."
            )
        
        if self.use_mock:
            return self._fetch_mock_data(ticker)
        else:
            return self._fetch_real_api(ticker)
    
    def _fetch_mock_data(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch mock stock data.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary containing stock information
        """
        if ticker not in MOCK_STOCK_DATA:
            available = ", ".join(sorted(MOCK_STOCK_DATA.keys()))
            raise ValueError(
                f"Invalid ticker symbol: '{ticker}'. "
                f"Available mock tickers: {available}"
            )
        
        return MOCK_STOCK_DATA[ticker].copy()
    
    def _fetch_real_api(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch stock data from Alpha Vantage API.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary containing stock information
        """
        # Check rate limit
        if not self.check_rate_limit():
            raise ConnectionError(
                f"API rate limit exceeded: {MAX_REQUESTS_PER_MINUTE} requests per minute. "
                "Please try again later."
            )
        
        self.increment_request_count()
        
        if not self.api_key:
            raise ValueError(
                "API key is required for real API queries. "
                "Get a free API key from: https://www.alphavantage.co/api/"
            )
        
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': ticker,
            'apikey': self.api_key
        }
        
        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=self.TIMEOUT
            )
            response.raise_for_status()
            
        except Timeout:
            raise TimeoutError(
                f"Request timed out after {self.TIMEOUT} seconds. "
                "The API server is not responding. Please try again later."
            )
        except ConnectionError:
            raise ConnectionError(
                "Failed to connect to the stock API. "
                "Please check your internet connection."
            )
        except RequestException as e:
            raise RequestException(f"API request failed: {str(e)}")
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            raise ValueError(
                "Malformed API response: Invalid JSON returned by the server."
            )
        
        # Validate response structure
        if not isinstance(data, dict):
            raise ValueError(
                "Malformed API response: Expected JSON object."
            )
        
        # Check for API errors
        if 'Error Message' in data:
            raise ValueError(
                f"Invalid ticker symbol: '{ticker}'. "
                "The ticker was not found in the database."
            )
        
        if 'Note' in data:
            # API call frequency limit reached
            raise ConnectionError(
                "API call frequency limit reached. "
                f"Message: {data['Note']} "
                "Please try again later or get a premium API key."
            )
        
        # Check for null responses
        if 'Global Quote' not in data or not data['Global Quote']:
            raise ValueError(
                f"No data available for ticker: '{ticker}'. "
                "The ticker may not be trading or data is not available."
            )
        
        quote = data['Global Quote']
        
        # Validate required fields
        required_fields = ['01. symbol', '02. open', '03. high', '04. low', 
                          '05. price', '06. volume']
        
        if not all(field in quote for field in required_fields):
            raise ValueError(
                "Malformed API response: Missing required stock data fields."
            )
        
        # Parse and validate numeric fields
        try:
            stock_data = {
                "symbol": quote['01. symbol'],
                "open": float(quote['02. open']),
                "high": float(quote['03. high']),
                "low": float(quote['04. low']),
                "close": float(quote['05. price']),
                "volume": int(float(quote['06. volume'])),
                "timestamp": datetime.now().isoformat(),
                "currency": "USD"
            }
        except (ValueError, KeyError) as e:
            raise ValueError(
                f"Malformed API response: Invalid data types in response. {str(e)}"
            )
        
        return stock_data
    
    def format_stock_data(self, stock_data: Dict[str, Any]) -> str:
        """
        Format stock data for display.
        
        Args:
            stock_data: Dictionary containing stock information
            
        Returns:
            Formatted string with stock details
        """
        symbol = stock_data.get('symbol', 'N/A')
        open_price = stock_data.get('open', 'N/A')
        close_price = stock_data.get('close', 'N/A')
        high_price = stock_data.get('high', 'N/A')
        low_price = stock_data.get('low', 'N/A')
        volume = stock_data.get('volume', 'N/A')
        currency = stock_data.get('currency', 'USD')
        timestamp = stock_data.get('timestamp', 'N/A')
        
        # Parse timestamp for display
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            time_str = timestamp
        
        # Format prices
        if isinstance(open_price, (int, float)):
            open_str = f"${open_price:.2f}"
        else:
            open_str = str(open_price)
        
        if isinstance(close_price, (int, float)):
            close_str = f"${close_price:.2f}"
        else:
            close_str = str(close_price)
        
        if isinstance(high_price, (int, float)):
            high_str = f"${high_price:.2f}"
        else:
            high_str = str(high_price)
        
        if isinstance(low_price, (int, float)):
            low_str = f"${low_price:.2f}"
        else:
            low_str = str(low_price)
        
        # Format volume
        if isinstance(volume, int):
            volume_str = f"{volume:,}"
        else:
            volume_str = str(volume)
        
        # Calculate price change
        if isinstance(open_price, (int, float)) and isinstance(close_price, (int, float)):
            change = close_price - open_price
            change_pct = (change / open_price * 100) if open_price != 0 else 0
            change_arrow = "📈" if change >= 0 else "📉"
            change_str = f"{change_arrow} {change:+.2f} ({change_pct:+.2f}%)"
        else:
            change_str = "N/A"
        
        # Build the formatted output
        output = "\n" + "=" * 70 + "\n"
        output += f"{'STOCK MARKET DATA':^70}\n"
        output += "=" * 70 + "\n"
        output += f"Symbol:        {symbol}\n"
        output += f"Currency:      {currency}\n"
        output += f"Updated:       {time_str}\n"
        output += "-" * 70 + "\n"
        output += f"Opening Price: {open_str}\n"
        output += f"Closing Price: {close_str}\n"
        output += f"Day Change:    {change_str}\n"
        output += "-" * 70 + "\n"
        output += f"High:          {high_str}\n"
        output += f"Low:           {low_str}\n"
        output += f"Volume:        {volume_str} shares\n"
        output += "=" * 70 + "\n"
        
        return output


def main():
    """Main function to run the stock data query script."""
    
    # Determine if using mock or real API
    api_key = os.getenv('ALPHAVANTAGE_API_KEY', None)
    use_mock = api_key is None  # Use mock if no API key
    
    # Get ticker symbol from command line or user input
    if len(sys.argv) > 1:
        ticker_symbol = sys.argv[1].strip()
    else:
        if use_mock:
            available = ", ".join(sorted(MOCK_STOCK_DATA.keys()))
            print(f"\nAvailable mock tickers: {available}\n")
        
        ticker_symbol = input("Enter stock ticker symbol: ").strip()
    
    # Initialize the API client
    client = StockAPIClient(api_key=api_key, use_mock=use_mock)
    
    try:
        # Fetch stock data
        print("\nFetching stock data...")
        stock_data = client.get_stock_data(ticker_symbol)
        
        # Display the results
        formatted_output = client.format_stock_data(stock_data)
        print(formatted_output)
        
    except ValueError as e:
        print(f"\n❌ Validation Error: {str(e)}\n")
        sys.exit(1)
    except TimeoutError as e:
        print(f"\n❌ Timeout Error: {str(e)}\n")
        sys.exit(1)
    except ConnectionError as e:
        print(f"\n❌ Connection Error: {str(e)}\n")
        sys.exit(1)
    except RequestException as e:
        print(f"\n❌ Request Error: {str(e)}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
