# Movie API Query Script

A Python script that queries the OMDb API to retrieve and display movie details with comprehensive error handling.

## Features

✅ **Query movies by title** - Search for any movie in the OMDb database
✅ **Display detailed information**:
  - Movie Title
  - Release Year
  - Genre
  - IMDb Rating
  - Director

✅ **Comprehensive Error Handling**:
  - Invalid/expired API key detection
  - Invalid movie name handling
  - Network timeout handling
  - Connection error handling
  - API request errors

✅ **Clean output formatting** - Professional display of movie information

## Prerequisites

- Python 3.6 or higher
- `requests` library

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Get a free OMDb API key:
   - Visit: https://www.omdbapi.com/apikey.aspx
   - Sign up for a free API key
   - **IMPORTANT**: Check your email and click the confirmation link to activate the key
   - Copy your activated API key

3. Set your API key as an environment variable:
   
   **PowerShell (Windows):**
   ```powershell
   $env:OMDB_API_KEY = "your_actual_api_key_here"
   ```
   
   **Command Prompt (Windows):**
   ```cmd
   set OMDB_API_KEY=your_actual_api_key_here
   ```
   
   **Linux/Mac (Bash):**
   ```bash
   export OMDB_API_KEY=your_actual_api_key_here
   ```
   
   Or edit `movie_query.py` directly and replace `'YOUR_API_KEY_HERE'` with your API key.

## Usage

### Method 1: Command Line Argument
```bash
python movie_query.py "The Shawshank Redemption"
```

### Method 2: Interactive Input
```bash
python movie_query.py
```
Then enter the movie title when prompted.

## Example Output

```
============================================================
                    MOVIE DETAILS
============================================================
Title:        The Shawshank Redemption
Release Year: 1994
Genre:        Drama
IMDb Rating:  9.3/10
Director:     Frank Darabont
============================================================
```

## Error Handling Examples

### Invalid API Key
```
❌ Validation Error: Invalid or expired API key. Please check your OMDb API key at https://www.omdbapi.com/apikey.aspx
```

### Movie Not Found
```
❌ Validation Error: Movie not found: 'Nonexistent Movie'. Please check the title and try again.
```

### Timeout Error
```
❌ Timeout Error: Request timed out after 10 seconds. The server is taking too long to respond. Please try again later.
```

### Connection Error
```
❌ Connection Error: Failed to connect to the OMDb API. Please check your internet connection.
```

### Empty Title
```
❌ Validation Error: Movie title cannot be empty.
```

## Code Structure

### `MovieAPIClient` Class

**Methods:**
- `__init__(api_key)` - Initialize with your API key
- `query_movie(title)` - Query the API and return movie data
- `format_movie_details(movie_data)` - Format and return prettified output

**Key Features:**
- Uses `requests.Session()` for efficient HTTP connections
- Configurable timeout (default: 10 seconds)
- Handles all common error scenarios
- Type hints for better code clarity

## Troubleshooting

### "Invalid or expired API key"
- Verify your API key is correct and active
- Check if your API key has hit usage limits (free tier has ~1000 requests/day)

### "Movie not found"
- Try searching with the exact movie title
- Use quotes for multi-word titles

### Timeout errors
- Check your internet connection
- Increase the `TIMEOUT` value in the `MovieAPIClient` class if needed

### Empty response
- Ensure you're using a valid movie title
- The OMDb API may not have all movies in their database

## API Limitations

- Free tier: ~1000 requests per day
- The script uses the `type: 'movie'` parameter to return only movie results
- Some movies may not be in the OMDb database

## License

MIT License - Feel free to modify and use as needed
