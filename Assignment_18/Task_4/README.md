# Translation API Script

A Python script that translates text to multiple languages using LibreTranslate API with intelligent retry mechanisms and comprehensive error handling.

## Features

✅ **Translate text to 30+ languages** - Supports most major world languages
✅ **Intelligent retry mechanism** - Automatic retry with exponential backoff
✅ **Display formatted results**:
  - Original text
  - Translated text
  - Target language
  - Translation attempt count
  - Live vs Mock mode indicator
  - Timestamp

✅ **Comprehensive Error Handling**:
  - Invalid language codes
  - API quota/rate limit exceeded
  - Empty text input
  - Text too long (max 5000 characters)
  - Network timeouts
  - Connection errors
  - Malformed API responses
  - JSON parsing errors

✅ **Advanced Features**:
  - Exponential backoff retry strategy
  - Rate limiting to prevent API throttling
  - Mock data mode for testing
  - Language list display
  - Input validation
  - Auto language detection

## Prerequisites

- Python 3.6 or higher
- `requests` library
- Internet connection (for real API calls)

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Supported Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| auto | Auto-detect | ar | Arabic |
| en | English | es | Spanish |
| fr | French | de | German |
| ja | Japanese | zh | Chinese |
| ru | Russian | pt | Portuguese |
| hi | Hindi | ko | Korean |
| it | Italian | nl | Dutch |
| tr | Turkish | pl | Polish |
| vi | Vietnamese | id | Indonesian |
| th | Thai | uk | Ukrainian |
| el | Greek | he | Hebrew |
| cs | Czech | ro | Romanian |
| sv | Swedish | da | Danish |

... and 16 more languages (type `list` to see complete list)

## Usage

### Method 1: Command Line Arguments
```bash
python translation_api.py "Hello world" es
```

### Method 2: Interactive Mode
```bash
python translation_api.py
```
Then enter text and target language when prompted.

### Method 3: List Available Languages
```bash
python translation_api.py
# Type 'list' at the prompt
```

## Example Output

```
===========================================================================
                        TRANSLATION RESULT
===========================================================================
Status:            ✅ Translated successfully
Mode:              🔵 Live API
Timestamp:         2025-11-11 14:30:45
---------------------------------------------------------------------------
Original Text (English):
Hello world

---------------------------------------------------------------------------
Translated Text (Spanish):
Hola mundo

===========================================================================
```

### With Retry Attempts

```
⏳ Attempt 1 failed, retrying in 1s...
⏳ Attempt 2 failed, retrying in 2s...

===========================================================================
                        TRANSLATION RESULT
===========================================================================
Status:            ✅ Succeeded after 3 attempts
Mode:              🔵 Live API
Timestamp:         2025-11-11 14:30:48
---------------------------------------------------------------------------
Original Text (English):
The quick brown fox jumps over the lazy dog

---------------------------------------------------------------------------
Translated Text (German):
Der schnelle braune Fuchs springt über den faulen Hund

===========================================================================
```

## Error Handling Examples

### Empty Text Input
```
❌ Validation Error: Text cannot be empty. Please provide text to translate.
```

### Invalid Language Code
```
❌ Validation Error: Invalid language code: 'xyz'. 
   Supported codes: auto, ar, bn, cs, cy, da, de, el, en, es, fa, ...
```

### Text Too Long
```
❌ Validation Error: Text too long. Maximum 5000 characters allowed.
```

### API Quota Exceeded
```
❌ Connection Error: API quota exceeded: Rate limit exceeded. Please try again later.
```

### Timeout Error
```
❌ Timeout Error: Request timed out after 15 seconds. The translation API is not responding.
```

### Connection Error
```
❌ Connection Error: Failed to connect to the translation API. 
   Please check your internet connection.
```

### Malformed Response
```
❌ Validation Error: Malformed API response: Invalid JSON returned by the server.
```

## Retry Mechanism

The script implements an intelligent retry mechanism:

