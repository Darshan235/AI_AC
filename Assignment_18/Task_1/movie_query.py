"""
Movie API Query Script
Retrieves and displays movie details from the OMDb API with comprehensive error handling.
"""

import requests
import sys
import os
from typing import Optional, Dict, Any
from requests.exceptions import Timeout, ConnectionError, RequestException


class MovieAPIClient:
    """Client for querying the OMDb API."""
    
    # API endpoint
    BASE_URL = "http://www.omdbapi.com/"
    
    # Timeout duration in seconds
    TIMEOUT = 10
    
    def __init__(self, api_key: str):
        """
        Initialize the MovieAPIClient.
        
        Args:
            api_key: OMDb API key
        """
        self.api_key = api_key
        self.session = requests.Session()
    
    def query_movie(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Query the OMDb API for a movie by title.
        
        Args:
            title: Movie title to search for
            
        Returns:
            Dictionary containing movie details or None if error occurs
            
        Raises:
            Various exceptions for different error scenarios
        """
        if not title or not title.strip():
            raise ValueError("Movie title cannot be empty.")
        
        if not self.api_key or not self.api_key.strip():
            raise ValueError("API key is missing. Please provide a valid OMDb API key.")
        
        params = {
            't': title.strip(),
            'apikey': self.api_key,
            'type': 'movie'
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
                "The server is taking too long to respond. Please try again later."
            )
        except ConnectionError:
            raise ConnectionError(
                "Failed to connect to the OMDb API. "
                "Please check your internet connection."
            )
        except RequestException as e:
            raise RequestException(f"An error occurred while making the request: {str(e)}")
        
        data = response.json()
        
        # Check if the API returned an error
        if data.get('Response') == 'False':
            error_message = data.get('Error', 'Unknown error occurred.')
            
            if 'invalid api key' in error_message.lower():
                raise ValueError(
                    "Invalid or expired API key. "
                    "Please check your OMDb API key at https://www.omdbapi.com/apikey.aspx"
                )
            elif 'movie not found' in error_message.lower():
                raise ValueError(
                    f"Movie not found: '{title}'. "
                    "Please check the title and try again."
                )
            else:
                raise ValueError(f"API Error: {error_message}")
        
        return data
    
    def format_movie_details(self, movie_data: Dict[str, Any]) -> str:
        """
        Format movie details for display.
        
        Args:
            movie_data: Dictionary containing movie information
            
        Returns:
            Formatted string with movie details
        """
        title = movie_data.get('Title', 'N/A')
        year = movie_data.get('Year', 'N/A')
        genre = movie_data.get('Genre', 'N/A')
        imdb_rating = movie_data.get('imdbRating', 'N/A')
        director = movie_data.get('Director', 'N/A')
        
        # Build the formatted output
        output = "\n" + "=" * 60 + "\n"
        output += f"{'MOVIE DETAILS':^60}\n"
        output += "=" * 60 + "\n"
        output += f"Title:        {title}\n"
        output += f"Release Year: {year}\n"
        output += f"Genre:        {genre}\n"
        output += f"IMDb Rating:  {imdb_rating}/10\n"
        output += f"Director:     {director}\n"
        output += "=" * 60 + "\n"
        
        return output


def main():
    """Main function to run the movie query script."""
    
    # Get API key from environment variable or use default
    # To set: $env:OMDB_API_KEY = "your_api_key" (PowerShell)
    #         export OMDB_API_KEY=your_api_key (Linux/Mac)
    API_KEY = os.getenv('OMDB_API_KEY', 'YOUR_API_KEY_HERE')
    
    # Check if API key is still the placeholder
    if API_KEY == 'YOUR_API_KEY_HERE':
        print("\n" + "=" * 60)
        print("❌ API KEY NOT CONFIGURED")
        print("=" * 60)
        print("\nPlease set your OMDb API key before running this script.\n")
        print("STEP 1: Get a free API key")
        print("  → Visit: https://www.omdbapi.com/apikey.aspx")
        print("  → Sign up for free")
        print("  → Check your email and click the confirmation link")
        print("  → Copy your API key\n")
        print("STEP 2: Set the environment variable in PowerShell:")
        print("  → $env:OMDB_API_KEY = 'your_api_key_here'\n")
        print("STEP 3: Run the script again:")
        print("  → python movie_query.py \"Movie Title\"\n")
        print("=" * 60 + "\n")
        sys.exit(1)
    
    # Get movie title from user input
    if len(sys.argv) > 1:
        movie_title = ' '.join(sys.argv[1:])
    else:
        movie_title = input("\nEnter the movie title: ").strip()
    
    # Initialize the API client
    client = MovieAPIClient(api_key=API_KEY)
    
    try:
        # Query the API
        print("\nSearching for movie information...")
        movie_data = client.query_movie(movie_title)
        
        # Display the results
        formatted_output = client.format_movie_details(movie_data)
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
