# v2.0 Implementation Plan - Complete Schema from PDF Documentation

## Overview
Extracted complete schema definitions from 523-page OpenAPI specification PDF. This document outlines fields to add for v2.0.

## 1. VIOLATIONS MODEL - Complete Enhancement

### Current State (v1.0)
- Basic boolean flags only (hasEPAViolations, hasOSHAViolations, etc.)

### v2.0 Additions
Found **24+ detailed fields** covering:

#### EPA Violations
```python
total_epa_violations_count: int = None  # Total count
most_recent_epa_violation_date: str = None  # YYYY-MM-DD
total_epa_violations_amount: float = None  # Monetary amount
epa_violations: list = None  # Array of detailed violations with:
    - has_air_facility: bool
    - has_clean_water_permit: bool
    - has_sdwis_permit: bool
    - has_rcra_permit: bool
    - has_tri_permit: bool
    - has_greenhouse_gas_permit: bool
    - report_url: str
```

#### OSHA Violations
```python
total_osha_violations_count: int = None
most_recent_osha_violation_date: str = None
total_osha_violations_amount: float = None
```

#### GCL Citations
```python
total_gcl_citations_count: int = None
most_recent_gcl_citation_date: str = None
total_gcl_citations_amount: float = None
```

#### DOL Wage/Hour Violations
```python
total_dol_wages_hours_violations_count: int = None
most_recent_dol_wages_hours_violation_date: str = None
total_dol_wages_hours_violations_amount: float = None
```

#### Medicare Nursing Home Violations
```python
total_medicare_nursing_home_violations_count: int = None
most_recent_medicare_nursing_home_violation_date: str = None
total_medicare_nursing_home_violations_amount: float = None
```

#### Canadian Environmental Violations
```python
total_ca_environmental_violations_count: int = None
most_recent_ca_environmental_violation_date: str = None
total_ca_environmental_violations_amount: float = None
```

### Loader Implementation
- JSON path: `organization.violations.*`
- Handle nested arrays for detailed EPA violations
- Extract counts, dates, amounts for each violation type

## 2. FINANCING EVENTS (UCC FILINGS) - Complete Enhancement

### Current State (v1.0)
- Model exists but NO loader implemented

### v2.0 Additions
Found **100+ fields** covering:

#### Top-Level Fields
```python
has_financing_events: bool = None
has_open_financing_events: bool = None
has_secured_filings: bool = None
has_open_secured_filings: bool = None
has_letter_of_liability: bool = None
has_open_letter_of_liability: bool = None
has_removed_letter_of_liability: bool = None
has_letter_of_agreement: bool = None
```

#### FinancingStatementFiling Structure
```python
total_count: int = None
most_recent_filing_date: str = None

# Period summaries (12 months)
period_summary_12_months_count: int = None
period_summary_12_months_amount: float = None

# Array of detailed filings
filings: list = None  # Each filing has:
```

#### Financing Filing Details (per filing)
```python
# Filing Information
filing_date: str = None
filing_reference: str = None
filing_medium: str = None
event_id: int = None
original_filing_date: str = None
original_filing_reference: str = None
published_date: str = None
received_date: str = None
end_date: str = None
end_indicator: bool = None
expiration_date: str = None

# Amounts
filing_amount: float = None
filing_amount_currency: str = None

# Types and Status
filing_type_description: str = None
filing_type_dnb_code: int = None
document_type_description: str = None
document_type_dnb_code: int = None
contract_type_description: str = None
contract_type_dnb_code: int = None

# Flags
has_whole_business_secured: bool = None
is_secured_on_all_assets: bool = None
is_stop_d: bool = None

# Complex nested structures
collaterals: list = None  # Array of collateral items
role_players: list = None  # Array of debtors/secured parties
contact_events: list = None  # Array of contacts
filing_results: list = None  # Array of outcomes
reasons: list = None  # Array of reasons
```

#### Collateral Details (per collateral)
```python
# Collateral classification
collateral_class_description: str = None
collateral_class_dnb_code: int = None
collateral_type_description: str = None
collateral_type_dnb_code: int = None

# Quantities
quantity: int = None
item_quantity: int = None

# Scope
scope_description: str = None
scope_dnb_code: int = None

# Detailed item information (for vehicles, equipment)
collateral_details: list = None  # Array with:
    - is_used: bool
    - manufactured_year: str
    - manufacture_name: str
    - model_name: str
    - model_year: str
    - serial_number: str
    - text_entry: list  # Free text descriptions

# Supplemental items (proceeds, products)
supplemental_items: list = None
```

#### Role Players (per party)
```python
role_player_type_description: str = None  # Debtor, Secured Party, etc.
role_player_type_dnb_code: int = None
duns: str = None
name: str = None
address: Address = None  # Full address structure
```

### Loader Implementation
- JSON path: `organization.financingEvents.financingStatementFilings.filings[]`
- Complex nested arrays: collaterals[], rolePlayers[], contactEvents[]
- Need careful handling of optional nested structures

## 3. INSOLVENCY MODEL - Complete Enhancement

### Current State (v1.0)
- Minimal structure (type, filing_date, court_name only)

### v2.0 Additions
Found **150+ fields** covering:

#### Top-Level Filing Fields
```python
# Activities and proceedings
activities: list = None  # Array of bankruptcy proceedings with:
    - activity_date: str
    - description: str

# Legal hearing
actual_legal_hearing_date: str = None

# Asset classification
asset_class: list = None  # Array with:
    - description: str
    - dnb_code: int

# Amounts
awarded_amount: float = None
awarded_amount_currency: str = None
```

