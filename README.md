# datablockAPI

A comprehensive Python package for working with D&B Direct+ API data, providing easy access to company information, financial data, and legal events.

## Features

- **API Client**: Robust client for D&B Direct+ API with retry logic and rate limiting
- **Data Models**: Complete SQLAlchemy models for storing and querying D&B data
- **Data Loading**: Efficient loading of JSON data into structured database tables
- **Configuration**: Centralized configuration management with environment variable support
- **Error Handling**: Custom exceptions and comprehensive error handling
- **Logging**: Structured logging throughout the package
- **Health Checks**: System health monitoring and diagnostics
- **Metrics**: Basic metrics collection for API usage monitoring
- **Testing**: Comprehensive test suite with unit and integration tests

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from datablockAPI.api import DNBAPIClient

# Initialize client (reads from environment variables)
client = DNBAPIClient()

# Get company information
company_data = client.get_company_info('540924028')

# Get all data blocks at once
all_data = client.get_all_blocks('540924028')
```

## Configuration

Set the following environment variables:

```bash
# Required
DNB_API_KEY=your_api_key
DNB_API_SECRET=your_api_secret

# Optional
DATABASE_URL=sqlite:///datablock.db
DNB_API_URL=https://plus.dnb.com
LOG_LEVEL=INFO
```

## Database Setup

```python
import datablockAPI as api

# Initialize database
api.init(database='sqlite:///datablock.db')

# Load data from JSON files
api.load(['path/to/companyinfo.json', 'path/to/financials.json'])
```

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=datablockAPI tests/
```

## Health Checks

```python
from datablockAPI.health import health_check

# Check system health
status = health_check()
print(status)
```

## API Reference

### DNBAPIClient

Main client for interacting with D&B Direct+ API.

#### Methods

- `authenticate()`: Authenticate and get access token
- `get_data_blocks(duns, block_ids, ...)`: Get specific data blocks
- `get_company_info(duns)`: Get company information
- `get_events_filings(duns)`: Get legal events and filings
- `get_financials(duns)`: Get financial data
- `get_all_blocks(duns)`: Get all common data blocks

### Data Models

Complete SQLAlchemy models for:
- Companies
- Company Information
- Industry Codes
- Legal Events (Liens, Judgments, Suits, etc.)
- Financial Statements
- Significant Events
- Exclusions

## Error Handling

The package provides custom exceptions:

- `AuthenticationError`: API authentication failures
- `RateLimitError`: API rate limit exceeded
- `APIError`: General API errors
- `ValidationError`: Data validation failures
- `DatabaseError`: Database operation failures
- `ConfigurationError`: Configuration issues

## Development

### Code Quality

```bash
# Format code
black datablockAPI/

# Lint code
ruff check datablockAPI/

# Type checking
mypy datablockAPI/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.</content>
<parameter name="filePath">c:\Users\jun\dataground\README.md