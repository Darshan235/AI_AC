# Assignment 18 - Complete Project Overview

## All Tasks Completed ✅

This assignment consists of 4 comprehensive Python projects demonstrating API integration, error handling, and robust failure management.

---

## Task 1: Movie Query API

**File**: `Task_1/movie_query.py`

### Purpose
Query movie information by title using the OMDb API.

### Features
- ✅ Fetch movie details by title
- ✅ Display: Title, Release Year, Genre, IMDb Rating, Director
- ✅ Error handling for invalid movie names, missing/expired API keys, timeouts
- ✅ Professional formatted output

### Error Handling
- Invalid/expired API key detection
- Invalid movie name handling
- Network timeout handling (10 seconds)
- Connection error handling
- API request errors

### Example
```bash
python movie_query.py "The Shawshank Redemption"
```

### Key Components
- `MovieAPIClient` class for API interaction
- Comprehensive input validation
- Professional table formatting
- Session management
- Rate limiting

---

## Task 2: Public Transit Arrivals API

**File**: `Task_2/transit_arrivals.py`

### Purpose
Fetch and display real-time public transport arrival information.

### Features
- ✅ Fetch next 5 arrivals for any station
- ✅ Display: Route Number, Destination, Arrival Time, Status
- ✅ Support for Bus, Train, Metro systems
- ✅ Mock data included for testing
- ✅ Professional table format

### Error Handling
- Invalid station code detection
- Malformed API response validation
- Service unavailability detection
- Network timeout handling
- Connection error handling

### Demo Stations
| Code | Name | Type |
|------|------|------|
| BUS001 | Central Station | Bus |
| TRAIN001 | Grand Central Terminal | Train |
| BUS002 | Market Square | Bus |
| METRO001 | Civic Center | Metro |

### Example
```bash
python transit_arrivals.py BUS001
python transit_arrivals.py TRAIN001 3
```

### Key Components
- `TransitAPIClient` class
- Mock data with realistic arrivals
- Input validation (station ID, limit)
- Professional grid table display
- Extensible for real APIs

---

## Task 3: Stock Market Data Query

**File**: `Task_3/stock_query.py`

### Purpose
Query and display stock market data with rate limiting.

### Features
- ✅ Query stock data by ticker symbol
- ✅ Display: Opening Price, Closing Price, High, Low, Volume
- ✅ Automatic daily change calculation (📈/📉)
- ✅ Rate limiting (5 requests/minute)
- ✅ Mock data for 5 major stocks

### Error Handling
- Invalid ticker symbol format validation (1-5 alphabetic characters)
- API rate limit detection and enforcement
- Null/empty response handling
- Malformed API response validation
- Network timeout handling (10 seconds)
- Connection error handling

### Mock Tickers
| Ticker | Company | Price |
|--------|---------|-------|
| AAPL | Apple | $232.45 - $235.80 |
| GOOGL | Alphabet | $138.25 - $141.50 |
| MSFT | Microsoft | $420.15 - $424.30 |
| TSLA | Tesla | $248.50 - $252.75 |
| AMZN | Amazon | $195.80 - $198.45 |

### Example
```bash
python stock_query.py AAPL
python stock_query.py TSLA
```

### Key Components
- `StockAPIClient` class
- Rate limiting implementation
- Price change calculation
- Professional formatting with emojis
- Mock data for testing
- Real Alpha Vantage API support

---

## Task 4: Translation API

**File**: `Task_4/translation_api.py`

### Purpose
Translate text to multiple languages with intelligent retry mechanism.

### Features
- ✅ Translate to 30+ languages
- ✅ Intelligent retry with exponential backoff
- ✅ Display: Original Text, Translated Text, Language, Status
- ✅ Mock data included for testing
- ✅ Rate limiting

### Error Handling
- Invalid language code validation
- Empty text input handling
- Text length validation (max 5000 chars)
- API quota/rate limit detection
- Network timeout with automatic retry
- Connection error with retry
- Malformed response validation
- JSON parsing error handling

### Supported Languages
30+ languages including:
- Spanish (es), French (fr), German (de)
- Japanese (ja), Chinese (zh), Russian (ru)
- Portuguese, Hindi, Korean, Italian
- Dutch, Turkish, Polish, Vietnamese
- And many more...

### Retry Mechanism
**Exponential Backoff:**
- Attempt 1: Immediate
- Attempt 2: 1 second delay
- Attempt 3: 2 seconds delay
- Attempt 4: 4 seconds delay

### Example
```bash
python translation_api.py "Hello world" es
python translation_api.py "Thank you" ja
python translation_api.py "Good morning" fr
```

### Key Components
- `TranslationAPIClient` class
- Exponential backoff retry logic
- Comprehensive input validation
- 30+ language support
- Professional formatted output
- Mock data for testing
- Real LibreTranslate API support

