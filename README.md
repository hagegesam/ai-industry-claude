# AI Industry Benchmark with Claude

A comprehensive tool for benchmarking AI use cases across different industries, powered by Claude and other AI agents.

This guide will help you set up and run the AI Industry Benchmark tool, which collects and analyzes AI use cases across different industries.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Step 1: Clone the Repository

```bash
git clone https://github.com/hagegesam/ai-industry-claude.git
cd ai-industry-claude
```

Or create a new directory and add the Python files manually.

## Step 2: Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

## Step 3: Install Required Packages

### Basic Installation (with OpenAI)

```bash
pip install -r requirements.txt
```

### Choose a Search Provider (Install at least one)

#### Option 1: Tavily AI Search (Recommended)
```bash
pip install tavily-python
```

#### Option 2: SerpAPI
```bash
pip install google-search-results
```

#### Option 3: DuckDuckGo
```bash
pip install duckduckgo-search
```

#### Option 4: Basic Google Search (No API key needed)
```bash
# No additional packages needed beyond the basic installation
```

## Step 4: Set Up API Keys and Database

Create a `.env` file in the project root directory with the following content:

```
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (choose at least one)
TAVILY_API_KEY=your_tavily_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here

# Database Configuration (Optional)
DATABASE_URL=sqlite:///ai_use_cases.db  # Default SQLite database
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/ai_use_cases
# For MySQL:
# DATABASE_URL=mysql://user:password@localhost:3306/ai_use_cases
```

### API Key Sources:

- **OpenAI API Key**: https://platform.openai.com/
- **Tavily API Key** (Recommended): https://tavily.com/ (Free tier available)
- **SerpAPI Key**: https://serpapi.com/ (Free trial available)

## Step 5: Running the Tool

### Command Line Interface
```bash
# Basic usage
python main.py --industry finance

# Specify number of use cases
python main.py --industry healthcare --count 10

# Specify output format
python main.py --industry automotive --format json
```

### Web Interface
```bash
# Start the Flask application
python app.py

# Open in browser: http://localhost:5000
```

## Output Fields

Each AI use case includes:
- `industry`: Industry sector
- `business_function`: Business function impacted
- `origine_de_la_source`: Source type
- `lien`: Source URL
- `derniere_mise_a_jour`: Last update date
- `processus_impacte`: Impacted business processes
- `gains_attendus_realises`: Expected or realized gains
- `usage_ia`: AI usage description
- `technologies_ia_utilisees`: AI technologies used
- `partenaires_impliques`: Implementation partners

## Database Support

The tool supports multiple database backends:
- SQLite (default)
- PostgreSQL
- MySQL
- MongoDB (coming soon)

### Features
- Automatic schema creation
- Efficient storage and retrieval
- Industry-based filtering
- Web interface for browsing use cases

## Available Industries

Examples include:
- finance
- healthcare
- automotive
- retail
- manufacturing
- telecom
- insurance
- education
- energy
- logistics

## Troubleshooting

### Module Import Issues
```bash
pip install <missing_module>
```

### Search Provider Issues
1. Verify API keys in `.env`
2. Try alternative search providers
3. Check provider-specific quotas and limits

### Database Issues
1. Verify database server is running
2. Check credentials in `.env`
3. Install appropriate database driver
4. Create database if using PostgreSQL/MySQL

### Rate Limiting
1. Switch to a different search provider
2. Reduce request count (`--count` parameter)
3. Add delays between requests
4. Use the web interface for browsing existing results
