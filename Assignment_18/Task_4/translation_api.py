"""
Translation API Script
Translates text to specified languages using LibreTranslate API with retry mechanism.
Includes comprehensive error handling and robust failure management.
"""

import requests
import sys
import json
import time
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime
from requests.exceptions import Timeout, ConnectionError, RequestException
from enum import Enum


# Supported Languages (LibreTranslate)
SUPPORTED_LANGUAGES = {
    "auto": "Auto-detect",
    "ar": "Arabic",
    "bn": "Bengali",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "fa": "Farsi",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "kn": "Kannada",
    "ko": "Korean",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ne": "Nepali",
    "nl": "Dutch",
    "pa": "Punjabi",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sv": "Swedish",
    "ta": "Tamil",
    "te": "Telugu",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "vi": "Vietnamese",
    "zh": "Chinese",
}


class RetryStrategy(Enum):
    """Retry strategy options."""
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    IMMEDIATE = "immediate"


class TranslationAPIClient:
    """Client for translating text using LibreTranslate API."""
    
    # LibreTranslate API endpoints
    FREE_API_URL = "https://libretranslate.de/translate"
    LANGUAGE_LIST_URL = "https://libretranslate.de/languages"
    
    # Alternative free API endpoints (for fallback)
    ALTERNATIVE_APIS = [
        "https://libretranslate.de/translate",  # Primary
        "https://api.mymemory.translated.net/get",  # MyMemory (Alternative format)
    ]
    
    # Configuration
    TIMEOUT = 15  # seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    RETRY_STRATEGY = RetryStrategy.EXPONENTIAL
    
    # Rate limiting
    REQUEST_TIMEOUT = 0.5  # Minimum delay between requests
    
    def __init__(self, max_retries: int = MAX_RETRIES, use_mock: bool = False):
        """
        Initialize the TranslationAPIClient.
        
        Args:
            max_retries: Maximum number of retry attempts
            use_mock: Whether to use mock data instead of real API
        """
        self.max_retries = max_retries
        self.use_mock = use_mock
        self.session = requests.Session()
        self.last_request_time = 0
    
    def _rate_limit(self) -> None:
        """Apply rate limiting to prevent API throttling."""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.REQUEST_TIMEOUT:
            time.sleep(self.REQUEST_TIMEOUT - elapsed)
        
        self.last_request_time = time.time()
    
    def _calculate_retry_delay(self, attempt: int) -> float:
        """
        Calculate delay before next retry attempt.
        
        Args:
            attempt: Attempt number (0-indexed)
            
        Returns:
            Delay in seconds
        """
        if self.RETRY_STRATEGY == RetryStrategy.EXPONENTIAL:
            return self.RETRY_DELAY * (2 ** attempt)
        elif self.RETRY_STRATEGY == RetryStrategy.LINEAR:
            return self.RETRY_DELAY * (attempt + 1)
        else:  # IMMEDIATE
            return 0
    
    def validate_input(self, text: str, target_language: str) -> Tuple[bool, Optional[str]]:
        """
        Validate user input.
        
        Args:
            text: Text to translate
            target_language: Target language code
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate text
        if not text or not text.strip():
            return False, "Text cannot be empty. Please provide text to translate."
        
        if len(text.strip()) > 5000:
            return False, "Text too long. Maximum 5000 characters allowed."
        
        # Validate language code
        if not target_language or not target_language.strip():
            return False, "Target language code cannot be empty."
        
        lang_code = target_language.lower().strip()
        
        if lang_code not in SUPPORTED_LANGUAGES:
            available = ", ".join(sorted(SUPPORTED_LANGUAGES.keys()))
            return False, (
                f"Invalid language code: '{target_language}'. "
                f"Supported codes: {available[:100]}..."
            )
        
        return True, None
    
    def _fetch_mock_translation(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Fetch mock translation data.
        
        Args:
            text: Text to translate
            target_language: Target language code
            
        Returns:
            Translation result dictionary
        """
        mock_translations = {
            ("hello world", "es"): "Hola mundo",
            ("hello world", "fr"): "Bonjour le monde",
            ("hello world", "de"): "Hallo Welt",
            ("hello world", "ja"): "こんにちは世界",
            ("hello world", "zh"): "你好世界",
            ("hello world", "ru"): "Привет мир",
            ("good morning", "es"): "Buenos días",
            ("good morning", "fr"): "Bonjour",
            ("good morning", "de"): "Guten Morgen",
            ("good morning", "ja"): "おはようございます",
            ("how are you", "de"): "Wie geht es dir?",
            ("how are you", "es"): "¿Cómo estás?",
            ("how are you", "fr"): "Comment allez-vous?",
            ("how are you", "ja"): "お元気ですか？",
            ("thank you", "fr"): "Merci",
            ("thank you", "es"): "Gracias",
            ("thank you", "de"): "Danke",
            ("thank you", "ja"): "ありがとうございます",
            ("goodbye", "ja"): "さようなら",
            ("goodbye", "es"): "Adiós",
            ("goodbye", "fr"): "Au revoir",
        }
        
        # Try to find exact or similar match
        key = (text.lower(), target_language.lower())
        
        if key in mock_translations:
            translated = mock_translations[key]
        else:
            # Generate a simple mock translation
            translated = f"[{SUPPORTED_LANGUAGES.get(target_language.lower(), 'Unknown')} translation of '{text}']"
        
        return {
            "translatedText": translated,
            "detectedLanguage": {
                "language": "en",
                "confidence": 0.95
            },
            "timestamp": datetime.now().isoformat(),
            "is_mock": True
        }
    
    def _fetch_real_translation(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Fetch translation from real LibreTranslate API.
        
        Args:
            text: Text to translate
            target_language: Target language code
            
        Returns:
            Translation result dictionary
        """
        self._rate_limit()
        
        payload = {
            "q": text,
            "source": "auto",
            "target": target_language.lower()
        }
        
        try:
            response = self.session.post(
                self.FREE_API_URL,
                json=payload,
                timeout=self.TIMEOUT
            )
            response.raise_for_status()
            
        except Timeout:
            raise TimeoutError(
                f"Request timed out after {self.TIMEOUT} seconds. "
                "The translation API is not responding."
            )
        except ConnectionError:
            raise ConnectionError(
                "Failed to connect to the translation API. "
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
        
        # Validate response
        if not isinstance(data, dict):
            raise ValueError(
                "Malformed API response: Expected JSON object."
            )
        
        # Check for API errors
        if 'error' in data:
            error_msg = data.get('error', 'Unknown error')
            
            if 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
                raise ConnectionError(
                    f"API quota exceeded: {error_msg}. "
                    "Please try again later."
                )
            elif 'language' in error_msg.lower():
                raise ValueError(
                    f"Invalid language code. {error_msg}"
                )
            else:
                raise ConnectionError(f"API Error: {error_msg}")
        
        if 'translatedText' not in data:
            raise ValueError(
                "Malformed API response: Missing 'translatedText' field."
            )
        
        data['timestamp'] = datetime.now().isoformat()
        data['is_mock'] = False
        
        return data
    
    def translate(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Translate text to target language with retry mechanism.
        
        Args:
            text: Text to translate
            target_language: Target language code
            
        Returns:
            Dictionary containing translation and metadata
            
        Raises:
            Various exceptions for different error scenarios
        """
        # Validate input
        is_valid, error_msg = self.validate_input(text, target_language)
        if not is_valid:
            raise ValueError(error_msg)
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                if self.use_mock:
                    result = self._fetch_mock_translation(text, target_language)
                else:
                    result = self._fetch_real_translation(text, target_language)
                
                result['attempts'] = attempt + 1
                return result
                
            except (TimeoutError, ConnectionError) as e:
                last_error = e
                
                if attempt < self.max_retries - 1:
                    delay = self._calculate_retry_delay(attempt)
                    print(f"⏳ Attempt {attempt + 1} failed, retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    raise
            
            except (ValueError, RequestException) as e:
                # Don't retry for validation or malformed response errors
                raise
        
        # If we get here, all retries failed
        raise last_error
    
    def format_translation(self, translation_data: Dict[str, Any], 
                          original_text: str, target_language: str) -> str:
        """
        Format translation result for display.
        
        Args:
            translation_data: Translation result dictionary
            original_text: Original input text
            target_language: Target language code
            
        Returns:
            Formatted string with translation details
        """
        translated_text = translation_data.get('translatedText', 'N/A')
        attempts = translation_data.get('attempts', 1)
        timestamp = translation_data.get('timestamp', 'N/A')
        is_mock = translation_data.get('is_mock', False)
        
        # Parse timestamp for display
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            time_str = timestamp
        
        # Get language names
        target_lang_name = SUPPORTED_LANGUAGES.get(
            target_language.lower(), 
            target_language.upper()
        )
        
        # Build the formatted output
        output = "\n" + "=" * 75 + "\n"
        output += f"{'TRANSLATION RESULT':^75}\n"
        output += "=" * 75 + "\n"
        
        # Show attempts info if retried
        if attempts > 1:
            output += f"Status:            ✅ Succeeded after {attempts} attempts\n"
        else:
            output += f"Status:            ✅ Translated successfully\n"
        
        if is_mock:
            output += f"Mode:              🔷 Mock Mode (Demo Data)\n"
        else:
            output += f"Mode:              🔵 Live API\n"
        
        output += f"Timestamp:         {time_str}\n"
        output += "-" * 75 + "\n"
        output += f"Original Text ({SUPPORTED_LANGUAGES.get('en', 'English')}):\n"
        output += f"{original_text}\n"
        output += "-" * 75 + "\n"
        output += f"Translated Text ({target_lang_name}):\n"
        output += f"{translated_text}\n"
        output += "=" * 75 + "\n"
        
        return output
    
    def get_available_languages(self) -> str:
        """
        Get a formatted list of available languages.
        
        Returns:
            Formatted string with language list
        """
        output = "\n" + "=" * 75 + "\n"
        output += f"{'SUPPORTED LANGUAGES':^75}\n"
        output += "=" * 75 + "\n"
        
        # Format languages in columns
        languages = []
        for code, name in sorted(SUPPORTED_LANGUAGES.items()):
            languages.append(f"{code:8} → {name}")
        
        # Print in 2 columns
        mid_point = len(languages) // 2
        for i in range(mid_point):
            left = languages[i]
            right = languages[mid_point + i] if mid_point + i < len(languages) else ""
            output += f"{left:40} {right}\n"
        
        output += "=" * 75 + "\n"
        
        return output


def main():
    """Main function to run the translation script."""
    
    # Initialize the API client (using mock mode for demo/testing)
    # Change use_mock=True to use_mock=False to use real LibreTranslate API
    client = TranslationAPIClient(max_retries=3, use_mock=True)
    
    # Get input text and target language from command line
    if len(sys.argv) > 2:
        original_text = sys.argv[1]
        target_language = sys.argv[2]
    else:
        print("\n" + "=" * 75)
        print(f"{'TRANSLATION SERVICE':^75}")
        print("=" * 75)
        print("\nEnter the text you want to translate (or 'list' to see languages):")
        original_text = input("> ").strip()
        
        if original_text.lower() == 'list':
            print(client.get_available_languages())
            return
        
        print("\nEnter target language code (e.g., 'es', 'fr', 'de', 'ja'):")
        print("(Type 'list' to see all supported languages)")
        target_language = input("> ").strip()
        
        if target_language.lower() == 'list':
            print(client.get_available_languages())
            return
    
    try:
        # Translate
        print("\n🔄 Translating...\n")
        translation_result = client.translate(original_text, target_language)
        
        # Display results
        formatted_output = client.format_translation(
            translation_result,
            original_text,
            target_language
        )
        print(formatted_output)
        
    except ValueError as e:
        print(f"\n❌ Validation Error: {str(e)}\n")
        sys.exit(1)
    except TimeoutError as e:
        print(f"\n❌ Timeout Error: {str(e)}\n")
        print("The translation service is not responding. Please try again later.\n")
        sys.exit(1)
    except ConnectionError as e:
        print(f"\n❌ Connection Error: {str(e)}\n")
        print("Please check your internet connection or try again later.\n")
        sys.exit(1)
    except RequestException as e:
        print(f"\n❌ Request Error: {str(e)}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
