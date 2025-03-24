# main.py
import os
import json
import argparse
import csv
import importlib.util
from processors import ArticleProcessor
from benchmarks import IndustryAnalyzer
from enrichment import QualityEnhancer
from database import DatabaseManager
from dotenv import load_dotenv


# Function to dynamically load a search class based on available modules/api keys
def get_search_tool():
    # Check for Google Custom Search API key first (recommended)
    # if os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID"):
    #     try:
    #         from google_custom_search import GoogleCustomSearch
    #         print("Using Google Custom Search API")
    #         return GoogleCustomSearch()
    #     except ImportError:
    #         print("Google Custom Search module not found. Falling back to other options.")

    # Check for Tavily API key
    if os.getenv("TAVILY_API_KEY"):
        try:
            from tavily_search import TavilySearchTool
            print("Using Tavily AI Search")
            return TavilySearchTool()
        except ImportError:
            print("Tavily search module not found. Falling back to other options.")

    # Check for SerpAPI key
    # if os.getenv("SERPAPI_API_KEY"):
    #     try:
    #         from search_utils import IndustrySearchTool
    #         print("Using SerpAPI for search")
    #         return IndustrySearchTool()
    #     except ImportError:
    #         print("SerpAPI module not found. Falling back to other options.")

    # Try to load DuckDuckGo
    try:
        spec = importlib.util.find_spec('duckduckgo_search')
        if spec:
            from duckduckgo_alternative import IndustrySearchTool
            print("Using DuckDuckGo for search")
            return IndustrySearchTool()
    except:
        print("DuckDuckGo search module not available. Falling back to basic search.")

    # Finally, use the simple Google search as fallback
    try:
        from google_search import SimpleSearchTool
        print("Using Simple Google Search (no API key required)")
        return SimpleSearchTool()
    except ImportError:
        print("Simple search module not found.")
        raise ImportError("No search module available. Please install at least one search option.")


load_dotenv()


def run_industry_benchmark(industry, cases_per_industry=5):
    """Run the benchmark process for a specified industry."""
    print(f"Processing industry: {industry}")

    # Initialize tools
    search_tool = get_search_tool()
    processor = ArticleProcessor()
    analyzer = IndustryAnalyzer()
    enhancer = QualityEnhancer()
    db_manager = DatabaseManager()

    industry_results = []

    # Search for articles about AI in this industry
    search_results = search_tool.search_industry_ai_cases(industry, num_results=cases_per_industry)

    if not search_results:
        print(f"No search results found for industry: {industry}")
        return {"use_cases": [], "benchmark": "No data available for benchmarking."}

    for result in search_results:
        # Check if this is a valid result with a link
        if not isinstance(result, dict):
            print(f"  Skipping invalid result format: {result}")
            continue

        url = result.get('link')
        if not url or not isinstance(url, str) or not url.startswith('http'):
            print(f"  Skipping invalid URL: {url}")
            continue

        try:
            print(f"  Processing article: {url}")

            # Load and process the article
            documents = processor.load_article(url)
            article_content = " ".join([doc.page_content for doc in documents])

            # Check content relevance before in-depth analysis
            if enhancer.filter_relevance(article_content, industry):
                # Extract structured information about the use case
                use_case_info = analyzer.analyze_article_content(article_content, url, industry)

                # Verify information coherence
                coherence = enhancer.verify_coherence(use_case_info, industry)
                print(f"  Coherence check: {coherence}")

                # Enrich information if needed
                enrichment = enhancer.enrich_information(use_case_info, industry)
                print(f"  Enrichment: {enrichment}")

                industry_results.append(use_case_info)
                print(f"  Article processed successfully: {url}")
            else:
                print(f"  Article not relevant for analysis, skipped.")
        except Exception as e:
            print(f"  Error processing {url}: {str(e)}")

    # Perform industry-specific benchmarking
    industry_benchmark = analyzer.compare_industry_use_cases(industry_results, industry)

    # Store results
    results = {
        "use_cases": [uc.model_dump() for uc in industry_results],
        "benchmark": industry_benchmark.content
    }

    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Save results in JSON format
    with open(f"output/benchmark_{industry}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Save results in CSV format
    with open(f"output/benchmark_{industry}.csv", "w", encoding="utf-8", newline='') as f:
        if industry_results:
            fieldnames = [
                "industry", "business_function", "entreprise", "origine_de_la_source",
                "lien", "derniere_mise_a_jour", "processus_impacte", "valeur_economique",
                "gains_attendus_realises", "usage_ia", "technologies_ia_utilisees",
                "partenaires_impliques"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for case in industry_results:
                case_dict = case.dict()
                # Convert lists to strings for CSV
                for key, value in case_dict.items():
                    if isinstance(value, list):
                        case_dict[key] = "; ".join(value)
                writer.writerow(case_dict)

    # Save results to database
    if industry_results:
        use_cases_to_save = [uc.model_dump() for uc in industry_results]
        saved_count = db_manager.save_use_cases(use_cases_to_save)
        print(f"  Saved {saved_count} use cases to database")

    print(f"Benchmark for {industry} completed successfully!")
    return results


def main():
    parser = argparse.ArgumentParser(description='Benchmark of AI use cases by industry')
    parser.add_argument('--industry', type=str, required=True,
                        help='Industry to analyze (e.g., finance, healthcare, automotive)')
    parser.add_argument('--count', type=int, default=5,
                        help='Number of use cases to search for')
    parser.add_argument('--format', type=str, choices=['json', 'csv', 'all'], default='all',
                        help='Output format (json, csv, or all for both)')

    args = parser.parse_args()

    print(f"Starting benchmark for industry: {args.industry}")
    print(f"Searching for {args.count} use cases...")
    print(f"Output format: {args.format}")

    run_industry_benchmark(args.industry, args.count)


if __name__ == "__main__":
    main()