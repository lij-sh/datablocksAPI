# DataBlock API

Python SQLAlchemy ORM wrapper for D&B DataBlock API data with comprehensive data loading and querying capabilities.

## Features

- **Complete Schema Coverage**: 50+ database tables covering all D&B DataBlock entities
- **Company Information**: Comprehensive company data with 80+ fields
  - Core identifiers, business characteristics, legal information
  - Operating status, dates, contact information
  - Three complete addresses (primary, mailing, registered) with geolocation
  - Industry codes (NAICS, SIC, NACE, D&B Hoovers, ISIC)
  - Multilingual names (Chinese, English, etc.)
  - Employee figures, websites, registration numbers
  - Stock exchanges, banks, activities, UNSPSC codes
- **Legal Events**: Liens, Judgments, Suits, Bankruptcy, Claims with full filing details
- **Financial Statements**: Overview + detailed line items (Balance Sheet, P&L, Cash Flow, Ratios)
- **Significant Events**: Operational and disaster events tracking
- **Awards & Contracts**: Government contracts and awards
- **Exclusions**: Active/inactive exclusions tracking
- **Deduplication**: Option A (Delete & Replace) - prevents duplicate data on reloads
- **Currency Tracking**: All monetary fields capture both value and currency

## Installation

\\\ash
pip install sqlalchemy pandas
\\\

## Quick Start

```python
import datablockAPI as api

# Initialize database
api.init(database='sqlite:///datablock.db')

# Load JSON data files
api.load(['companyinfo.json', 'companyfinancial.json', 'eventsfilings.json'])

# Query data
session = api.get_session()
from datablockAPI.core.models import Company, CompanyInfo, IndustryCode, LienFiling

# Get company info with industry codes
company = session.query(Company).filter_by(duns='540924028').first()
info = company.company_info
print(f"{info.primary_name} - {info.legal_form_description}")
print(f"Location: {info.primary_address_locality}, {info.primary_address_country}")
print(f"Industry Codes: {len(info.industry_codes)}")

# Query liens
liens = session.query(LienFiling).all()
```

## Database Schema

### Company Information Tables (NEW in v1.1)
- `company_info` - 80+ fields covering all company metadata
- `industry_codes` - NAICS, SIC, NACE, D&B Hoovers, ISIC classifications
- `trade_style_names` - DBA names
- `multilingual_names` - Company names in multiple languages
- `website_addresses` - URLs and domain names
- `telephone_numbers` - Phone numbers with international codes
- `email_addresses` - Email contacts
- `registration_numbers` - Tax IDs, business licenses, USCC codes
- `stock_exchanges` - Stock ticker information
- `banks` - Banking relationships
- `company_activities` - Business descriptions
- `employee_figures` - Employee counts (actual vs modeled, individual vs consolidated)
- `unspsc_codes` - UN product/service classification codes

### Legal Events Tables
- `legal_events_summary` - Summary flags
- `lien_filings` - Tax liens, UCC liens
- `judgment_filings` - Court judgments
- `suits` - Lawsuit filings
- `claim_filings` - Claims
- `bankruptcies` - Bankruptcy filings

### Financial Tables
- `financial_statements` - Statement metadata
- `financial_overviews` - Key metrics summary
- `balance_sheet_items` - Balance sheet line items
- `profit_loss_items` - Income statement line items
- `cash_flow_items` - Cash flow line items
- `financial_ratios` - Financial ratios

### Other Tables
- `significant_events` - Operational/disaster events
- `awards` - Government contracts
- `active_exclusions` - Exclusion records
- And more...

## Version

v1.1.0 - Enhanced CompanyInfo with 80+ fields and 12 related tables