### Retry Strategy Options
1. **Exponential Backoff** (Default)
   - Attempt 1: 1 second delay
   - Attempt 2: 2 seconds delay
   - Attempt 3: 4 seconds delay

2. **Linear Backoff**
   - Attempt 1: 1 second delay
   - Attempt 2: 2 seconds delay
   - Attempt 3: 3 seconds delay

3. **Immediate**
   - No delay between attempts

### When Retries Happen
✅ Timeout errors  
✅ Connection errors  
✅ Server errors (5xx)  

### When Retries Don't Happen
❌ Validation errors (invalid language, empty text)  
❌ Malformed responses  
❌ User input errors  

## Code Structure

### `TranslationAPIClient` Class

**Methods:**
- `__init__(max_retries, use_mock)` - Initialize client
- `translate(text, target_language)` - Main translation method
- `validate_input(text, target_language)` - Validate user input
- `_fetch_real_translation()` - Query LibreTranslate API
- `_fetch_mock_translation()` - Use mock data
- `_calculate_retry_delay()` - Exponential backoff calculation
- `format_translation()` - Format results for display
- `get_available_languages()` - Display language list

**Key Features:**
- Comprehensive input validation
- Retry logic with exponential backoff
- Rate limiting between requests
- Detailed error messages
- Timestamp tracking
- Mock data support
- Session management

## API Information

### LibreTranslate
- **Type**: Free, open-source translation API
- **Rate Limits**: Generous (suitable for demo/learning)
- **Supported Languages**: 30+
- **Documentation**: https://libretranslate.de/
- **No API key required**: Works out-of-the-box

### Alternative APIs (Can be integrated)
- **Google Translate API** - Premium option
- **Microsoft Translator** - Enterprise solution
- **MyMemory API** - Community-powered
- **AWS Translate** - Cloud-based

## Advanced Configuration

### Modify Retry Settings
```python
client = TranslationAPIClient(
    max_retries=5,  # More attempts
    use_mock=False   # Use real API
)
```

### Change Retry Strategy
```python
client.RETRY_STRATEGY = RetryStrategy.LINEAR
```

### Adjust Timeouts
```python
client.TIMEOUT = 20  # 20 seconds
client.RETRY_DELAY = 2  # 2 seconds base delay
```

### Rate Limiting
```python
client.REQUEST_TIMEOUT = 1.0  # 1 second between requests
```

### Use Mock Data
```python
client = TranslationAPIClient(use_mock=True)
# Great for testing without API calls
```

## Batch Translation (Advanced)

```python
from translation_api import TranslationAPIClient

client = TranslationAPIClient()
texts = ["Hello", "Good morning", "Thank you"]
target_lang = "es"

for text in texts:
    result = client.translate(text, target_lang)
    print(client.format_translation(result, text, target_lang))
```

## Troubleshooting

### "Invalid language code"
- Check language code spelling (case-insensitive)
- Use `list` to see all supported codes
- Common codes: en, es, fr, de, ja, zh, ru

### "API quota exceeded"
- Wait a few moments before retrying
- The script will automatically retry with delays
- Check your internet connection

### "Text too long"
- Break your text into smaller chunks
- Maximum 5000 characters per request

### Timeout errors
- Check your internet connection
- Try again (script will auto-retry)
- Increase timeout if network is slow

### Empty translation result
- The text might not be translatable
- Try different text or language pair

### "Malformed API response"
- The API may be temporarily unavailable
- Try again in a moment
- Consider using mock mode for testing

## Performance Tips

1. **Batch Processing**: Translate multiple texts in a loop
2. **Caching**: Store translations to avoid re-translating
3. **Rate Limiting**: Built-in to prevent API throttling
4. **Mock Mode**: Use for development/testing to save API calls

## Security Considerations

- No sensitive data should be translated via public APIs
- Use mock mode for testing with sensitive information
- Consider self-hosted LibreTranslate for privacy
- All data is sent via HTTPS

## License

MIT License - Feel free to modify and use as needed