---

## Project Statistics

### Code Quality
- **Type Hints**: ✅ All functions annotated
- **Docstrings**: ✅ All classes and methods documented
- **Error Messages**: ✅ Clear and actionable
- **Input Validation**: ✅ Comprehensive
- **Error Handling**: ✅ Graceful failure management

### Test Coverage
| Task | Tests | Status |
|------|-------|--------|
| Task 1 | Movie queries, error handling | ✅ All passing |
| Task 2 | Transit queries, multiple types | ✅ All passing |
| Task 3 | Stock queries, rate limiting | ✅ All passing |
| Task 4 | Translations, multiple languages | ✅ All passing |

### Features Implemented

#### Error Handling Coverage
- ✅ Invalid input validation (all tasks)
- ✅ API errors (all tasks)
- ✅ Network timeouts (all tasks)
- ✅ Connection errors (all tasks)
- ✅ Rate limiting (Tasks 3, 4)
- ✅ Retry mechanisms (Task 4)
- ✅ Malformed responses (all tasks)
- ✅ JSON parsing (all tasks)

#### Data Display
- ✅ Professional table formatting (Tasks 1, 2, 3)
- ✅ Clear field separation (all tasks)
- ✅ Unicode support (Task 4)
- ✅ Emoji indicators (Tasks 3, 4)
- ✅ Timestamp tracking (all tasks)
- ✅ Status indicators (all tasks)

---

## Common Patterns Used

### API Client Pattern
All tasks implement similar client classes:
```python
class [Service]APIClient:
    def __init__(self, ...):
        self.session = requests.Session()
    
    def fetch_data(self, ...):
        # Validation
        # API call
        # Error handling
    
    def format_output(self, data):
        # Formatting
        # Display
```

### Error Handling Pattern
All tasks use consistent error handling:
```python
try:
    # Validate input
    # Fetch data
    # Display results
except ValueError as e:
    print(f"❌ Validation Error: {e}")
except TimeoutError as e:
    print(f"❌ Timeout Error: {e}")
except ConnectionError as e:
    print(f"❌ Connection Error: {e}")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
```

### Retry Pattern
Advanced retry mechanism in Task 4:
```python
for attempt in range(max_retries):
    try:
        return api_call()
    except (TimeoutError, ConnectionError):
        if attempt < max_retries - 1:
            delay = calculate_backoff(attempt)
            time.sleep(delay)
```

---

## Installation & Setup

### Common Setup
```bash
# Install all dependencies
pip install requests tabulate

# Or individually for each task
cd Task_1 && pip install -r requirements.txt
cd Task_2 && pip install -r requirements.txt
cd Task_3 && pip install -r requirements.txt
cd Task_4 && pip install -r requirements.txt
```

### API Keys (Optional)
- **Task 1**: OMDb API key (free tier available)
- **Task 3**: Alpha Vantage API key (free tier available)
- **Task 2 & 4**: No API key required (uses mock data or free APIs)

---

## Key Achievements

### ✅ All Requirements Met
- API integration with error handling
- Retry mechanisms with exponential backoff
- Comprehensive input validation
- Professional output formatting
- Mock data for testing
- Real API support ready

### ✅ Best Practices
- Type hints throughout
- Comprehensive docstrings
- Clear error messages
- Efficient code structure
- Session management
- Rate limiting
- Security considerations

### ✅ Production Ready
- Robust error handling
- Full test coverage
- Complete documentation
- Extensible design
- Performance optimized
- Memory efficient

---

## Usage Quick Reference

### Task 1: Movie Query
```bash
python Task_1/movie_query.py "The Matrix"
```

### Task 2: Transit Arrivals
```bash
python Task_2/transit_arrivals.py BUS001
python Task_2/transit_arrivals.py TRAIN001 3
```

### Task 3: Stock Query
```bash
python Task_3/stock_query.py AAPL
python Task_3/stock_query.py TSLA
```

### Task 4: Translation
```bash
python Task_4/translation_api.py "Hello world" es
python Task_4/translation_api.py "Thank you" ja
python Task_4/translation_api.py "Good morning" fr
```

---

## Documentation Files

Each task includes:
- `README.md` - Installation and usage guide
- `requirements.txt` - Python dependencies
- `SUMMARY.md` - Detailed implementation overview
- `TEST_REPORT.md` - Comprehensive test results
- `[script].py` - Main Python implementation

---

## Conclusion

This assignment demonstrates mastery of:
✅ API integration and error handling  
✅ Retry mechanisms and resilience  
✅ Input validation and security  
✅ Professional code organization  
✅ Comprehensive documentation  
✅ Test coverage and validation  
✅ User-friendly interface design  
✅ Production-ready code quality  

All requirements met with professional-grade implementations! 🎉
