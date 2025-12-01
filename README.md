# datablockAPI

A comprehensive Python package for working with D&B Direct+ API data, providing easy access to company information, financial data, and legal events.

## Architecture Overview

datablockAPI follows a **separated concerns architecture** with clear separation between data acquisition and data processing:

### 1. Client Request Functions (API → JSON)
**Purpose**: Request raw responses from D&B Direct+ API and save as JSON files locally

- `request_company_info()` - Requests company information and saves raw JSON
- `request_company_financials()` - Requests financial data and saves raw JSON
- `request_events_filings()` - Requests events/filings data and saves raw JSON
- `request_all_data()` - Requests all data blocks and saves raw JSON files

**Key Point**: These methods ONLY handle API communication and raw JSON storage. No data parsing or database operations.

### 2. Loader Functions (JSON → Database)
**Purpose**: Parse JSON files and load structured data into database tables

- `load()` - Load JSON files into database with automatic data parsing and model creation
- Handles all data transformation from raw API responses to structured database records
- Supports batch loading and incremental updates

**Key Point**: The loader handles all data parsing, validation, and database insertion.

## Features

- **Separated Concerns Architecture**: Clear separation between API requests and data processing
- **API Client**: Robust client for D&B Direct+ API with retry logic and rate limiting
- **Data Models**: Complete SQLAlchemy models for storing and querying D&B data
- **Data Loading**: Efficient loading of JSON data into structured database tables
- **Configuration**: Centralized configuration management with environment variable support
- **Error Handling**: Custom exceptions and comprehensive error handling
- **Logging**: Structured logging throughout the package
- **Health Checks**: System health monitoring and diagnostics
- **Metrics**: Basic metrics collection for API usage monitoring

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from datablockAPI.api import DNBAPIClient
import datablockAPI as api
import pandas as pd

# Initialize client and database
client = DNBAPIClient()
api.init(database='sqlite:///datablock.db')

# Phase 1: Request data from D&B API (saves raw JSON files)
duns_list = ['540924028', '315369934', '060704780']

for duns in duns_list:
    print(f"Requesting data for DUNS: {duns}")
    
    # These methods ONLY request API data and save raw JSON files
    client.request_company_info(duns, output_dir='company_data')
    client.request_events_filings(duns, output_dir='events_data')
    # Note: Financial data may require premium subscription

# Phase 2: Load JSON files into database (parses and structures data)
import glob
api.load(glob.glob('company_data/*.json'))
api.load(glob.glob('events_data/*.json'))

# Phase 3: Query the structured database
session = api.get_session()

# Example queries using pandas
from datablockAPI.core.models import Company, CompanyInfo

query = session.query(
    Company.duns,
    Company.primary_name,
    CompanyInfo.start_date,
    CompanyInfo.operating_status_description
).join(CompanyInfo)

df_companies = pd.read_sql(query.statement, session.bind)
print(df_companies.head())
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

## Health Checks

```python
from datablockAPI.health import health_check

# Check system health
status = health_check()
print(status)
```

## API Reference

### DNBAPIClient - Request Functions (API → JSON)

These methods ONLY request data from D&B API and save raw JSON responses to local files:

- `request_data_blocks(duns, block_ids, output_dir="dnb_data")`: Request specific data blocks by ID
- `request_company_info(duns, output_dir="dnb_data")`: Request company information only
- `request_company_financials(duns, output_dir="dnb_data")`: Request financial data only
- `request_events_filings(duns, output_dir="dnb_data")`: Request events and filings only
- `request_all_data(duns, output_dir="dnb_data")`: Request all data blocks

### Loader Functions (JSON → Database)

These functions parse JSON files and load structured data into database tables:

- `api.load(json_files)`: Load JSON file(s) into database with automatic parsing
- `api.load_json_to_db(json_files)`: Alternative loading method

### Query Examples

Once data is loaded into the database, you can query it using SQLAlchemy and pandas:

```python
import datablockAPI as api
import pandas as pd
from datablockAPI.core.models import Company, CompanyInfo, LegalEventsSummary

# Get database session
session = api.get_session()

# Example 1: Basic company information
query = session.query(
    Company.duns,
    Company.primary_name,
    CompanyInfo.start_date,
    CompanyInfo.operating_status_description,
    CompanyInfo.primary_address_locality,
    CompanyInfo.primary_address_country
).join(CompanyInfo)

df_companies = pd.read_sql(query.statement, session.bind)
print("Company Information:")
print(df_companies.head())

# Example 2: Legal events summary
query = session.query(
    Company.primary_name,
    LegalEventsSummary.has_liens,
    LegalEventsSummary.has_judgments,
    LegalEventsSummary.has_suits,
    LegalEventsSummary.has_bankruptcy
).join(LegalEventsSummary)

df_legal = pd.read_sql(query.statement, session.bind)
print("\\nLegal Events Summary:")
print(df_legal.head())
```

### Separated Concerns Architecture

datablockAPI follows a **separated concerns** design pattern that clearly separates data acquisition from data storage:

#### Request Phase (API → JSON)
- **Purpose**: Fetch data from D&B Direct+ API and save to JSON files
- **Methods**: `client.request_*()` methods
- **Output**: Raw JSON files with complete API responses
- **Benefits**:
  - Independent of database operations
  - Can retry failed requests without affecting stored data
  - JSON files serve as permanent data backup
  - Can process data offline after initial requests

#### Load Phase (JSON → Database)
- **Purpose**: Parse JSON files and populate structured database tables
- **Methods**: `api.load()` functions
- **Input**: Raw JSON files from request phase
- **Benefits**:
  - Independent of API availability
  - Can reload data without re-requesting from API
  - Enables data validation and transformation
  - Supports incremental loading and updates

