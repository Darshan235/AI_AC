"""
Public Transport API Query Script
Fetches and displays real-time transit arrival information with comprehensive error handling.
Uses mock data to simulate a real public transport API.
"""

import requests
import json
import sys
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from requests.exceptions import Timeout, ConnectionError, RequestException
from tabulate import tabulate


# Mock Transit API Data
MOCK_TRANSIT_DATA = {
    "stops": {
        "BUS001": {
            "name": "Central Station",
            "type": "bus",
            "arrivals": [
                {"route": "12", "destination": "Airport Terminal", "arrival_time": 3, "status": "On time"},
                {"route": "5A", "destination": "Downtown Center", "arrival_time": 7, "status": "On time"},
                {"route": "23", "destination": "Harbor View", "arrival_time": 12, "status": "Delayed +2 min"},
                {"route": "8", "destination": "University Campus", "arrival_time": 15, "status": "On time"},
                {"route": "15", "destination": "Shopping Mall", "arrival_time": 21, "status": "On time"},
            ]
        },
        "TRAIN001": {
            "name": "Grand Central Terminal",
            "type": "train",
            "arrivals": [
                {"route": "A", "destination": "North Station", "arrival_time": 5, "status": "On time"},
                {"route": "C", "destination": "South End", "arrival_time": 12, "status": "On time"},
                {"route": "B", "destination": "East Side", "arrival_time": 18, "status": "Delayed +5 min"},
                {"route": "D", "destination": "West Point", "arrival_time": 24, "status": "On time"},
                {"route": "E", "destination": "Airport Express", "arrival_time": 31, "status": "On time"},
            ]
        },
        "BUS002": {
            "name": "Market Square",
            "type": "bus",
            "arrivals": [
                {"route": "42", "destination": "Riverside Park", "arrival_time": 4, "status": "On time"},
                {"route": "7B", "destination": "Medical Center", "arrival_time": 9, "status": "On time"},
                {"route": "33", "destination": "Sports Complex", "arrival_time": 14, "status": "On time"},
                {"route": "14", "destination": "Theater District", "arrival_time": 19, "status": "On time"},
                {"route": "21", "destination": "City Hall", "arrival_time": 26, "status": "Delayed +3 min"},
            ]
        },
        "METRO001": {
            "name": "Civic Center",
            "type": "metro",
            "arrivals": [
                {"route": "Red Line", "destination": "Tech Park", "arrival_time": 2, "status": "On time"},
                {"route": "Blue Line", "destination": "Arts District", "arrival_time": 8, "status": "On time"},
                {"route": "Green Line", "destination": "Zoo Station", "arrival_time": 13, "status": "On time"},
                {"route": "Red Line", "destination": "Industrial Zone", "arrival_time": 20, "status": "On time"},
                {"route": "Yellow Line", "destination": "Beach Terminal", "arrival_time": 28, "status": "On time"},
            ]
        },
    }
}


