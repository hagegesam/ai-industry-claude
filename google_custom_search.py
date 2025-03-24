# google_custom_search.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class GoogleCustomSearch:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cx = os.getenv("GOOGLE_CSE_ID")  # Custom Search Engine ID

        if not self.api_key or not self.cx:
            print("Warning: GOOGLE_API_KEY or GOOGLE_CSE_ID not found in environment variables.")
            print("Please set up a Google Custom Search Engine at https://programmablesearchengine.google.com/")

    def search_industry_ai_cases(self, industry, num_results=5):
        """Search for AI use cases in a specific industry using Google Custom Search."""
        query = f"cas d'utilisation IA intelligence artificielle dans {industry} études de cas exemples France Europe"

        # Set up the search parameters
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": min(num_results, 10),  # Google CSE allows max 10 results per request
            "lr": "lang_fr",  # Restrict to French language
            "gl": "fr"  # Set geolocation to France
        }

        try:
            response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("items", []):
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })

            return results

        except Exception as e:
            print(f"Error searching with Google Custom Search: {e}")
            return []

    def search_specific_case(self, industry, specific_case):
        """Search for a specific AI use case in an industry."""
        query = f"{specific_case} implémentation IA dans {industry} résultats métriques"
        return self.search_industry_ai_cases(query, 3)

# Usage example:
# search_tool = GoogleCustomSearch()
# results = search_tool.search_industry_ai_cases("finance", 5)