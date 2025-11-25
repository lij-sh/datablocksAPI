# datablockAPI

A Python API for loading D&B DataBlocks (company information, financials, and events/filings) into a relational database.

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
import datablockAPI as api

# Initialize database
api.init(database='sqlite:///datablock.db')

# Load JSON data files
api.load([
    'Material/companyinfo.json',
    'Material/companyfinancial.json',
    'Material/eventsfilings.json'
])
```

## Database Support

The API supports multiple database backends:

```python
# SQLite (file-based)
api.init(database='sqlite:///datablock.db')

# PostgreSQL
api.init(database='postgresql://user:password@localhost:5432/datablock')

# MySQL
api.init(database='mysql+pymysql://user:password@localhost:3306/datablock')
```

## Data Models

### Companies (Shared)
- `companies` - Central company entity (DUNS-based)

### Legal Events
- `legal_events_summary` - Summary flags for all legal events
- `liens` + `lien_filings` + `lien_filing_role_players`
- `judgments` + `judgment_filings` + `judgment_filing_role_players`
- `suits`, `bankruptcies`, `claims`, `insolvencies`, `liquidations`, `other_legal_events`

### Awards
- `awards_summary` - Summary of all awards
- `contracts` + `contract_actions` + `contract_characteristics`
- `loans`, `grants`, `debts` (placeholder structures)

### Exclusions
- `exclusions_summary`
- `active_exclusions`, `inactive_exclusions`

### Other Events
- `significant_events_summary`
- `financing_events_summary`
- `violations_summary`
- `document_filings`
- `commercial_collection_claims`

### Financials
- `financial_statements` - Both fiscal and other financial statements
- Supports balance sheets, P&L, cash flow statements

### Company Info
- `company_info` - Core company metadata
- Related tables for addresses, industry codes, etc.

## Querying Data

```python
from datablockAPI import get_session
from datablockAPI.core.models import Company, LienFiling, Contract

session = get_session()

# Get all companies
companies = session.query(Company).all()

# Get liens for a specific company
company = session.query(Company).filter_by(duns='060704780').first()
liens = session.query(LienFiling).filter_by(company_id=company.id).all()

# Get contracts
contracts = session.query(Contract).filter_by(company_id=company.id).all()

session.close()
```

## Architecture

```
datablockAPI/
├── __init__.py              # API entry point (init, load)
├── core/
│   ├── database.py          # Database connection & initialization
│   ├── models.py            # SQLAlchemy ORM models
│   └── loader.py            # JSON data loading logic
└── utils/
    └── __init__.py
```

## Features

- ✅ **Database-agnostic**: SQLite, PostgreSQL, MySQL support
- ✅ **Normalized schema**: Option B design with separate tables per event type
- ✅ **Hierarchical data**: Preserves JSON structure (Company → Category → EventType → Filings)
- ✅ **DUNS-based deduplication**: Upserts companies, prevents duplicates
- ✅ **Relational integrity**: Foreign keys, cascading deletes
- ✅ **Time-series support**: Multiple financial statements, events over time
- ✅ **Role players**: Tracks participants in legal filings (debtors, lien holders, etc.)

## Test Results

```
✓ Database initialized: sqlite:///datablock.db
✓ Created 28 tables
✓ Loaded 3 file(s)
✓ Companies in database: 3
✓ Lien filings in database: 11
✓ Contracts in database: 100
```

## Future Enhancements

- [ ] Complete implementation of all legal event types (suits, bankruptcy, claims, etc.)
- [ ] Full financial statement models (balance sheet items, P&L items, ratios)
- [ ] Company info related tables (addresses, industry codes, contacts)
- [ ] Bulk loading optimizations
- [ ] Data validation with Pydantic schemas
- [ ] Query helper methods
- [ ] Export functionality

## License

MIT