class TransitAPIClient:
    """Client for querying public transport arrival information."""
    
    # Base URL for the API (can be replaced with real API)
    BASE_URL = "http://api.transit.local/v1"
    
    # Timeout duration in seconds
    TIMEOUT = 10
    
    def __init__(self, use_mock: bool = True):
        """
        Initialize the TransitAPIClient.
        
        Args:
            use_mock: Whether to use mock data (True) or real API (False)
        """
        self.use_mock = use_mock
        self.session = requests.Session()
    
    def get_next_arrivals(self, station_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch the next arrivals for a given station.
        
        Args:
            station_id: The station/stop ID
            limit: Number of arrivals to fetch (default: 5)
            
        Returns:
            List of dictionaries containing arrival information
            
        Raises:
            Various exceptions for different error scenarios
        """
        # Validate station ID
        if not station_id or not station_id.strip():
            raise ValueError("Station ID cannot be empty.")
        
        station_id = station_id.upper().strip()
        
        # Validate limit
        if not isinstance(limit, int) or limit < 1 or limit > 10:
            raise ValueError("Limit must be between 1 and 10.")
        
        if self.use_mock:
            return self._fetch_mock_data(station_id, limit)
        else:
            return self._fetch_real_api(station_id, limit)
    
    def _fetch_mock_data(self, station_id: str, limit: int) -> List[Dict[str, Any]]:
        """
        Fetch mock transit data.
        
        Args:
            station_id: The station/stop ID
            limit: Number of arrivals to fetch
            
        Returns:
            List of arrival dictionaries
        """
        if station_id not in MOCK_TRANSIT_DATA["stops"]:
            raise ValueError(
                f"Invalid station code: '{station_id}'. "
                f"Available stations: {', '.join(MOCK_TRANSIT_DATA['stops'].keys())}"
            )
        
        stop_data = MOCK_TRANSIT_DATA["stops"][station_id]
        arrivals = stop_data["arrivals"][:limit]
        
        # Add metadata
        result = {
            "station_id": station_id,
            "station_name": stop_data["name"],
            "station_type": stop_data["type"],
            "timestamp": datetime.now().isoformat(),
            "arrivals": arrivals
        }
        
        return result
    
    def _fetch_real_api(self, station_id: str, limit: int) -> List[Dict[str, Any]]:
        """
        Fetch data from real transit API.
        
        Args:
            station_id: The station/stop ID
            limit: Number of arrivals to fetch
            
        Returns:
            List of arrival dictionaries
        """
        params = {
            'station_id': station_id,
            'limit': limit
        }
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}/arrivals",
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
                "Failed to connect to the Transit API. "
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
        
        if data.get('status') == 'error':
            error_msg = data.get('message', 'Unknown error occurred.')
            
            if 'station' in error_msg.lower() or 'not found' in error_msg.lower():
                raise ValueError(
                    f"Invalid station code: '{station_id}'. "
                    f"Station not found in the transit system."
                )
            elif 'service unavailable' in error_msg.lower():
                raise ConnectionError(
                    f"Service temporarily unavailable for station '{station_id}'. "
                    "Please try again in a few moments."
                )
            else:
                raise ValueError(f"API Error: {error_msg}")
        
        return data
    
    def format_arrivals_table(self, arrivals_data: Dict[str, Any]) -> str:
        """
        Format arrival data as a readable table.
        
        Args:
            arrivals_data: Dictionary containing arrival information
            
        Returns:
            Formatted table as string
        """
        station_id = arrivals_data.get('station_id', 'N/A')
        station_name = arrivals_data.get('station_name', 'N/A')
        station_type = arrivals_data.get('station_type', 'N/A').title()
        timestamp = arrivals_data.get('timestamp', 'N/A')
        arrivals = arrivals_data.get('arrivals', [])
        
        # Parse timestamp for display
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            time_str = timestamp
        
        # Build table data
        table_data = []
        for idx, arrival in enumerate(arrivals, 1):
            route = arrival.get('route', 'N/A')
            destination = arrival.get('destination', 'N/A')
            arrival_time = arrival.get('arrival_time', 'N/A')
            status = arrival.get('status', 'N/A')
            
            # Format arrival time
            if isinstance(arrival_time, int):
                arrival_mins = f"{arrival_time} min"
            else:
                arrival_mins = arrival_time
            
            table_data.append([idx, route, destination, arrival_mins, status])
        
        # Create the table
        headers = ["#", "Route", "Destination", "Arrival In", "Status"]
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        
        # Build the full output
        output = "\n" + "=" * 80 + "\n"
        output += f"{'TRANSIT ARRIVALS':^80}\n"
        output += "=" * 80 + "\n"
        output += f"Station: {station_name} ({station_id})\n"
        output += f"Type: {station_type} | Updated: {time_str}\n"
        output += "-" * 80 + "\n"
        output += table + "\n"
        output += "=" * 80 + "\n"
        
        return output


def main():
    """Main function to run the transit arrivals script."""
    
    # Get station ID from command line or user input
    if len(sys.argv) > 1:
        station_id = sys.argv[1].strip()
    else:
        print("\nAvailable demo stations:")
        print("  • BUS001  - Central Station (Bus)")
        print("  • TRAIN001 - Grand Central Terminal (Train)")
        print("  • BUS002  - Market Square (Bus)")
        print("  • METRO001 - Civic Center (Metro)")
        print()
        station_id = input("Enter station code: ").strip()
    
    # Optional: get number of arrivals to display
    limit = 5
    if len(sys.argv) > 2:
        try:
            limit = int(sys.argv[2])
        except ValueError:
            print(f"Warning: Invalid limit '{sys.argv[2]}', using default of 5")
    
    # Initialize the API client (using mock data by default)
    client = TransitAPIClient(use_mock=True)
    
    try:
        # Fetch arrivals
        print("\nFetching transit information...")
        arrivals_data = client.get_next_arrivals(station_id, limit)
        
        # Display the results
        formatted_output = client.format_arrivals_table(arrivals_data)
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
