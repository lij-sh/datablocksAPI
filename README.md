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

# Initialize client
client = DNBAPIClient()

# Step 1: Initialize database (creates all tables)
client.init_database('datablock.db')

# Step 2: Request data for multiple companies (saves to JSON files)
duns_list = ['540924028', '315369934', '060704780']

for duns in duns_list:
    # Request company information
    client.request_company_info(duns, output_dir='company_data')
    
    # Request financial data
    client.request_company_financials(duns, output_dir='financial_data')
    
    # Request events and filings
    client.request_events_filings(duns, output_dir='events_data')

# Step 3: Load JSON files into database
import glob
client.load_json_to_db(glob.glob('company_data/*.json'))
client.load_json_to_db(glob.glob('financial_data/*.json'))
client.load_json_to_db(glob.glob('events_data/*.json'))

# Step 4: Query the database
companies = client.query_companies(limit=5)
for company in companies:
    print(f"{company['duns']}: {company['primary_name']}")
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
from datablockAPI.api import DNBAPIClient

# Initialize client
client = DNBAPIClient()

# Create and initialize database with all tables
client.init_database('datablock.db')

# Or connect to existing database
client.init_database('existing.db', create_if_not_exists=False)

# Load JSON data files into database
client.load_json_to_db(['company_data/company1.json', 'company_data/company2.json'])
# Or load all files from a directory
import glob
client.load_json_to_db(glob.glob('company_data/*.json'))
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

Main client for interacting with D&B Direct+ API using a separated concerns architecture.

#### Database Management

- `init_database(database_path, create_if_not_exists=True)`: Initialize database connection and create all tables
- `get_session()`: Get SQLAlchemy session for direct database queries

#### Data Request Methods (API → JSON)

These methods request data from D&B API and save responses to JSON files. They do NOT load data into the database.

- `request_data_blocks(duns, block_ids, output_dir="dnb_data")`: Request specific data blocks by ID
- `request_company_info(duns, output_dir="dnb_data")`: Request company information only
- `request_company_financials(duns, output_dir="dnb_data")`: Request financial data only
- `request_events_filings(duns, output_dir="dnb_data")`: Request events and filings only
- `request_all_data(duns, output_dir="dnb_data")`: Request all data blocks

#### Data Loading Methods (JSON → Database)

These methods load previously saved JSON files into the database. They do NOT make API calls.

- `load_json_to_db(json_files)`: Load JSON file(s) into database tables

#### Query Methods

- `query_companies(limit=None, filters=None)`: Query companies with optional filters
- `query_company_by_duns(duns)`: Get company details by DUNS number

### Separated Concerns Architecture

The datablockAPI follows a **separated concerns** design pattern that clearly separates data acquisition from data storage:

#### Request Phase (API → JSON)
- **Purpose**: Fetch data from D&B Direct+ API and save to JSON files
- **Methods**: `request_*()` methods
- **Benefits**: 
  - Independent of database operations
  - Can retry failed requests without affecting stored data
  - JSON files serve as permanent data backup
  - Can process data offline after initial requests

#### Load Phase (JSON → Database)
- **Purpose**: Parse JSON files and populate structured database tables
- **Methods**: `load_json_to_db()`
- **Benefits**:
  - Independent of API availability
  - Can reload data without re-requesting from API
  - Enables data validation and transformation
  - Supports incremental loading and updates

#### Workflow Example
```python
# Phase 1: Request data (can be done when API is available)
client.request_company_info('540924028', output_dir='company_data')
client.request_events_filings('540924028', output_dir='events_data')

# Phase 2: Load data (can be done anytime, even offline)
client.load_json_to_db(glob.glob('company_data/*.json'))
client.load_json_to_db(glob.glob('events_data/*.json'))

# Phase 3: Query data (always available once loaded)
companies = client.query_companies()
```

### Data Models

Complete SQLAlchemy models for:
- Companies
- Company Information
- Industry Codes
- Legal Events (Liens, Judgments, Suits, etc.)
- Financial Statements
- Significant Events
- Exclusions

## Data Models and Entity Relationships

The datablockAPI uses a comprehensive SQLAlchemy-based data model to represent D&B company data. The database schema consists of 56+ tables organized around core business entities.

### Core Entities

#### Company
The central entity representing a business organization.
- **Primary Key**: `id` (auto-increment)
- **Natural Key**: `duns` (9-digit D&B D-U-N-S number)
- **Attributes**: `primary_name`, `country_iso_alpha2_code`, `created_at`, `updated_at`

