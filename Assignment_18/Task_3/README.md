# Stock Market Data Query Script

A Python script that fetches and displays stock market data with comprehensive error handling.

## Features

✅ **Query stock data by ticker** - Get real-time or mock stock information
✅ **Display detailed information**:
  - Opening Price
  - Closing Price
  - Daily High
  - Daily Low
  - Trading Volume
  - Day Change (with percentage)
  - Last Updated Timestamp

✅ **Comprehensive Error Handling**:
  - Invalid ticker symbols
  - API call rate limiting
  - Null/empty responses
  - Malformed API responses
  - Network timeouts
  - Connection errors
  - API frequency limits

✅ **Flexible data sources** - Mock data or real Alpha Vantage API
✅ **Professional formatting** - Clean, readable output with emoji indicators

## Prerequisites

- Python 3.6 or higher
- `requests` library
- `tabulate` library

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. **Optional**: Get an Alpha Vantage API key for real market data:
   - Visit: https://www.alphavantage.co/api/
   - Sign up for a free API key
   - Set as environment variable:
   
   **PowerShell (Windows):**
   ```powershell
   $env:ALPHAVANTAGE_API_KEY = "your_api_key_here"
   ```
   
   **Linux/Mac:**
   ```bash
   export ALPHAVANTAGE_API_KEY=your_api_key_here
   ```

## Available Mock Tickers

The script includes mock data for these stocks:

| Ticker | Company | Sector |
|--------|---------|--------|
| AAPL | Apple Inc. | Technology |
| GOOGL | Alphabet Inc. | Technology |
| MSFT | Microsoft Corporation | Technology |
| TSLA | Tesla Inc. | Automotive |
| AMZN | Amazon.com Inc. | E-Commerce |

## Usage

### Method 1: Command Line Argument
```bash
python stock_query.py AAPL
```

### Method 2: Interactive Input
```bash
python stock_query.py
```
Then enter the ticker symbol when prompted.

### Method 3: With Real API
```powershell
$env:ALPHAVANTAGE_API_KEY = "your_key"; python stock_query.py AAPL
```

## Example Output

```
======================================================================
                    STOCK MARKET DATA
======================================================================
Symbol:        AAPL
Currency:      USD
Updated:       2025-11-11 13:45:30
----------------------------------------------------------------------
Opening Price: $232.45
Closing Price: $235.80
Day Change:    📈 +3.35 (+1.44%)
----------------------------------------------------------------------
High:          $238.50
Low:           $231.20
Volume:        52,840,000 shares
======================================================================
```

## Error Handling Examples

### Invalid Ticker Symbol
```
❌ Validation Error: Invalid ticker symbol: 'INVALID'. Ticker symbols must be 1-5 alphabetic characters.
```

### Ticker Not Found (Mock Data)
```
❌ Validation Error: Invalid ticker symbol: 'XYZ'. Available mock tickers: AAPL, GOOGL, MSFT, TSLA, AMZN
```

### Rate Limit Exceeded
```
❌ Connection Error: API rate limit exceeded: 5 requests per minute. Please try again later.
```

### Null Response
```
❌ Validation Error: No data available for ticker: 'NONEXIST'. The ticker may not be trading or data is not available.
```

### API Call Frequency Limit
```
❌ Connection Error: API call frequency limit reached. Message: Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day.
```

### Malformed Response
```
❌ Validation Error: Malformed API response: Invalid JSON returned by the server.
```

### Timeout Error
```
❌ Timeout Error: Request timed out after 10 seconds. The API server is not responding. Please try again later.
```

### Empty Ticker
```
❌ Validation Error: Ticker symbol cannot be empty.
```

## Code Structure

### `StockAPIClient` Class

**Methods:**
- `__init__(api_key, use_mock)` - Initialize with optional API key
- `get_stock_data(ticker_symbol)` - Fetch stock data for a ticker
- `check_rate_limit()` - Validate request rate limit
- `increment_request_count()` - Track API requests
- `_fetch_mock_data(ticker)` - Get mock stock data
- `_fetch_real_api(ticker)` - Query Alpha Vantage API
- `format_stock_data(stock_data)` - Format for display

**Key Features:**
- Rate limiting (5 requests/minute)
- Comprehensive input validation
- Detailed error messages
- Timestamp tracking
- Currency handling
- Price change calculation

## Rate Limiting

The script implements client-side rate limiting:
- **Maximum**: 5 requests per minute
- **Reset**: Automatically resets every 60 seconds
- **Detection**: Prevents excess API calls

This matches Alpha Vantage's free tier limits.

## Using Real API Data

### Step 1: Get API Key
- Visit: https://www.alphavantage.co/api/
- Sign up and copy your key

### Step 2: Set Environment Variable
```powershell
$env:ALPHAVANTAGE_API_KEY = "YOUR_KEY"
```

### Step 3: Run Script
```bash
python stock_query.py AAPL
```

The script will automatically use the real API when an API key is set.

## API Response Fields

Alpha Vantage GLOBAL_QUOTE returns:
- `01. symbol` - Stock ticker
- `02. open` - Opening price
- `03. high` - Daily high
- `04. low` - Daily low
- `05. price` - Current/closing price
- `06. volume` - Trading volume

## Troubleshooting

### "Invalid ticker symbol"
- Check ticker spelling (case-insensitive)
- Use valid 1-5 letter ticker codes
- Verify ticker exists in market data

### API Rate Limit Exceeded
- Wait 60 seconds before next request
- Upgrade to premium tier for higher limits

### "No data available"
- Ticker may not be trading
- Market may be closed
- Ticker may not exist

### Timeout errors
- Check internet connection
- Try again later if API is slow

### "Invalid JSON" response
- API may be temporarily unavailable
- Try again later

## Advanced Usage

### Custom Mock Data
Add new stocks to `MOCK_STOCK_DATA`:

```python
MOCK_STOCK_DATA["NVDA"] = {
    "symbol": "NVDA",
    "name": "NVIDIA Corporation",
    "open": 875.50,
    "close": 880.25,
    "high": 885.00,
    "low": 870.00,
    "volume": 35000000,
    "timestamp": datetime.now().isoformat(),
    "currency": "USD"
}
```

### Modifying Rate Limits
Change `MAX_REQUESTS_PER_MINUTE` constant:

```python
MAX_REQUESTS_PER_MINUTE = 10  # Allow 10 requests/minute
```

### Batch Queries (Advanced)
```python
client = StockAPIClient(api_key=api_key)
tickers = ["AAPL", "GOOGL", "MSFT"]
for ticker in tickers:
    data = client.get_stock_data(ticker)
    print(client.format_stock_data(data))
```

## API Providers

This script is configured for Alpha Vantage but can be adapted for:
- **Yahoo Finance API** - Historical and real-time data
- **IEX Cloud** - Real-time and alternative data
- **Polygon.io** - Stock market data and news
- **Finnhub** - Real-time market data
- **TradingView** - Charts and analysis

## License

MIT License - Feel free to modify and use as needed
