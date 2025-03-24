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

## Step 5: Running the Benchmark

```bash
# Basic usage
python main.py --industry finance

# Specify number of use cases to search for
python main.py --industry healthcare --count 10

# Specify output format (json, csv, or all)
python main.py --industry automotive --format json
```

## Database Support

The tool now supports storing AI use cases in a database. By default, it uses SQLite, but you can configure it to use other databases like PostgreSQL or MySQL.

### Supported Databases:
- SQLite (default)
- PostgreSQL
- MySQL
- MongoDB (coming soon)

### Database Features:
- Automatic schema creation
- Efficient storage of use cases
- Easy retrieval by industry
- Data persistence between runs
- Support for all use case fields

### Using Different Databases

To use a different database, update the `DATABASE_URL` in your `.env` file:

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/ai_use_cases

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/ai_use_cases

# SQLite (default)
DATABASE_URL=sqlite:///ai_use_cases.db
```

## Available Industries to Benchmark

You can analyze any industry, for example:
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

### Error: "No module named 'X'"
```bash
pip install X
```

### Search-related errors
Try switching to a different search provider by obtaining the appropriate API key and adding it to your `.env` file.

### Database errors
1. Ensure your database server is running
2. Check your database credentials in the `.env` file
3. Verify you have the correct database driver installed
4. Make sure the database exists (for PostgreSQL/MySQL)

### Rate limiting errors
Some search providers may impose rate limits. If you encounter rate limiting, try:
1. Using a different search provider
2. Reducing the number of requests (lower the `--count` parameter)
3. Adding delays between requests (edit the code to add `time.sleep(3)` between searches)
