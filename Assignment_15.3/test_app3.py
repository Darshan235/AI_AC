import unittest
import requests

class SearchAPITests(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = "http://localhost:5000"

    def test_search_by_name(self):
        """Test search by name functionality"""
        response = requests.get(f"{self.BASE_URL}/search", params={"name": "laptop"})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["name"], "Laptop")

    def test_search_by_category(self):
        """Test search by category functionality"""
        response = requests.get(f"{self.BASE_URL}/search", params={"category": "electronics"})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["count"], 3)

    def test_search_by_price_range(self):
        """Test search by price range functionality"""
        response = requests.get(
            f"{self.BASE_URL}/search", 
            params={"min_price": "100", "max_price": "800"}
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["count"], 2)

    def test_combined_search(self):
        """Test combined search parameters"""
        response = requests.get(
            f"{self.BASE_URL}/search", 
            params={"category": "electronics", "max_price": "500"}
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["count"], 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)