#### Workflow Example
```python
# Phase 1: Request data (requires API access)
client.request_company_info('540924028', output_dir='data')
client.request_events_filings('540924028', output_dir='data')

# Phase 2: Load data (can be done anytime, even offline)
api.load(glob.glob('data/*.json'))

# Phase 3: Query data (always available once loaded)
session = api.get_session()
# ... run queries as shown in examples above
```

## Data Models and Schema

datablockAPI uses a comprehensive SQLAlchemy-based data model with **56+ tables** organized around core business entities. The schema captures all aspects of D&B company data including legal events, financial statements, and business metadata.

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

Captures various types of legal proceedings and filings:

#### Event Types & Tables
- **Liens**: `Lien` → `LienFiling` → `LienFilingRolePlayer`
- **Judgments**: `Judgment` → `JudgmentFiling` → `JudgmentFilingRolePlayer`
- **Suits**: `Suit` → `SuitFiling` → `SuitFilingRolePlayer`
- **Bankruptcies**: `Bankruptcy` → `BankruptcyFiling` → `BankruptcyFilingRolePlayer`
- **Claims**: `Claim` → `ClaimFiling` → `ClaimFilingRolePlayer`

#### Legal Events Summary
- **LegalEventsSummary**: High-level counts and status flags for all legal event types

### Financial Data System

#### FinancialStatement
Core financial reporting entity containing balance sheets, income statements, and cash flow data.
- **Relationships**:
  - `FinancialOverview`: Summary financial metrics and ratios
  - `BalanceSheetItem`: Individual balance sheet line items
  - `ProfitLossItem`: Income statement items
  - `CashFlowItem`: Cash flow statement items
  - `FinancialRatio`: Calculated financial ratios

### Company Metadata Tables

#### Industry & Business Classification
- **IndustryCode**: SIC/NAICS industry classifications with descriptions
- **UNSPSCCode**: United Nations product/service codes
- **CompanyActivity**: Business activities and operations descriptions

#### Contact & Location
- **WebsiteAddress**: Company websites and URLs
- **TelephoneNumber**: Phone numbers with international dialing codes
- **EmailAddress**: Email addresses
- **RegistrationNumber**: Business registration numbers by jurisdiction
- **StockExchange**: Stock exchange listings and ticker symbols

#### Human Resources
- **EmployeeFigure**: Headcount and employee information with date ranges

#### Trade & Legal
- **TradeStyleName**: Alternative company names and tradestyles
- **MultilingualName**: Company names in different languages
- **Bank**: Banking relationships

### Events & Activities

#### Significant Events
- **SignificantEvent**: Major corporate events (mergers, acquisitions, disasters, etc.)
- **SignificantEventTextEntry**: Detailed descriptions and impact details

#### Awards & Contracts
- **AwardsSummary**: Summary of government contracts and awards
- **Contract**: Individual contract details with amounts and agencies
- **ContractAction**: Contract modifications and funding actions
- **ContractCharacteristic**: Contract classifications and types

#### Financing Events
- **FinancingEventsSummary**: Summary of financing activities
- **FinancingEvent**: Individual financing events (loans, grants, debts)
- **FinancingEventFiling**: Specific financing filings and UCC records

### Risk & Compliance

#### Exclusions
- **ExclusionsSummary**: Government exclusion status and counts
- **ActiveExclusion**: Individual active exclusion records with agencies and dates

### Entity Relationship Diagram

```
Company (1) ──── (1) CompanyInfo
    │                    │
    ├── (1) LegalEventsSummary
    ├── (*) Lien ─── (*) LienFiling ─── (*) LienFilingRolePlayer
    ├── (*) Judgment ─── (*) JudgmentFiling ─── (*) JudgmentFilingRolePlayer
    ├── (*) Suit ─── (*) SuitFiling ─── (*) SuitFilingRolePlayer
    ├── (*) Bankruptcy ─── (*) BankruptcyFiling ─── (*) BankruptcyFilingRolePlayer
    ├── (*) Claim ─── (*) ClaimFiling ─── (*) ClaimFilingRolePlayer
    ├── (1) FinancialStatement ─── (1) FinancialOverview
    │                              ├── (*) BalanceSheetItem
    │                              ├── (*) ProfitLossItem
    │                              ├── (*) CashFlowItem
    │                              └── (*) FinancialRatio
    ├── (*) SignificantEvent ─── (*) SignificantEventTextEntry
    ├── (1) AwardsSummary ─── (*) Contract ─── (*) ContractAction
    │                        └── (*) ContractCharacteristic
    ├── (1) FinancingEventsSummary ─── (*) FinancingEvent ─── (*) FinancingEventFiling
    └── (1) ExclusionsSummary ─── (*) ActiveExclusion
```

### Key Relationships

- **One-to-One**: Company ↔ CompanyInfo, Company ↔ Summary tables
- **One-to-Many**: Company → Events, FinancialStatement → Financial line items
- **Many-to-Many**: Companies can have multiple industry codes, activities, contacts, etc.
- **Hierarchical**: Events → Filings → Role Players/Text Entries

### Database Schema Features

- **56+ tables** with proper foreign key relationships
- **Comprehensive indexing** on frequently queried fields (DUNS, dates, codes)
- **Data integrity constraints** ensuring referential integrity
- **Audit fields** (`created_at`, `updated_at`) on all tables
- **Support for complex queries** across company data, legal events, and financial performance

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

# Type checking (optional - not required for CI)
mypy datablockAPI/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive documentation for new functionality
4. Ensure code follows the established patterns and architecture
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.</content>
<parameter name="filePath">c:\Users\jun\dataground\README.md