#### Collaterals (Assets Used as Security)
```python
collaterals: list = None  # Same structure as Financing Events
# Each collateral has:
    - collateral_details: list  # Vehicle/equipment details
    - collateral_supplemental_items: list  # Proceeds, products
    - item_quantity: int
    - quantity: int
    - scope: object (description, dnb_code)
    - supplemental_items: list
    - text_entry: list
```

#### Contact Events (Trustees, Lawyers, etc.)
```python
contact_events: list = None  # Array with:
    - contact_date: str
    - duns: str
    - name: str
    - organization_name: str
    - address: Address
    - comments: list (description, dnb_code)
    - non_specific_source: object (Trustee, Official Registry, etc.)
    - positions: list  # Job positions
    - results: list  # Outcomes
    - role_players: list  # Related parties
    - text_entry: list
```

#### Court Information
```python
court_name: str = None
court_address: Address = None  # Full address with:
    - address_country: object
    - address_county: object
    - address_locality: object
    - address_region: object
    - continental_region: object
    - postal_code: str
    - street_address: object
```

### Loader Implementation
- JSON path: `organization.legalEvents.insolvency.filings[]`
- Reuse collateral and address structures from Financing Events
- Handle complex nested contact events with multiple sub-objects

## 4. LIQUIDATION MODEL - Complete Enhancement

### Current State (v1.0)
- Minimal structure (type, filing_date, court_name only)

### v2.0 Additions
Found **200 fields** - SAME structure as Insolvency

Liquidation uses identical field structure to Insolvency but specifically for company winding-up/liquidation events.

### Implementation Strategy
- Reuse all Insolvency field definitions
- JSON path: `organization.legalEvents.liquidation.filings[]`
- Can share same nested classes (Activities, Collaterals, ContactEvents, etc.)

## Implementation Priority

### Phase 1: Violations (EASIEST - Start Here)
- Clear, flat structure with counts/amounts/dates
- No complex nested arrays
- Straightforward JSON parsing
- **Estimated effort**: 1-2 hours

### Phase 2: Insolvency + Liquidation (MEDIUM)
- Shared complex structure
- Multiple nested arrays
- Can implement once, use twice
- **Estimated effort**: 3-4 hours

### Phase 3: Financing Events/UCC (COMPLEX)
- Most complex nested structures
- Collateral details with vehicle/equipment specs
- Multiple role players and contact events
- **Estimated effort**: 4-5 hours

## Shared Data Structures (Implement Once, Reuse Everywhere)

### Collateral Detail
Used in: Financing Events, Insolvency, Liquidation
```python
@dataclass
class CollateralDetail:
    is_used: bool = None
    manufactured_year: str = None
    manufacture_name: str = None
    model_name: str = None
    model_year: str = None
    serial_number: str = None
    text_entry: list = None
```

### Address
Used in: All models with contact/court information
```python
@dataclass
class Address:
    country_code: str = None
    country_name: str = None
    locality_name: str = None  # City
    region_name: str = None  # State
    region_abbreviated_name: str = None
    county_name: str = None
    postal_code: str = None
    street_line1: str = None
    street_line2: str = None
    continental_region: str = None
```

### Role Player
Used in: Financing Events, Insolvency, Liquidation, Suits, Liens, etc.
```python
@dataclass
class RolePlayer:
    role_type_description: str = None  # Debtor, Creditor, Trustee, etc.
    role_type_dnb_code: int = None
    duns: str = None
    name: str = None
    organization_name: str = None
    address: Address = None
```

## Next Steps

1. ✓ PDF extracted and analyzed
2. ✓ Complete schema documented
3. **TODO**: Implement Phase 1 (Violations) in models.py
4. **TODO**: Implement Phase 1 loader in loader.py
5. **TODO**: Test with existing JSON samples
6. **TODO**: Implement Phase 2 (Insolvency/Liquidation)
7. **TODO**: Implement Phase 3 (Financing Events)
8. **TODO**: Update README with v2.0 features
9. **TODO**: Commit and tag as v2.0.0

## Sample JSON Paths for Testing

### Violations
```json
{
  "organization": {
    "violations": {
      "hasEPAViolations": true,
      "totalEPAViolationsCount": 3,
      "mostRecentEPAViolationDate": "2018-09-12",
      "totalEPAViolationsAmount": {
        "value": 125000.5
      },
      "epaViolations": [...]
    }
  }
}
```

### Financing Events
```json
{
  "organization": {
    "financingEvents": {
      "financingStatementFilings": {
        "totalCount": 2,
        "mostRecentFilingDate": "2020-10-09",
        "filings": [...]
      }
    }
  }
}
```

### Insolvency
```json
{
  "organization": {
    "legalEvents": {
      "insolvency": {
        "filings": [
          {
            "activities": [...],
            "collaterals": [...],
            "contactEvents": [...],
            "courtName": "...",
            "courtAddress": {...}
          }
        ]
      }
    }
  }
}
```

## Version Notes
- **Current**: v1.0.0 - Based on JSON samples only
- **Target**: v2.0.0 - Complete schema from OpenAPI PDF
- **Breaking Changes**: None - all v1.0 functionality preserved
- **New Features**: Complete field coverage for Violations, UCC, Insolvency, Liquidation
