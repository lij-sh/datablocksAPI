# Database Schema Documentation

Comprehensive documentation of all database tables, fields, types, and JSON source mappings for the DataBlock API.

## Table of Contents

- [Core Tables](#core-tables)
  - [Company](#company)
  - [CompanyInfo](#companyinfo)
- [Company Info Related Tables](#company-info-related-tables)
  - [IndustryCode](#industrycode)
  - [TradeStyleName](#tradestylename)
  - [MultilingualName](#multilingualname)
  - [WebsiteAddress](#websiteaddress)
  - [TelephoneNumber](#telephonenumber)
  - [EmailAddress](#emailaddress)
  - [RegistrationNumber](#registrationnumber)
  - [StockExchange](#stockexchange)
  - [Bank](#bank)
  - [CompanyActivity](#companyactivity)
  - [EmployeeFigure](#employeefigure)
  - [UNSPSCCode](#unspsccode)
- [Legal Events Tables](#legal-events-tables)
- [Financial Tables](#financial-tables)
- [Other Tables](#other-tables)

---

## Core Tables

### Company

**Table Name**: `companies`  
**JSON Source**: All JSON files - `organization` object  
**Purpose**: Core company entity shared across all data blocks

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key (auto-increment) | - |
| duns | String(9) | No | D-U-N-S Number (unique index) | `organization.duns` |
| primary_name | String(500) | Yes | Company primary name | `organization.primaryName` |
| country_iso_alpha2_code | String(2) | Yes | Country code (ISO Alpha-2) | `organization.countryISOAlpha2Code` |
| created_at | DateTime | No | Record creation timestamp | - |
| updated_at | DateTime | No | Record update timestamp | - |

**Relationships**:
- `company_info` → CompanyInfo (one-to-one)
- `legal_events_summary` → LegalEventsSummary (one-to-one)
- `awards_summary` → AwardsSummary (one-to-one)
- `exclusions_summary` → ExclusionsSummary (one-to-one)
- `significant_events_summary` → SignificantEventsSummary (one-to-one)
- `financing_events_summary` → FinancingEventsSummary (one-to-one)
- `violations_summary` → ViolationsSummary (one-to-one)

---

### CompanyInfo

**Table Name**: `company_info`  
**JSON Source**: `companyinfo.json` - `organization` object  
**Purpose**: Comprehensive company information with 80+ metadata fields

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key (auto-increment) | - |
| company_id | Integer | No | Foreign key to companies table | - |
| **Core Identifiers** |
| primary_name | String(500) | Yes | Company primary trading name | `organization.primaryName` |
| registered_name | String(500) | Yes | Registered legal name | `organization.registeredName` |
| country_iso_alpha2_code | String(2) | Yes | Country code (ISO Alpha-2) | `organization.countryISOAlpha2Code` |
| **Business Characteristics** |
| is_fortune_1000_listed | Boolean | Yes | Fortune 1000 listed flag | `organization.isFortune1000Listed` |
| is_forbes_largest_private_listed | Boolean | Yes | Forbes largest private companies flag | `organization.isForbesLargestPrivateCompaniesListed` |
| is_non_classified_establishment | Boolean | Yes | Non-classified establishment flag | `organization.isNonClassifiedEstablishment` |
| is_standalone | Boolean | Yes | Standalone organization flag | `organization.isStandalone` |
| is_agent | Boolean | Yes | Agent designation flag | `organization.isAgent` |
| is_importer | Boolean | Yes | Importer flag | `organization.isImporter` |
| is_exporter | Boolean | Yes | Exporter flag | `organization.isExporter` |
| is_small_business | Boolean | Yes | Small business designation | `organization.isSmallBusiness` |
| **Primary Industry** |
| primary_industry_code_sic_v4 | String(50) | Yes | Primary SIC v4 code | `organization.primaryIndustryCode.usSicV4` |
| primary_industry_description_sic_v4 | String(500) | Yes | Primary SIC v4 description | `organization.primaryIndustryCode.usSicV4Description` |
| **Legal Information** |
| business_entity_type_desc | String(200) | Yes | Business entity type | `organization.businessEntityType.description` |
| business_entity_type_dnb_code | Integer | Yes | Business entity type D&B code | `organization.businessEntityType.dnbCode` |
| legal_form_description | String(200) | Yes | Legal form description | `organization.legalForm.description` |
| legal_form_dnb_code | Integer | Yes | Legal form D&B code | `organization.legalForm.dnbCode` |
| legal_form_start_date | Date | Yes | Legal form effective start date | `organization.legalForm.startDate` |
| **Dates** |
| start_date | String(20) | Yes | Business start date (can be year only) | `organization.startDate` |
| incorporated_date | Date | Yes | Date of incorporation | `organization.incorporatedDate` |
| control_ownership_date | Date | Yes | Control ownership date | `organization.controlOwnershipDate` |
| first_report_date | Date | Yes | First report date | `organization.dunsControlStatus.firstReportDate` |
| investigation_date | Date | Yes | Investigation date | `organization.investigationDate` |
| tsr_report_date | Date | Yes | TSR report date | `organization.tsrReportDate` |
| fiscal_year_end | String(10) | Yes | Fiscal year end (MM-DD format) | `organization.fiscalYearEnd` |
| imperial_calendar_start_year | String(10) | Yes | Imperial calendar start year | `organization.imperialCalendarStartYear` |
| **Operating Status** |
| operating_status_description | String(200) | Yes | Operating status description | `organization.dunsControlStatus.operatingStatus.description` |
| operating_status_dnb_code | Integer | Yes | Operating status D&B code | `organization.dunsControlStatus.operatingStatus.dnbCode` |
| operating_status_start_date | Date | Yes | Operating status start date | `organization.dunsControlStatus.operatingStatus.startDate` |
| operating_sub_status_description | String(200) | Yes | Operating sub-status description | `organization.dunsControlStatus.operatingSubStatus.description` |
| operating_sub_status_dnb_code | Integer | Yes | Operating sub-status D&B code | `organization.dunsControlStatus.operatingSubStatus.dnbCode` |
| detailed_operating_status_desc | String(200) | Yes | Detailed operating status | `organization.dunsControlStatus.detailedOperatingStatus.description` |
| detailed_operating_status_dnb_code | Integer | Yes | Detailed operating status code | `organization.dunsControlStatus.detailedOperatingStatus.dnbCode` |
| **Status Flags** |
| is_marketable | Boolean | Yes | Marketable status flag | `organization.dunsControlStatus.isMarketable` |
| is_mail_undeliverable | Boolean | Yes | Mail undeliverable flag | `organization.dunsControlStatus.isMailUndeliverable` |
| is_telephone_disconnected | Boolean | Yes | Telephone disconnected flag | `organization.dunsControlStatus.isTelephoneDisconnected` |
| is_delisted | Boolean | Yes | Delisted flag | `organization.dunsControlStatus.isDelisted` |
| is_self_requested_duns | Boolean | Yes | Self-requested DUNS flag | `organization.dunsControlStatus.isSelfRequestedDUNS` |
| self_request_date | Date | Yes | Self-request date | `organization.dunsControlStatus.selfRequestDate` |
| **Record Classification** |
| record_class_description | String(200) | Yes | Record class description | `organization.dunsControlStatus.recordClass.description` |
| record_class_dnb_code | Integer | Yes | Record class D&B code | `organization.dunsControlStatus.recordClass.dnbCode` |
| **Control Ownership** |
| control_ownership_type_desc | String(200) | Yes | Control ownership type | `organization.controlOwnershipType.description` |
| control_ownership_type_dnb_code | Integer | Yes | Control ownership type code | `organization.controlOwnershipType.dnbCode` |
| **Primary Address** (17 fields) |
| primary_address_line1 | String(500) | Yes | Street address line 1 | `organization.primaryAddress.streetAddress.line1` |
| primary_address_line2 | String(500) | Yes | Street address line 2 | `organization.primaryAddress.streetAddress.line2` |
| primary_address_locality | String(200) | Yes | City/locality | `organization.primaryAddress.addressLocality.name` |
| primary_address_region | String(200) | Yes | State/province name | `organization.primaryAddress.addressRegion.name` |
| primary_address_region_abbr | String(50) | Yes | State/province abbreviation | `organization.primaryAddress.addressRegion.abbreviatedName` |
| primary_address_region_iso_code | String(10) | Yes | Region ISO subdivision code | `organization.primaryAddress.addressRegion.isoSubDivisionCode` |
| primary_address_postal_code | String(50) | Yes | Postal/ZIP code | `organization.primaryAddress.postalCode` |
| primary_address_country | String(200) | Yes | Country name | `organization.primaryAddress.addressCountry.name` |
| primary_address_country_iso | String(2) | Yes | Country ISO Alpha-2 code | `organization.primaryAddress.addressCountry.isoAlpha2Code` |
| primary_address_continental_region | String(100) | Yes | Continental region | `organization.primaryAddress.continentalRegion.name` |
| primary_address_latitude | Numeric(10,6) | Yes | Latitude coordinate | `organization.primaryAddress.latitude` |
| primary_address_longitude | Numeric(10,6) | Yes | Longitude coordinate | `organization.primaryAddress.longitude` |
| primary_address_geo_precision_desc | String(200) | Yes | Geographical precision | `organization.primaryAddress.geographicalPrecision.description` |
| primary_address_geo_precision_dnb_code | Integer | Yes | Geographical precision code | `organization.primaryAddress.geographicalPrecision.dnbCode` |
| primary_address_is_manufacturing | Boolean | Yes | Manufacturing location flag | `organization.primaryAddress.isManufacturingLocation` |
| primary_address_is_registered | Boolean | Yes | Registered address flag | `organization.primaryAddress.isRegisteredAddress` |
| **Mailing Address** (7 fields) |
| mailing_address_line1 | String(500) | Yes | Mailing street line 1 | `organization.mailingAddress.streetAddress.line1` |
| mailing_address_line2 | String(500) | Yes | Mailing street line 2 | `organization.mailingAddress.streetAddress.line2` |
| mailing_address_locality | String(200) | Yes | Mailing city | `organization.mailingAddress.addressLocality.name` |
| mailing_address_region | String(200) | Yes | Mailing state/province | `organization.mailingAddress.addressRegion.name` |
| mailing_address_postal_code | String(50) | Yes | Mailing postal code | `organization.mailingAddress.postalCode` |
| mailing_address_country | String(200) | Yes | Mailing country | `organization.mailingAddress.addressCountry.name` |
| mailing_address_country_iso | String(2) | Yes | Mailing country ISO code | `organization.mailingAddress.addressCountry.isoAlpha2Code` |
| **Registered Address** (7 fields) |
| registered_address_line1 | String(500) | Yes | Registered street line 1 | `organization.registeredAddress.streetAddress.line1` |
| registered_address_line2 | String(500) | Yes | Registered street line 2 | `organization.registeredAddress.streetAddress.line2` |
| registered_address_locality | String(200) | Yes | Registered city | `organization.registeredAddress.addressLocality.name` |
| registered_address_region | String(200) | Yes | Registered state/province | `organization.registeredAddress.addressRegion.name` |
| registered_address_postal_code | String(50) | Yes | Registered postal code | `organization.registeredAddress.postalCode` |
| registered_address_country | String(200) | Yes | Registered country | `organization.registeredAddress.addressCountry.name` |
| registered_address_country_iso | String(2) | Yes | Registered country ISO code | `organization.registeredAddress.addressCountry.isoAlpha2Code` |
| **Language and Currency** |
| preferred_language_desc | String(100) | Yes | Preferred language | `organization.preferredLanguage.description` |
| preferred_language_dnb_code | Integer | Yes | Preferred language code | `organization.preferredLanguage.dnbCode` |
| default_currency | String(3) | Yes | Default currency code (ISO) | `organization.defaultCurrency` |
| **Contact Information** |
| certified_email | String(500) | Yes | Certified email address | `organization.certifiedEmail` |
| legal_entity_identifier | String(100) | Yes | Legal Entity Identifier (LEI) | `organization.legalEntityIdentifier` |
| securities_report_id | String(100) | Yes | Securities report ID | `organization.securitiesReportID` |
| **Classifications** |
| employer_designation_desc | String(200) | Yes | Employer designation | `organization.employerDesignation.description` |
| employer_designation_dnb_code | Integer | Yes | Employer designation code | `organization.employerDesignation.dnbCode` |
| charter_type_desc | String(200) | Yes | Charter type | `organization.charterType.description` |
| charter_type_dnb_code | Integer | Yes | Charter type code | `organization.charterType.dnbCode` |
| organization_size_category_desc | String(200) | Yes | Organization size category | `organization.organizationSizeCategory.description` |
| organization_size_category_dnb_code | Integer | Yes | Organization size code | `organization.organizationSizeCategory.dnbCode` |
| business_trust_index_score | Numeric(10,2) | Yes | Business trust index score | `organization.businessTrustIndex.score` |
| business_trust_index_description | String(200) | Yes | Business trust index description | `organization.businessTrustIndex.description` |

**Relationships**:
- `company` → Company (many-to-one)
- `industry_codes` → IndustryCode[] (one-to-many, cascade delete)
- `trade_style_names` → TradeStyleName[] (one-to-many, cascade delete)
- `multilingual_names` → MultilingualName[] (one-to-many, cascade delete)
- `website_addresses` → WebsiteAddress[] (one-to-many, cascade delete)
- `telephone_numbers` → TelephoneNumber[] (one-to-many, cascade delete)
- `email_addresses` → EmailAddress[] (one-to-many, cascade delete)
- `registration_numbers` → RegistrationNumber[] (one-to-many, cascade delete)
- `stock_exchanges` → StockExchange[] (one-to-many, cascade delete)
- `banks` → Bank[] (one-to-many, cascade delete)
- `activities` → CompanyActivity[] (one-to-many, cascade delete)
- `employee_figures` → EmployeeFigure[] (one-to-many, cascade delete)
- `unspsc_codes` → UNSPSCCode[] (one-to-many, cascade delete)

---

## Company Info Related Tables

### IndustryCode

**Table Name**: `industry_codes`  
**JSON Source**: `companyinfo.json` - `organization.industryCodes[]` array  
**Purpose**: Industry classification codes (NAICS, SIC, NACE, D&B Hoovers, ISIC, etc.)

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| code | String(50) | Yes | Industry classification code | `industryCodes[].code` |
| description | String(500) | Yes | Industry description | `industryCodes[].description` |
| type_description | String(200) | Yes | Code type (e.g., "NAICS 2022", "SIC v4") | `industryCodes[].typeDescription` |
| type_dnb_code | Integer | Yes | Code type D&B code | `industryCodes[].typeDnBCode` |
| priority | Integer | Yes | Display priority (1 = highest) | `industryCodes[].priority` |

**Example JSON**:
```json
{
  "industryCodes": [
    {
      "code": "325611",
      "description": "Soap and Other Detergent Manufacturing",
      "typeDescription": "North American Industry Classification System 2022",
      "typeDnBCode": 30832,
      "priority": 1
    }
  ]
}
```

---

### TradeStyleName

**Table Name**: `trade_style_names`  
**JSON Source**: `companyinfo.json` - `organization.tradeStyleNames[]` array  
**Purpose**: Alternate business names (DBA - Doing Business As)

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| name | String(500) | Yes | Trade style name / DBA | `tradeStyleNames[]` or `tradeStyleNames[].name` |
| priority | Integer | Yes | Display priority (sequential) | Assigned during load |

**Note**: JSON can contain either strings or objects with a `name` field.

---

### MultilingualName

**Table Name**: `multilingual_names`  
**JSON Source**: `companyinfo.json` - Three arrays:
- `organization.multilingualPrimaryName[]`
- `organization.multilingualRegisteredNames[]`
- `organization.multilingualTradestyleNames[]`

**Purpose**: Company names in multiple languages with writing scripts

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| name | String(500) | Yes | Name in specified language | `multilingual*.name` |
| name_type | String(50) | Yes | Type: 'primary', 'registered', 'tradestyle' | Determined by source array |
| language_description | String(100) | Yes | Language (e.g., "Chinese", "English") | `multilingual*.language.description` |
| language_dnb_code | Integer | Yes | Language D&B code | `multilingual*.language.dnbCode` |
| writing_script_desc | String(100) | Yes | Writing script (e.g., "Han (Hanzi, Kanji, Hanja)") | `multilingual*.writingScript.description` |
| writing_script_dnb_code | Integer | Yes | Writing script D&B code | `multilingual*.writingScript.dnbCode` |

**Example JSON**:
```json
{
  "multilingualPrimaryName": [
    {
      "name": "湖北活力集团有限公司",
      "language": {
        "description": "Chinese",
        "dnbCode": 30086
      },
      "writingScript": {
        "description": "Han (Hanzi, Kanji, Hanja)",
        "dnbCode": 28484
      }
    }
  ]
}
```

---

### WebsiteAddress

**Table Name**: `website_addresses`  
**JSON Source**: `companyinfo.json` - `organization.websiteAddress[]` array  
**Purpose**: Company website URLs and domain names

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| url | String(500) | Yes | Full website URL | `websiteAddress[].url` |
| domain_name | String(200) | Yes | Domain name | `websiteAddress[].domainName` |

**Example JSON**:
```json
{
  "websiteAddress": [
    {
      "url": "http://www.power28.com.cn",
      "domainName": "www.power28.com.cn"
    }
  ]
}
```

---

### TelephoneNumber

**Table Name**: `telephone_numbers`  
**JSON Source**: `companyinfo.json` - `organization.telephone[]` array  
**Purpose**: Company telephone numbers with international dialing codes

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| telephone_number | String(50) | Yes | Telephone number | `telephone[].telephoneNumber` |
| international_dialing_code | String(10) | Yes | International dialing code (e.g., "+86") | `telephone[].internationalDialingCode` |
| is_unreachable | Boolean | Yes | Unreachable status flag | `telephone[].isUnreachable` |

---

### EmailAddress

**Table Name**: `email_addresses`  
**JSON Source**: `companyinfo.json` - `organization.email[]` array  
**Purpose**: Company email addresses

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| email | String(500) | Yes | Email address | `email[]` or `email[].email` |

**Note**: JSON can contain either strings or objects with an `email` field.

---

### RegistrationNumber

**Table Name**: `registration_numbers`  
**JSON Source**: `companyinfo.json` - `organization.registrationNumbers[]` array  
**Purpose**: Business registration numbers (tax IDs, business licenses, USCC codes, etc.)

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| registration_number | String(200) | Yes | Registration number | `registrationNumbers[].registrationNumber` |
| type_description | String(200) | Yes | Type (e.g., "United Social Credit Code") | `registrationNumbers[].typeDescription` |
| type_dnb_code | Integer | Yes | Type D&B code | `registrationNumbers[].typeDnBCode` |
| registration_number_class_desc | String(200) | Yes | Class description | `registrationNumbers[].registrationNumberClass.description` |
| registration_number_class_dnb_code | Integer | Yes | Class D&B code | `registrationNumbers[].registrationNumberClass.dnbCode` |
| is_preferred | Boolean | Yes | Preferred registration number flag | `registrationNumbers[].isPreferredRegistrationNumber` |
| registration_location | String(500) | Yes | Registration location | `registrationNumbers[].registrationLocation.name` |

**Example JSON**:
```json
{
  "registrationNumbers": [
    {
      "registrationNumber": "91421000MA48YBWA2T",
      "typeDescription": "United Social Credit Code (CN)",
      "typeDnBCode": 26256,
      "isPreferredRegistrationNumber": true
    }
  ]
}
```

---

### StockExchange

**Table Name**: `stock_exchanges`  
**JSON Source**: `companyinfo.json` - `organization.stockExchanges[]` array  
**Purpose**: Stock exchange listings and ticker symbols

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| stock_exchange_name | String(200) | Yes | Stock exchange name | `stockExchanges[].stockExchangeName` |
| stock_exchange_code | String(50) | Yes | Stock exchange code | `stockExchanges[].stockExchangeCode` |
| ticker_symbol | String(50) | Yes | Ticker symbol | `stockExchanges[].tickerSymbol` |
| country_iso_alpha2_code | String(2) | Yes | Country code | `stockExchanges[].countryISOAlpha2Code` |

---

### Bank

**Table Name**: `banks`  
**JSON Source**: `companyinfo.json` - `organization.banks[]` array  
**Purpose**: Banking relationships and financial institutions

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| bank_name | String(500) | Yes | Bank name | `banks[].bankName` |
| bank_duns | String(9) | Yes | Bank's D-U-N-S Number | `banks[].duns` |

---

### CompanyActivity

**Table Name**: `company_activities`  
**JSON Source**: `companyinfo.json` - `organization.activities[]` array  
**Purpose**: Business activity descriptions in multiple languages

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| description | Text | Yes | Business activity description | `activities[].description` |
| language_description | String(100) | Yes | Language of description | `activities[].language.description` |
| language_dnb_code | Integer | Yes | Language D&B code | `activities[].language.dnbCode` |

**Example JSON**:
```json
{
  "activities": [
    {
      "description": "主要从事生产销售食品用洗涤剂、消毒剂、化妆品",
      "language": {
        "description": "Chinese",
        "dnbCode": 30086
      }
    }
  ]
}
```

---

### EmployeeFigure

**Table Name**: `employee_figures`  
**JSON Source**: `companyinfo.json` - `organization.numberOfEmployees[]` array  
**Purpose**: Employee count information with scope and reliability indicators

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| value | Integer | Yes | Number of employees | `numberOfEmployees[].value` |
| minimum_value | Integer | Yes | Minimum employee count | `numberOfEmployees[].minimumValue` |
| maximum_value | Integer | Yes | Maximum employee count | `numberOfEmployees[].maximumValue` |
| employee_figures_date | Date | Yes | As-of date for the figure | `numberOfEmployees[].employeeFiguresDate` |
| information_scope_description | String(200) | Yes | Scope: "Individual", "Consolidated", etc. | `numberOfEmployees[].informationScopeDescription` |
| information_scope_dnb_code | Integer | Yes | Scope D&B code | `numberOfEmployees[].informationScopeDnBCode` |
| reliability_description | String(100) | Yes | Reliability: "Actual", "Modelled", etc. | `numberOfEmployees[].reliabilityDescription` |
| reliability_dnb_code | Integer | Yes | Reliability D&B code | `numberOfEmployees[].reliabilityDnBCode` |

**Example JSON**:
```json
{
  "numberOfEmployees": [
    {
      "value": 637,
      "minimumValue": 637,
      "informationScopeDescription": "Individual",
      "reliabilityDescription": "Actual"
    }
  ]
}
```

---

### UNSPSCCode

**Table Name**: `unspsc_codes`  
**JSON Source**: `companyinfo.json` - `organization.unspscCodes[]` array  
**Purpose**: UNSPSC (United Nations Standard Products and Services Code) classifications

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_info_id | Integer | No | Foreign key to company_info | - |
| code | String(50) | Yes | UNSPSC code | `unspscCodes[].code` |
| description | String(500) | Yes | Product/service description | `unspscCodes[].description` |
| priority | Integer | Yes | Display priority | `unspscCodes[].priority` |

**Example JSON**:
```json
{
  "unspscCodes": [
    {
      "code": "47131800",
      "description": "Bath and body products",
      "priority": 1
    }
  ]
}
```

---

## Legal Events Tables

### LegalEventsSummary

**Table Name**: `legal_events_summary`  
**JSON Source**: `eventsfilings.json` - `organization.legalEvents` object  
**Purpose**: Summary of all legal events for a company

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| has_legal_events | Boolean | Yes | Has any legal events | `legalEvents.hasLegalEvents` |
| has_open_legal_events | Boolean | Yes | Has open legal events | `legalEvents.hasOpenLegalEvents` |
| has_suits | Boolean | Yes | Has suits | `legalEvents.hasSuits` |
| has_open_suits | Boolean | Yes | Has open suits | `legalEvents.hasOpenSuits` |
| has_liens | Boolean | Yes | Has liens | `legalEvents.hasLiens` |
| has_open_liens | Boolean | Yes | Has open liens | `legalEvents.hasOpenLiens` |
| has_judgments | Boolean | Yes | Has judgments | `legalEvents.hasJudgments` |
| has_open_judgments | Boolean | Yes | Has open judgments | `legalEvents.hasOpenJudgments` |
| has_bankruptcy | Boolean | Yes | Has bankruptcy | `legalEvents.hasBankruptcy` |
| has_open_bankruptcy | Boolean | Yes | Has open bankruptcy | `legalEvents.hasOpenBankruptcy` |
| has_claims | Boolean | Yes | Has claims | `legalEvents.hasClaims` |
| most_recent_lien_date | Date | Yes | Most recent lien date | `legalEvents.mostRecentLienDate` |
| most_recent_judgment_date | Date | Yes | Most recent judgment date | `legalEvents.mostRecentJudgmentDate` |
| most_recent_suit_date | Date | Yes | Most recent suit date | `legalEvents.mostRecentSuitDate` |

### LienFiling

**Table Name**: `lien_filings`  
**JSON Source**: `eventsfilings.json` - `organization.legalEvents.liens.lienFilings[]` array  
**Purpose**: Individual lien filings (tax liens, UCC liens, etc.)

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| lien_id | Integer | Yes | Foreign key to liens (parent) | - |
| filing_id | String(100) | Yes | Filing identifier | `lienFilings[].filingID` |
| filing_number | String(100) | Yes | Filing number | `lienFilings[].filingNumber` |
| filing_date | Date | Yes | Date of filing | `lienFilings[].filingDate` |
| status_description | String(200) | Yes | Status description | `lienFilings[].status.description` |
| status_dnb_code | Integer | Yes | Status D&B code | `lienFilings[].status.dnbCode` |
| filing_type_description | String(200) | Yes | Filing type | `lienFilings[].filingType.description` |
| filing_type_dnb_code | Integer | Yes | Filing type code | `lienFilings[].filingType.dnbCode` |
| release_date | Date | Yes | Release date | `lienFilings[].releaseDate` |
| legal_form_description | String(200) | Yes | Legal form | `lienFilings[].legalForm.description` |
| legal_form_dnb_code | Integer | Yes | Legal form code | `lienFilings[].legalForm.dnbCode` |
| filing_amount_value | Numeric(20,2) | Yes | Filing amount | `lienFilings[].filingAmount.value` |
| filing_amount_currency | String(3) | Yes | Currency code | `lienFilings[].filingAmount.currency` |
| original_filing_number | String(100) | Yes | Original filing number | `lienFilings[].originalFilingNumber` |
| original_filing_date | Date | Yes | Original filing date | `lienFilings[].originalFilingDate` |

**Relationships**:
- `role_players` → LienFilingRolePlayer[] (one-to-many)
- `reference_dates` → LienFilingReferenceDate[] (one-to-many)
- `text_entries` → LienFilingTextEntry[] (one-to-many)

### JudgmentFiling

**Table Name**: `judgment_filings`  
**JSON Source**: `eventsfilings.json` - `organization.legalEvents.judgments.judgmentFilings[]` array  
**Purpose**: Court judgment filings

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| judgment_id | Integer | Yes | Foreign key to judgments | - |
| filing_id | String(100) | Yes | Filing identifier | `judgmentFilings[].filingID` |
| filing_number | String(100) | Yes | Filing/docket number | `judgmentFilings[].filingNumber` |
| filing_date | Date | Yes | Filing date | `judgmentFilings[].filingDate` |
| status_description | String(200) | Yes | Status | `judgmentFilings[].status.description` |
| status_dnb_code | Integer | Yes | Status code | `judgmentFilings[].status.dnbCode` |
| filing_type_description | String(200) | Yes | Filing type | `judgmentFilings[].filingType.description` |
| filing_type_dnb_code | Integer | Yes | Filing type code | `judgmentFilings[].filingType.dnbCode` |
| legal_form_description | String(200) | Yes | Legal form | `judgmentFilings[].legalForm.description` |
| legal_form_dnb_code | Integer | Yes | Legal form code | `judgmentFilings[].legalForm.dnbCode` |
| filing_amount_value | Numeric(20,2) | Yes | Judgment amount | `judgmentFilings[].filingAmount.value` |
| filing_amount_currency | String(3) | Yes | Currency | `judgmentFilings[].filingAmount.currency` |
| docket_number | String(100) | Yes | Court docket number | `judgmentFilings[].docketNumber` |

**Relationships**:
- `role_players` → JudgmentFilingRolePlayer[] (one-to-many)

### SuitFiling

**Table Name**: `suit_filings`  
**JSON Source**: `eventsfilings.json` - `organization.legalEvents.suits.suitFilings[]` array  
**Purpose**: Lawsuit filings

Similar structure to JudgmentFiling with additional fields:
- `action_amount_value` / `action_amount_currency`
- `plaintiff_amount_sought_value` / `plaintiff_amount_sought_currency`

---

## Financial Tables

### FinancialStatement

**Table Name**: `financial_statements`  
**JSON Source**: `companyfinancial.json` - `organization.financials.financialStatements[]` array  
**Purpose**: Financial statement metadata and header information

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| financial_statement_to_date | Date | Yes | Statement period end date | `financialStatements[].financialStatementToDate` |
| currency | String(3) | Yes | Currency code (ISO 4217) | `financialStatements[].currency` |
| units | String(50) | Yes | Units (e.g., "Single Unit") | `financialStatements[].units.description` |
| units_dnb_code | Integer | Yes | Units D&B code | `financialStatements[].units.dnbCode` |
| reliability_description | String(200) | Yes | Reliability | `financialStatements[].reliabilityDescription` |
| reliability_dnb_code | Integer | Yes | Reliability code | `financialStatements[].reliabilityDnBCode` |
| information_scope_description | String(200) | Yes | Scope: "Consolidated", "Individual" | `financialStatements[].informationScopeDescription` |
| information_scope_dnb_code | Integer | Yes | Scope code | `financialStatements[].informationScopeDnBCode` |
| accounting_standard_description | String(200) | Yes | Accounting standard | `financialStatements[].accountingStandard.description` |
| accounting_standard_dnb_code | Integer | Yes | Standard code | `financialStatements[].accountingStandard.dnbCode` |
| audit_opinion_description | String(200) | Yes | Audit opinion | `financialStatements[].auditOpinion.description` |
| audit_opinion_dnb_code | Integer | Yes | Opinion code | `financialStatements[].auditOpinion.dnbCode` |
| fiscal_period | Integer | Yes | Fiscal period (months) | `financialStatements[].fiscalPeriod` |

**Relationships**:
- `overview` → FinancialOverview (one-to-one)
- `balance_sheet_items` → BalanceSheetItem[] (one-to-many)
- `profit_loss_items` → ProfitLossItem[] (one-to-many)
- `cash_flow_items` → CashFlowItem[] (one-to-many)
- `ratios` → FinancialRatio[] (one-to-many)

### FinancialOverview

**Table Name**: `financial_overviews`  
**JSON Source**: `companyfinancial.json` - `financialStatements[].statementOverview` object  
**Purpose**: Key financial metrics summary (assets, sales, net income, etc.)

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| statement_id | Integer | No | Foreign key to financial_statements | - |
| total_assets | Numeric(20,2) | Yes | Total assets | `statementOverview.totalAssets` |
| sales_revenue | Numeric(20,2) | Yes | Sales/revenue | `statementOverview.salesRevenue` |
| gross_profit | Numeric(20,2) | Yes | Gross profit | `statementOverview.grossProfit` |
| operating_profit_loss | Numeric(20,2) | Yes | Operating profit/loss | `statementOverview.operatingProfitLoss` |
| net_income_loss | Numeric(20,2) | Yes | Net income/loss | `statementOverview.netIncomeLoss` |
| equity | Numeric(20,2) | Yes | Shareholders' equity | `statementOverview.equity` |
| current_assets | Numeric(20,2) | Yes | Current assets | `statementOverview.currentAssets` |
| current_liabilities | Numeric(20,2) | Yes | Current liabilities | `statementOverview.currentLiabilities` |
| total_liabilities | Numeric(20,2) | Yes | Total liabilities | `statementOverview.totalLiabilities` |

### BalanceSheetItem

**Table Name**: `balance_sheet_items`  
**JSON Source**: `companyfinancial.json` - `financialStatements[].balanceSheet[]` array  
**Purpose**: Detailed balance sheet line items

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| statement_id | Integer | No | Foreign key to financial_statements | - |
| item_description | String(500) | Yes | Line item description | `balanceSheet[].itemDescription` |
| item_dnb_code | Integer | Yes | Item D&B code | `balanceSheet[].itemDnBCode` |
| value | Numeric(20,2) | Yes | Line item value | `balanceSheet[].value` |
| priority | Integer | Yes | Display order | `balanceSheet[].priority` |
| item_group_level | Integer | Yes | Hierarchy level | `balanceSheet[].itemGroupLevel` |

### ProfitLossItem

**Table Name**: `profit_loss_items`  
**JSON Source**: `companyfinancial.json` - `financialStatements[].profitAndLoss[]` array  
**Purpose**: Income statement line items

Same structure as BalanceSheetItem.

### CashFlowItem

**Table Name**: `cash_flow_items`  
**JSON Source**: `companyfinancial.json` - `financialStatements[].cashFlow[]` array  
**Purpose**: Cash flow statement line items

Same structure as BalanceSheetItem.

### FinancialRatio

**Table Name**: `financial_ratios`  
**JSON Source**: `companyfinancial.json` - `financialStatements[].financialRatios[]` array  
**Purpose**: Financial ratios and performance metrics

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| statement_id | Integer | No | Foreign key to financial_statements | - |
| ratio_category_description | String(200) | Yes | Category (e.g., "Profitability") | `financialRatios[].ratioCategory.description` |
| ratio_category_dnb_code | Integer | Yes | Category code | `financialRatios[].ratioCategory.dnbCode` |
| ratio_description | String(500) | Yes | Ratio name | `financialRatios[].description` |
| ratio_dnb_code | Integer | Yes | Ratio code | `financialRatios[].dnbCode` |
| value | Numeric(20,6) | Yes | Ratio value | `financialRatios[].value` |

---

## Other Tables

### SignificantEventsSummary

**Table Name**: `significant_events_summary`  
**JSON Source**: `eventsfilings.json` - `organization.significantEvents` object  
**Purpose**: Summary of operational and disaster events

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| has_significant_events | Boolean | Yes | Has any events | `significantEvents.hasSignificantEvents` |
| total_events_count | Integer | Yes | Total event count | `significantEvents.significantEventsSummary.totalEventsCount` |
| most_recent_event_date | Date | Yes | Most recent event date | `significantEvents.significantEventsSummary.mostRecentEventDate` |

### SignificantEvent

**Table Name**: `significant_events`  
**JSON Source**: `eventsfilings.json` - `organization.significantEvents.significantEventsSummary.events[]` array  
**Purpose**: Individual significant events

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| event_id | String(100) | Yes | Event identifier | `events[].eventID` |
| event_date | Date | Yes | Event date | `events[].eventDate` |
| event_type_description | String(200) | Yes | Event type | `events[].eventType.description` |
| event_type_dnb_code | Integer | Yes | Event type code | `events[].eventType.dnbCode` |
| event_category_description | String(200) | Yes | Category | `events[].eventCategory.description` |
| event_category_dnb_code | Integer | Yes | Category code | `events[].eventCategory.dnbCode` |

**Relationships**:
- `text_entries` → SignificantEventTextEntry[] (one-to-many)

### AwardsSummary

**Table Name**: `awards_summary`  
**JSON Source**: `eventsfilings.json` - `organization.awards` object  
**Purpose**: Government contracts and awards summary

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| has_awards | Boolean | Yes | Has any awards | `awards.hasAwards` |
| total_awards_count | Integer | Yes | Total award count | `awards.totalAwardsCount` |
| most_recent_award_date | Date | Yes | Most recent award date | `awards.mostRecentAwardDate` |
| total_awards_amount_value | Numeric(20,2) | Yes | Total amount | `awards.totalAwardsAmount.value` |
| total_awards_amount_currency | String(3) | Yes | Currency | `awards.totalAwardsAmount.currency` |

### Contract

**Table Name**: `contracts`  
**JSON Source**: `eventsfilings.json` - `organization.awards.contracts[]` array  
**Purpose**: Individual government contracts

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| contract_id | String(100) | Yes | Contract identifier | `contracts[].contractID` |
| base_contract_id | String(100) | Yes | Base contract ID | `contracts[].baseContractID` |
| modification_number | String(50) | Yes | Modification number | `contracts[].modificationNumber` |
| signature_date | Date | Yes | Signature date | `contracts[].signatureDate` |
| current_completion_date | Date | Yes | Completion date | `contracts[].currentCompletionDate` |
| description | Text | Yes | Contract description | `contracts[].description` |

**Relationships**:
- `actions` → ContractAction[] (one-to-many)
- `characteristics` → ContractCharacteristic[] (one-to-many)

### ExclusionsSummary

**Table Name**: `exclusions_summary`  
**JSON Source**: `eventsfilings.json` - `organization.exclusions` object  
**Purpose**: Government exclusions summary

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| has_active_exclusions | Boolean | Yes | Has active exclusions | `exclusions.hasActiveExclusions` |
| has_inactive_exclusions | Boolean | Yes | Has inactive exclusions | `exclusions.hasInactiveExclusions` |
| total_active_count | Integer | Yes | Active count | `exclusions.totalActiveExclusionsCount` |
| total_inactive_count | Integer | Yes | Inactive count | `exclusions.totalInactiveExclusionsCount` |
| most_recent_active_date | Date | Yes | Most recent active date | `exclusions.mostRecentActiveExclusionDate` |

### ActiveExclusion

**Table Name**: `active_exclusions`  
**JSON Source**: `eventsfilings.json` - `organization.exclusions.activeExclusions[]` array  
**Purpose**: Active government exclusions

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| exclusion_id | String(100) | Yes | Exclusion identifier | `activeExclusions[].exclusionID` |
| exclusion_date | Date | Yes | Exclusion date | `activeExclusions[].exclusionDate` |
| termination_date | Date | Yes | Termination date | `activeExclusions[].terminationDate` |
| exclusion_type_description | String(200) | Yes | Type | `activeExclusions[].exclusionType.description` |
| exclusion_type_dnb_code | Integer | Yes | Type code | `activeExclusions[].exclusionType.dnbCode` |
| excluding_agency | String(500) | Yes | Agency name | `activeExclusions[].excludingAgency` |
| classification | String(200) | Yes | Classification | `activeExclusions[].classification` |

### ViolationsSummary

**Table Name**: `violations_summary`  
**JSON Source**: `eventsfilings.json` - `organization.violations` object  
**Purpose**: Regulatory violations summary (EPA, OSHA, etc.)

| Field | Type | Nullable | Description | JSON Path |
|-------|------|----------|-------------|-----------|
| id | Integer | No | Primary key | - |
| company_id | Integer | No | Foreign key to companies | - |
| has_epa_violations | Boolean | Yes | Has EPA violations | `violations.hasEPAViolations` |
| has_osha_violations | Boolean | Yes | Has OSHA violations | `violations.hasOSHAViolations` |
| total_epa_violations_count | Integer | Yes | Total EPA count | `violations.totalEPAViolationsCount` |
| total_osha_violations_count | Integer | Yes | Total OSHA count | `violations.totalOSHAViolationsCount` |
| most_recent_epa_violation_date | Date | Yes | Most recent EPA date | `violations.mostRecentEPAViolationDate` |
| most_recent_osha_violation_date | Date | Yes | Most recent OSHA date | `violations.mostRecentOSHAViolationDate` |

---

## Entity Relationship Diagram

```
┌─────────────┐
│   Company   │ (Core entity)
├─────────────┤
│ id          │◄─────────────────┐
│ duns        │                  │
│ primary_name│                  │
└─────────────┘                  │
      │                          │
      │ 1:1                      │ FK: company_id
      ├──────────► CompanyInfo   │
      │            (80+ fields)  │
      │                │         │
      │                │ 1:M     │
      │                ├─► IndustryCode
      │                ├─► TradeStyleName
      │                ├─► MultilingualName
      │                ├─► WebsiteAddress
      │                ├─► TelephoneNumber
      │                ├─► EmailAddress
      │                ├─► RegistrationNumber
      │                ├─► StockExchange
      │                ├─► Bank
      │                ├─► CompanyActivity
      │                ├─► EmployeeFigure
      │                └─► UNSPSCCode
      │
      │ 1:1
      ├──────────► LegalEventsSummary
      │                │ 1:M
      │                ├─► LienFiling ──► LienFilingRolePlayer
      │                ├─► JudgmentFiling ──► JudgmentFilingRolePlayer
      │                ├─► SuitFiling ──► SuitFilingRolePlayer
      │                ├─► Bankruptcy ──► BankruptcyFiling
      │                └─► ClaimFiling ──► ClaimFilingRolePlayer
      │
      │ 1:M
      ├──────────► FinancialStatement
      │                │ 1:1
      │                ├─► FinancialOverview
      │                │ 1:M
      │                ├─► BalanceSheetItem
      │                ├─► ProfitLossItem
      │                ├─► CashFlowItem
      │                └─► FinancialRatio
      │
      │ 1:1
      ├──────────► SignificantEventsSummary
      │                │ 1:M
      │                └─► SignificantEvent ──► SignificantEventTextEntry
      │
      │ 1:1
      ├──────────► AwardsSummary
      │                │ 1:M
      │                └─► Contract ──► ContractAction
      │                            └─► ContractCharacteristic
      │
      │ 1:1
      ├──────────► ExclusionsSummary
      │                │ 1:M
      │                ├─► ActiveExclusion
      │                └─► InactiveExclusion
      │
      └ 1:1────────► ViolationsSummary
```

---

## Data Loading Strategy

### Deduplication: Option A (Delete & Replace)

For CompanyInfo and related tables, the loader implements **Option A** deduplication:

1. **Query** existing CompanyInfo record for the company
2. **Delete** all 12 child table records (IndustryCode, TradeStyleName, etc.)
3. **Delete** the CompanyInfo record
4. **Create** new CompanyInfo record with all 80+ fields
5. **Create** all new child table records from JSON arrays

This ensures:
- ✅ No duplicate records on reload
- ✅ Complete data replacement with latest values
- ✅ Proper cascade deletion of orphaned records
- ✅ Clean state after each load

### JSON Path Resolution

Complex nested paths are resolved using the `_get_nested()` helper function:

```python
# Example: organization.dunsControlStatus.operatingStatus.description
operating_status_desc = _get_nested(org, 'dunsControlStatus', 'operatingStatus', 'description')

# Example: organization.primaryAddress.streetAddress.line1
address_line1 = _get_nested(primary_addr, 'streetAddress', 'line1')
```

---

## Version History

- **v1.1.0** (2025-11-26): Complete CompanyInfo implementation
  - Added 80+ fields to CompanyInfo model
  - Added 12 related tables (IndustryCode, MultilingualName, etc.)
  - Comprehensive loader with nested JSON navigation
  - Three complete addresses (primary, mailing, registered)
  - Full support for multilingual data
  - Employee figures with scope and reliability
  - UNSPSC product/service classifications

- **v1.0.0**: Initial release
  - Legal events (liens, judgments, suits, bankruptcy, claims)
  - Financial statements with line items
  - Significant events, awards, exclusions
  - Option A deduplication strategy

---

## Usage Examples

### Query Company with All Related Data

```python
import datablockAPI as api
from datablockAPI.core.models import Company

# Initialize
api.init('sqlite:///datablock.db')
session = api.get_session()

# Query company with eager loading
company = session.query(Company).filter_by(duns='540924028').first()
info = company.company_info

# Access main fields
print(f"Name: {info.primary_name}")
print(f"Legal Form: {info.legal_form_description}")
print(f"Address: {info.primary_address_line1}, {info.primary_address_locality}")
print(f"Coordinates: ({info.primary_address_latitude}, {info.primary_address_longitude})")

# Access related tables
print(f"Industry Codes: {len(info.industry_codes)}")
for ic in info.industry_codes[:3]:
    print(f"  {ic.code} - {ic.description} ({ic.type_description})")

print(f"Employees: {len(info.employee_figures)}")
for emp in info.employee_figures:
    print(f"  {emp.value} ({emp.information_scope_description}, {emp.reliability_description})")

print(f"Websites: {len(info.website_addresses)}")
for site in info.website_addresses:
    print(f"  {site.url}")
```

### Query Industry Codes

```python
from datablockAPI.core.models import IndustryCode

# Get all NAICS codes
naics_codes = session.query(IndustryCode).filter(
    IndustryCode.type_description.like('%NAICS%')
).order_by(IndustryCode.priority).all()
```

### Query Financial Data

```python
from datablockAPI.core.models import FinancialStatement, FinancialOverview

# Get latest financial statement
stmt = session.query(FinancialStatement).join(
    Company
).filter(
    Company.duns == '540924028'
).order_by(
    FinancialStatement.financial_statement_to_date.desc()
).first()

# Access overview
print(f"Total Assets: {stmt.overview.total_assets} {stmt.currency}")
print(f"Sales: {stmt.overview.sales_revenue} {stmt.currency}")
print(f"Net Income: {stmt.overview.net_income_loss} {stmt.currency}")

# Access detailed line items
for item in stmt.balance_sheet_items:
    print(f"{item.item_description}: {item.value}")
```

---

## Notes

- All monetary fields include both `value` (Numeric) and `currency` (String) columns
- Date fields use Python `date` type; parsed from ISO format strings (YYYY-MM-DD)
- Boolean fields default to `None` (NULL) when not specified in JSON
- All relationships use SQLAlchemy's `relationship()` with proper `back_populates`
- Child tables use `cascade="all, delete-orphan"` for automatic cleanup
- String fields are generously sized to accommodate long values
- Numeric fields use appropriate precision: Numeric(20,2) for money, Numeric(10,6) for coordinates
- All tables include proper foreign key constraints
- Indexes are created on frequently queried fields (e.g., `duns`)

---

**Generated**: November 26, 2025  
**Version**: 1.1.0  
**Repository**: https://github.com/lij-sh/datablocksAPI