#### CompanyInfo
Detailed company information and metadata linked to each Company.
- **Relationship**: One-to-one with Company
- **Contains**: Business characteristics, legal information, operating status, addresses, industry classifications

### Legal Events System

The legal events system captures various types of legal proceedings and filings:

#### Event Types
- **Liens**: Security interests and claims against company assets
- **Judgments**: Court-ordered financial obligations
- **Suits**: Legal proceedings and lawsuits
- **Bankruptcies**: Insolvency proceedings
- **Claims**: Various legal claims and disputes

#### Event Structure
Each event type follows a consistent pattern:
- **Summary Table**: High-level counts and status (e.g., `LegalEventsSummary`)
- **Event Table**: Individual events (e.g., `Lien`, `Judgment`)
- **Filing Table**: Specific legal filings (e.g., `LienFiling`, `JudgmentFiling`)
- **Role Players**: Parties involved in the event
- **Reference Dates**: Important dates related to the event
- **Text Entries**: Detailed descriptions and notes

### Financial Data System

#### FinancialStatement
Core financial reporting entity containing balance sheets, income statements, and cash flow data.
- **Relationships**:
  - `FinancialOverview`: Summary financial metrics
  - `BalanceSheetItem`: Individual balance sheet line items
  - `ProfitLossItem`: Income statement items
  - `CashFlowItem`: Cash flow statement items
  - `FinancialRatio`: Calculated financial ratios

### Company Metadata

#### Industry & Business Classification
- **IndustryCode**: SIC/NAICS industry classifications
- **UNSPSCCode**: United Nations product/service codes
- **CompanyActivity**: Business activities and operations

#### Contact & Location
- **WebsiteAddress**: Company websites and URLs
- **RegistrationNumber**: Business registration numbers by jurisdiction

#### Human Resources
- **EmployeeFigure**: Headcount and employee information

### Events & Activities

#### Significant Events
- **SignificantEvent**: Major corporate events (mergers, acquisitions, etc.)
- **SignificantEventTextEntry**: Detailed descriptions of events

#### Awards & Contracts
- **AwardsSummary**: Summary of government contracts and awards
- **Contract**: Individual contract details
- **ContractAction**: Contract modifications and updates

#### Financing Events
- **FinancingEventsSummary**: Summary of financing activities
- **FinancingEvent**: Individual financing events (UCC filings, etc.)
- **FinancingEventFiling**: Specific financing filings

### Risk & Compliance

#### Exclusions
- **ExclusionsSummary**: Government exclusion status
- **Exclusion**: Individual exclusion records

### Entity Relationship Diagram Overview

```
Company (1) ──── (1) CompanyInfo
    │                    │
    ├── (1) LegalEventsSummary
    ├── (*) Lien ─── (*) LienFiling
    ├── (*) Judgment ─── (*) JudgmentFiling
    ├── (*) Suit ─── (*) SuitFiling
    ├── (*) Bankruptcy ─── (*) BankruptcyFiling
    ├── (*) Claim ─── (*) ClaimFiling
    ├── (1) FinancialStatement ─── (1) FinancialOverview
    │                              ├── (*) BalanceSheetItem
    │                              ├── (*) ProfitLossItem
    │                              ├── (*) CashFlowItem
    │                              └── (*) FinancialRatio
    ├── (*) SignificantEvent ─── (*) SignificantEventTextEntry
    ├── (1) AwardsSummary ─── (*) Contract ─── (*) ContractAction
    ├── (1) FinancingEventsSummary ─── (*) FinancingEvent ─── (*) FinancingEventFiling
    └── (1) ExclusionsSummary ─── (*) Exclusion
```

### Key Relationships

- **One-to-One**: Company ↔ CompanyInfo, Company ↔ [Summary Tables]
- **One-to-Many**: Company → Events, FinancialStatement → Financial Items
- **Many-to-Many**: Companies can have multiple industry codes, activities, etc.
- **Hierarchical**: Events → Filings → Role Players/Text Entries

### Database Schema

The complete schema includes:
- **56+ tables** with proper foreign key relationships
- **Comprehensive indexing** on frequently queried fields (DUNS, dates, codes)
- **Data integrity constraints** ensuring referential integrity
- **Audit fields** (created_at, updated_at) on all tables

This relational structure enables complex queries across company data, legal events, financial performance, and business intelligence analysis.

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