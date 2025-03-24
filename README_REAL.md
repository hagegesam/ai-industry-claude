# AI Industry Benchmark Tool

This tool helps create a benchmark of AI use cases in specific industries by:
1. Searching for relevant articles and case studies
2. Analyzing the content to extract structured information
3. Generating a comprehensive benchmark

## Key Features

- **Industry-specific search**: Target any industry (finance, healthcare, etc.)
- **French output**: All results and analysis are in French
- **Structured data**: Detailed information on each AI use case
- **Quality enhancement**: Filtering, coherence checking, and enrichment
- **Multiple output formats**: JSON and CSV for easy integration

## Quick Start

1. Install dependencies:
   ```bash
   pip install langchain-core langchain-community langchain-openai langchain-text-splitters python-dotenv requests beautifulsoup4
   ```

2. Set up your API keys in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_key_here
   
   # Choose one of these search API options:
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_CSE_ID=your_custom_search_engine_id
   
   # OR
   TAVILY_API_KEY=your_tavily_key_here
   
   # OR
   SERPAPI_API_KEY=your_serpapi_key_here
   ```

3. Run the benchmark:
   ```bash
   python main.py --industry finance
   ```

## Search Options (in order of recommendation)

1. **Google Custom Search API** (Recommended)
   - Free tier: 100 queries per day
   - Setup: https://programmablesearchengine.google.com/
   - Add to .env: `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`

2. **Tavily AI Search**
   - Smart search specifically designed for AI applications
   - Free tier available
   - Setup: https://tavily.com/
   - Add to .env: `TAVILY_API_KEY`

3. **SerpAPI**
   - Paid service with free trial
   - Setup: https://serpapi.com/
   - Add to .env: `SERPAPI_API_KEY`

4. **DuckDuckGo** (Free, no API key)
   - Install: `pip install duckduckgo-search`

5. **Basic Google Search** (Free, no API key, fallback)
   - No setup required, but less reliable

## Output Fields

For each AI use case, the benchmark collects:

- `industry`: Industry sector
- `business_function`: Business function impacted
- `entreprise`: Company implementing the solution
- `origine_de_la_source`: Source type
- `lien`: Source URL
- `derniere_mise_a_jour`: Last update date
- `processus_impacte`: Impacted business processes
- `valeur_economique`: Economic value
- `gains_attendus_realises`: Expected or realized gains
- `usage_ia`: AI usage description
- `technologies_ia_utilisees`: AI technologies used
- `partenaires_impliques`: Implementation partners

## Troubleshooting

### No search results or connection errors

If you encounter issues with search results, try:

1. **Switch search providers**: Update your .env file with a different API key
2. **Check API key validity**: Ensure your API key is active and correctly entered
3. **Update code**: Make sure you're using the latest version of the code files

### Google Custom Search Setup Instructions

1. Go to https://programmablesearchengine.google.com/
2. Click "Add" to create a new search engine
3. Select "Search the entire web" 
4. Give it a name (e.g., "AI Use Cases Search")
5. Once created, find your Search Engine ID (cx) on the setup page
6. Get an API key from https://console.cloud.google.com/apis/credentials
7. Add both to your .env file

```
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CSE_ID=your_search_engine_id_here
```

## Examples

```bash
# Finance industry benchmark
python main.py --industry finance --count 7

# Healthcare industry with JSON output only
python main.py --industry sante --format json

# Manufacturing industry
python main.py --industry fabrication --count 10
```