# DataBlock API

Python SQLAlchemy ORM wrapper for D&B DataBlock API data with comprehensive data loading and querying capabilities.

## Features

- **Complete Schema Coverage**: 38+ database tables covering all D&B DataBlock entities
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

\\\python
import datablockAPI as api

# Initialize database
api.init(database='sqlite:///datablock.db')

# Load JSON data files
api.load(['companyinfo.json', 'companyfinancial.json', 'eventsfilings.json'])

# Query data
session = api.get_session()
from datablockAPI.core.models import Company, LienFiling

liens = session.query(LienFiling).all()
\\\

## Version

v1.0.0 - Initial release with Option A deduplication and complete financial models
