# Public Transit Arrivals Script

A Python script that fetches and displays real-time public transport arrival information with comprehensive error handling.

## Features

✅ **Fetch transit arrivals** - Get the next 5 arrivals for any station
✅ **Display detailed information**:
  - Route number/name
  - Destination
  - Arrival time (in minutes)
  - Current status (on-time, delayed, etc.)

✅ **Comprehensive Error Handling**:
  - Invalid station codes
  - Service unavailability
  - Malformed API responses
  - Network timeouts
  - Connection errors
  - JSON parsing errors

✅ **Readable table format** - Professional display using grid tables

✅ **Mock data included** - Works out-of-the-box without external API setup

## Prerequisites

- Python 3.6 or higher
- `requests` library
- `tabulate` library

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Available Demo Stations

The script includes mock data for these stations:

| Code | Name | Type |
|------|------|------|
| BUS001 | Central Station | Bus |
| TRAIN001 | Grand Central Terminal | Train |
| BUS002 | Market Square | Bus |
| METRO001 | Civic Center | Metro |

## Usage

### Method 1: Command Line Argument
```bash
python transit_arrivals.py BUS001
```

### Method 2: With Limit Parameter
```bash
python transit_arrivals.py TRAIN001 7
```

### Method 3: Interactive Input
```bash
python transit_arrivals.py
```
Then select from the available stations when prompted.

## Example Output

```
================================================================================
                         TRANSIT ARRIVALS
================================================================================
Station: Central Station (BUS001)
Type: Bus | Updated: 2025-11-11 14:30:45
--------------------------------------------------------------------------------
┌───┬───────┬──────────────────────┬─────────────┬──────────────────┐
│ # │ Route │ Destination          │ Arrival In  │ Status           │
╞═══╪═══════╪══════════════════════╪═════════════╪══════════════════╡
│ 1 │ 12    │ Airport Terminal     │ 3 min       │ On time          │
├───┼───────┼──────────────────────┼─────────────┼──────────────────┤
│ 2 │ 5A    │ Downtown Center      │ 7 min       │ On time          │
├───┼───────┼──────────────────────┼─────────────┼──────────────────┤
│ 3 │ 23    │ Harbor View          │ 12 min      │ Delayed +2 min   │
├───┼───────┼──────────────────────┼─────────────┼──────────────────┤
│ 4 │ 8     │ University Campus    │ 15 min      │ On time          │
├───┼───────┼──────────────────────┼─────────────┼──────────────────┤
│ 5 │ 15    │ Shopping Mall        │ 21 min      │ On time          │
└───┴───────┴──────────────────────┴─────────────┴──────────────────┘
================================================================================
```

## Error Handling Examples

### Invalid Station Code
```
❌ Validation Error: Invalid station code: 'INVALID'. Available stations: BUS001, TRAIN001, BUS002, METRO001
```

### Empty Station ID
```
❌ Validation Error: Station ID cannot be empty.
```

### Invalid Limit
```
❌ Validation Error: Limit must be between 1 and 10.
```

### Service Unavailable
```
❌ Connection Error: Service temporarily unavailable for station 'BUS001'. Please try again in a few moments.
```

### Timeout Error
```
❌ Timeout Error: Request timed out after 10 seconds. The API server is not responding. Please try again later.
```

### Malformed Response
```
❌ Validation Error: Malformed API response: Invalid JSON returned by the server.
```

## Code Structure

### `TransitAPIClient` Class

**Methods:**
- `__init__(use_mock=True)` - Initialize with mock or real API mode
- `get_next_arrivals(station_id, limit=5)` - Fetch arrivals for a station
- `_fetch_mock_data(station_id, limit)` - Get mock transit data
- `_fetch_real_api(station_id, limit)` - Query real transit API (extensible)
- `format_arrivals_table(arrivals_data)` - Format data into readable table

**Key Features:**
- Flexible mock/real API switching
- Comprehensive input validation
- Detailed error messages
- Station metadata tracking
- Timestamp tracking

## Using Real API

To connect to a real public transport API:

1. Update the `BASE_URL` in the `TransitAPIClient` class
2. Initialize the client with `use_mock=False`:
   ```python
   client = TransitAPIClient(use_mock=False)
   ```
3. Adjust API parameters in `_fetch_real_api()` method

Example for real APIs:
- **Google Transit API** - Real-time transit information
- **TfL Unified API** (London) - Bus and train arrivals
- **Bay Area Rapid Transit API** - BART schedules
- **CTA API** (Chicago) - Bus and train data

## Troubleshooting

### "Invalid station code"
- Check that the station code is correct (case-insensitive)
- Use one of the demo stations: BUS001, TRAIN001, BUS002, METRO001

### Timeout errors
- Check your internet connection
- Increase the `TIMEOUT` value in the class if needed

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check virtual environment is activated

## Advanced Usage

### Custom Mock Data
Add your own stations to `MOCK_TRANSIT_DATA`:

```python
MOCK_TRANSIT_DATA["stops"]["CUSTOM01"] = {
    "name": "My Station",
    "type": "bus",
    "arrivals": [
        {"route": "99", "destination": "My Route", "arrival_time": 5, "status": "On time"},
    ]
}
```

### Connection Pooling
The script uses `requests.Session()` for efficient HTTP connections when using real APIs.

## License

MIT License - Feel free to modify and use as needed
