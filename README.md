# LocalRankLens

A competitive intelligence tool for digital marketing consultants and agencies. LocalRankLens simulates local search engine results for target cities and keyword sets, providing actionable insights for sales pitches, SEO strategy, and paid media planning.

## Features

- **Local Search Simulation**: Query Google search results for specific cities and keywords
- **Competitive Intelligence**: Extract top Google Maps listings, Local Services Ads, and organic results
- **Professional Reporting**: Generate client-ready HTML reports with organized data
- **Flexible Configuration**: JSON-based configuration for easy customization
- **Error Handling**: Robust error handling and retry logic for API calls

## Quick Start

### Prerequisites

- Python 3.10 or higher
- SerpAPI account and API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd NCDLRL1
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.template .env
# Edit .env and add your SERPAPI_KEY
```

5. Configure your search parameters:
```bash
# Edit config.json with your business details and keywords
```

### Usage

```bash
python src/localranklens.py
```

Reports will be generated in the `output/` directory.

## Configuration

Edit `config.json` to customize:

- **business_name**: Your client's business name
- **location**: Target city and state
- **keywords**: Organized by category (core, upsell, emergency)
- **output_prefix**: Filename prefix for reports
- **report_settings**: Control what data to include in reports

## Project Structure

```
NCDLRL1/
├── src/                    # Source code
│   ├── localranklens.py   # Main orchestrator
│   ├── config_manager.py  # Configuration handling
│   ├── search_scraper.py  # SerpAPI integration
│   ├── data_processor.py  # Data extraction and processing
│   └── report_writer.py   # HTML report generation
├── tests/                 # Test suite
├── output/                # Generated reports
├── docs/                  # Documentation
├── config.json           # Configuration file
├── requirements.txt       # Python dependencies
└── .env.template         # Environment variables template
```

## Development

### Running Tests

```bash
pytest tests/ -v --cov=src
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

[Add your license information here]
