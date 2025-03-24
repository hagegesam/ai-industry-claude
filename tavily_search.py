# tavily_search.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class TavilySearchTool:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/search"

        if not self.api_key:
            print("Warning: TAVILY_API_KEY not found in environment variables.")
            print("Please sign up for a free API key at https://tavily.com")

    def search_industry_ai_cases(self, industry, num_results=5):
        """Search for AI use cases in a specific industry using Tavily AI Search."""
        query = f"cas d'utilisation IA intelligence artificielle dans {industry} études de cas exemples France Europe"

        # Set up the search parameters
        params = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": num_results,
            "include_answer": False,
            "include_domains": ["*.fr", "*.eu", "*.com", "*.org"],
            "include_raw_content": False,
        }

        try:
            response = requests.post(self.base_url, json=params)
            response.raise_for_status()
            data = response.json()

            results = []
            for result in data.get("results", []):
                results.append({
                    "title": result.get("title", ""),
                    "link": result.get("url", ""),
                    "snippet": result.get("content", "")
                })

            return results

        except Exception as e:
            print(f"Error searching with Tavily: {e}")
            return []

    def search_specific_case(self, industry, specific_case):
        """Search for a specific AI use case in an industry."""
        query = f"{specific_case} implémentation IA dans {industry} résultats métriques"
        return self.search_industry_ai_cases(query, 3)

# Usage example:
# search_tool = TavilySearchTool()
# results = search_tool.search_industry_ai_cases("finance", 5)