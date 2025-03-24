# search_utils.py
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import os

load_dotenv()


class IndustrySearchTool:
    def __init__(self):
        self.search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

    def search_industry_ai_cases(self, industry, num_results=5):
        """Search for AI use cases in a specific industry."""
        # Query in French for French results
        query = f"cas d'utilisation IA intelligence artificielle dans {industry} études de cas exemples France Europe"

        try:
            # Get the raw search results
            raw_results = self.search.run(query)

            # Check if it's a string that might be JSON
            if isinstance(raw_results, str):
                try:
                    import json
                    parsed = json.loads(raw_results)
                    if 'organic_results' in parsed:
                        return parsed['organic_results'][:num_results]
                except json.JSONDecodeError:
                    # Not JSON, continue with other handling
                    pass

            # If it's a list of search results already
            if isinstance(raw_results, list):
                return raw_results[:num_results]

            # If it's a dictionary with organic_results
            if isinstance(raw_results, dict) and 'organic_results' in raw_results:
                return raw_results['organic_results'][:num_results]

            # For other formats like plain text, create a dummy result to show the content
            if isinstance(raw_results, str):
                # Split by lines and create fake results
                lines = raw_results.split('\n')
                fake_results = []
                for i, line in enumerate(lines[:num_results]):
                    if line.strip():
                        fake_results.append({
                            'title': f'Result {i + 1}',
                            'link': f'https://example.com/result_{i + 1}',  # Fake URL
                            'snippet': line.strip()
                        })
                return fake_results

            # Fallback: return empty results if none of the above worked
            print("Warning: Could not parse search results properly.")
            return []
        except Exception as e:
            print(f"Error in search: {e}")
            return []

    def search_specific_case(self, industry, specific_case):
        """Search for a specific AI use case in an industry."""
        # Query in French for French results
        query = f"{specific_case} implémentation IA dans {industry} résultats métriques"
        results = self.search.run(query)
        # Parse the results - SerpAPI typically returns a JSON string
        import json
        try:
            parsed_results = json.loads(results)
            # Extract organic results
            if 'organic_results' in parsed_results:
                return parsed_results['organic_results'][:3]
            return []
        except:
            # If not JSON, return as is
            return [{"title": "Result", "link": results, "snippet": results}]