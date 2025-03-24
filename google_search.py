# google_search.py
import requests
from bs4 import BeautifulSoup
import random
import time


class SimpleSearchTool:
    def __init__(self):
        # List of user agents to rotate
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
        ]

    def _get_random_user_agent(self):
        return random.choice(self.user_agents)

    def search_industry_ai_cases(self, industry, num_results=5):
        """Search for AI use cases in a specific industry using Google."""
        query = f"cas d'utilisation IA intelligence artificielle dans {industry} études de cas exemples France Europe"
        encoded_query = '+'.join(query.split())
        url = f"https://www.google.com/search?q={encoded_query}&num={num_results + 5}&hl=fr"

        headers = {'User-Agent': self._get_random_user_agent()}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []

        # Find all search result containers
        for result in soup.select('div.g'):
            # Extract title
            title_element = result.select_one('h3')
            title = title_element.text if title_element else "No title"

            # Extract URL
            link_element = result.select_one('a')
            link = link_element.get('href', '') if link_element else ""
            if link.startswith('/url?q='):
                link = link.split('/url?q=')[1].split('&sa=')[0]

            # Extract snippet
            snippet_element = result.select_one('div.VwiC3b')
            snippet = snippet_element.text if snippet_element else "No snippet"

            if link and not link.startswith('/'):
                search_results.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet
                })

            if len(search_results) >= num_results:
                break

        # Add a small delay to avoid rate limiting
        time.sleep(1)
        return search_results

    def search_specific_case(self, industry, specific_case, num_results=3):
        """Search for a specific AI use case in an industry."""
        query = f"{specific_case} implémentation IA dans {industry} résultats métriques"

        # Reuse the same search method with different query
        return self.search_industry_ai_cases(query, num_results)

# Usage example:
# search_tool = SimpleSearchTool()
# results = search_tool.search_industry_ai_cases("finance", 5)