"""
datablockAPI - SQLAlchemy ORM Models
Defines all database tables for companies, events, financials, and related data.
"""

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
import enum

from .database import Base


# ============================================================================
# SHARED/CORE MODELS
# ============================================================================

class Company(Base):
    """Core company entity - shared by all data blocks."""
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    duns = Column(String(9), unique=True, nullable=False, index=True)
    primary_name = Column(String(500))
    country_iso_alpha2_code = Column(String(2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company_info = relationship("CompanyInfo", back_populates="company", uselist=False)
    legal_events_summary = relationship("LegalEventsSummary", back_populates="company", uselist=False)
    awards_summary = relationship("AwardsSummary", back_populates="company", uselist=False)
    exclusions_summary = relationship("ExclusionsSummary", back_populates="company", uselist=False)
    significant_events_summary = relationship("SignificantEventsSummary", back_populates="company", uselist=False)
    financing_events_summary = relationship("FinancingEventsSummary", back_populates="company", uselist=False)
    violations_summary = relationship("ViolationsSummary", back_populates="company", uselist=False)
    
    def __repr__(self):
        return f"<Company(duns='{self.duns}', name='{self.primary_name}')>"


# ============================================================================
# LEGAL EVENTS MODELS
# ============================================================================

class LegalEventsSummary(Base):
    """Summary of all legal events for a company."""
    __tablename__ = 'legal_events_summary'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, unique=True)
    
    # Boolean flags
    has_legal_events = Column(Boolean)
    has_open_legal_events = Column(Boolean)
    has_suits = Column(Boolean)
    has_open_suits = Column(Boolean)
    has_liens = Column(Boolean)
    has_open_liens = Column(Boolean)
    has_bankruptcy = Column(Boolean)
    has_open_bankruptcy = Column(Boolean)
    has_judgments = Column(Boolean)
    has_open_judgments = Column(Boolean)
    has_financial_embarrassment = Column(Boolean)
    has_open_financial_embarrassment = Column(Boolean)
    has_criminal_proceedings = Column(Boolean)
    has_open_criminal_proceedings = Column(Boolean)
    has_claims = Column(Boolean)
    has_open_claims = Column(Boolean)
    has_debarments = Column(Boolean)  # Deprecated - use exclusions
    has_open_debarments = Column(Boolean)
    has_insolvency = Column(Boolean)
    has_liquidation = Column(Boolean)
    has_suspension_of_payments = Column(Boolean)
    has_other_legal_events = Column(Boolean)
    
    # Relationships
    company = relationship("Company", back_populates="legal_events_summary")


# Liens
class Lien(Base):
    """Lien event type with summary information."""
    __tablename__ = 'liens'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    most_recent_filing_date = Column(Date)
    open_count = Column(Integer)
    open_amount_value = Column(Numeric(precision=18, scale=2))
    open_amount_currency = Column(String(3))
    period_summary_json = Column(JSON)  # Flexible storage for period summaries
    
    # Relationships
    company = relationship("Company")
    filings = relationship("LienFiling", back_populates="lien", cascade="all, delete-orphan")


class LienFiling(Base):
    """Individual lien filing record."""
    __tablename__ = 'lien_filings'
    
    id = Column(Integer, primary_key=True)
    lien_id = Column(Integer, ForeignKey('liens.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    # Filing details
    is_stop_d = Column(Boolean)
    filing_type_description = Column(String(200))
    filing_type_dnb_code = Column(Integer)
    filing_class_description = Column(String(200))
    filing_class_dnb_code = Column(Integer)
    filing_sub_type = Column(String(200))
    filing_date = Column(Date)
    received_date = Column(Date)
    published_date = Column(Date)
    verified_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    end_indicator = Column(Boolean)
    legal_hearing_date = Column(Date)
    actual_legal_hearing_date = Column(Date)
    event_duration = Column(String(50))
    filing_medium = Column(String(200))
    jurisdiction_type_desc = Column(String(200))
    jurisdiction_type_dnb_code = Column(Integer)
    filing_reference = Column(String(200))
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    awarded_amount_value = Column(Numeric(precision=18, scale=2))
    awarded_amount_currency = Column(String(3))
    original_filing_date = Column(Date)
    filing_chapter = Column(String(50))
    status_description = Column(String(200))
    status_dnb_code = Column(Integer)
    status_date = Column(Date)
    court_name = Column(String(500))
    court_type_description = Column(String(200))
    has_historical_event = Column(Boolean)
    priority = Column(Integer)
    priority_group = Column(String(100))
    
    # Relationships
    lien = relationship("Lien", back_populates="filings")
    company = relationship("Company")
    role_players = relationship("LienFilingRolePlayer", back_populates="filing", cascade="all, delete-orphan")
    reference_dates = relationship("LienFilingReferenceDate", back_populates="filing", cascade="all, delete-orphan")
    text_entries = relationship("LienFilingTextEntry", back_populates="filing", cascade="all, delete-orphan")


class LienFilingRolePlayer(Base):
    """Role players (participants) in lien filings."""
    __tablename__ = 'lien_filing_role_players'
    
    id = Column(Integer, primary_key=True)
    lien_filing_id = Column(Integer, ForeignKey('lien_filings.id'), nullable=False)
    
    role_player_type_desc = Column(String(200))
    role_player_type_dnb_code = Column(Integer)
    name = Column(String(500))
    employer_name = Column(String(500))
    duns = Column(String(9))
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    address_line1 = Column(String(500))
    address_line2 = Column(String(500))
    city = Column(String(200))
    region_name = Column(String(200))
    region_abbr = Column(String(50))
    postal_code = Column(String(50))
    country_name = Column(String(200))
    country_iso_alpha2_code = Column(String(2))
    telephone = Column(String(50))
    operating_status = Column(String(200))
    
    # Relationship
    filing = relationship("LienFiling", back_populates="role_players")


class LienFilingReferenceDate(Base):
    """Reference dates for lien filings."""
    __tablename__ = 'lien_filing_ref_dates'
    
    id = Column(Integer, primary_key=True)
    lien_filing_id = Column(Integer, ForeignKey('lien_filings.id'), nullable=False)
    
    reference_type_desc = Column(String(200))
    reference_type_dnb_code = Column(Integer)
    reference_date = Column(Date)
    
    # Relationship
    filing = relationship("LienFiling", back_populates="reference_dates")


class LienFilingTextEntry(Base):
    """Text entries for lien filings."""
    __tablename__ = 'lien_filing_text_entries'
    
    id = Column(Integer, primary_key=True)
    lien_filing_id = Column(Integer, ForeignKey('lien_filings.id'), nullable=False)
    
    type_description = Column(String(200))
    type_dnb_code = Column(Integer)
    priority = Column(Integer)
    text = Column(Text)
    language_description = Column(String(100))
    language_dnb_code = Column(Integer)
    
    # Relationship
    filing = relationship("LienFiling", back_populates="text_entries")


# Note: Judgments, Suits, Bankruptcy, Claims, Insolvency, Liquidation, OtherLegalEvents
# follow the same pattern as Liens. For brevity, I'll create placeholder classes.
# These will be fully implemented with the same structure.

class Judgment(Base):
    """Judgment event type."""
    __tablename__ = 'judgments'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    most_recent_filing_date = Column(Date)
    open_count = Column(Integer)
    open_amount_value = Column(Numeric(precision=18, scale=2))
    open_amount_currency = Column(String(3))
    period_summary_json = Column(JSON)
    
    company = relationship("Company")
    filings = relationship("JudgmentFiling", back_populates="judgment", cascade="all, delete-orphan")


class JudgmentFiling(Base):
    """Individual judgment filing - same structure as LienFiling."""
    __tablename__ = 'judgment_filings'
    
    id = Column(Integer, primary_key=True)
    judgment_id = Column(Integer, ForeignKey('judgments.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    # Same fields as LienFiling
    is_stop_d = Column(Boolean)
    filing_type_description = Column(String(200))
    filing_type_dnb_code = Column(Integer)
    filing_date = Column(Date)
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    status_description = Column(String(200))
    status_date = Column(Date)
    # ... (all other fields same as LienFiling)
    
    judgment = relationship("Judgment", back_populates="filings")
    company = relationship("Company")
    role_players = relationship("JudgmentFilingRolePlayer", back_populates="filing", cascade="all, delete-orphan")


class JudgmentFilingRolePlayer(Base):
    """Role players in judgment filings."""
    __tablename__ = 'judgment_filing_role_players'
    
    id = Column(Integer, primary_key=True)
    judgment_filing_id = Column(Integer, ForeignKey('judgment_filings.id'), nullable=False)
    
    role_player_type_desc = Column(String(200))
    role_player_type_dnb_code = Column(Integer)
    name = Column(String(500))
    employer_name = Column(String(500))
    duns = Column(String(9))
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    address_line1 = Column(String(500))
    address_line2 = Column(String(500))
    city = Column(String(200))
    region_name = Column(String(200))
    region_abbr = Column(String(50))
    postal_code = Column(String(50))
    country_name = Column(String(200))
    country_iso_alpha2_code = Column(String(2))
    telephone = Column(String(50))
    operating_status = Column(String(200))
    
    filing = relationship("JudgmentFiling", back_populates="role_players")


# Placeholder classes for other legal event types
class Suit(Base):
    """Suit event type."""
    __tablename__ = 'suits'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    most_recent_filing_date = Column(Date)
    open_count = Column(Integer)
    open_amount_value = Column(Numeric(precision=18, scale=2))
    open_amount_currency = Column(String(3))
    period_summary_json = Column(JSON)
    company = relationship("Company")
    filings = relationship("SuitFiling", back_populates="suit", cascade="all, delete-orphan")


class SuitFiling(Base):
    """Individual suit filing - same structure as LienFiling."""
    __tablename__ = 'suit_filings'
    
    id = Column(Integer, primary_key=True)
    suit_id = Column(Integer, ForeignKey('suits.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    is_stop_d = Column(Boolean)
    filing_type_description = Column(String(200))
    filing_type_dnb_code = Column(Integer)
    filing_date = Column(Date)
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    status_description = Column(String(200))
    status_date = Column(Date)
    
    suit = relationship("Suit", back_populates="filings")
    company = relationship("Company")
    role_players = relationship("SuitFilingRolePlayer", back_populates="filing", cascade="all, delete-orphan")


class SuitFilingRolePlayer(Base):
    """Role players in suit filings."""
    __tablename__ = 'suit_filing_role_players'
    
    id = Column(Integer, primary_key=True)
    suit_filing_id = Column(Integer, ForeignKey('suit_filings.id'), nullable=False)
    
    role_player_type_desc = Column(String(200))
    role_player_type_dnb_code = Column(Integer)
    name = Column(String(500))
    employer_name = Column(String(500))
    duns = Column(String(9))
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    address_line1 = Column(String(500))
    address_line2 = Column(String(500))
    city = Column(String(200))
    region_name = Column(String(200))
    region_abbr = Column(String(50))
    postal_code = Column(String(50))
    country_name = Column(String(200))
    country_iso_alpha2_code = Column(String(2))
    telephone = Column(String(50))
    operating_status = Column(String(200))
    
    filing = relationship("SuitFiling", back_populates="role_players")


class Bankruptcy(Base):
    """Bankruptcy event type."""
    __tablename__ = 'bankruptcies'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    most_recent_filing_date = Column(Date)
    period_summary_json = Column(JSON)
    company = relationship("Company")
    filings = relationship("BankruptcyFiling", back_populates="bankruptcy", cascade="all, delete-orphan")


class BankruptcyFiling(Base):
    """Individual bankruptcy filing."""
    __tablename__ = 'bankruptcy_filings'
    
    id = Column(Integer, primary_key=True)
    bankruptcy_id = Column(Integer, ForeignKey('bankruptcies.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    is_stop_d = Column(Boolean)
    filing_type_description = Column(String(200))
    filing_type_dnb_code = Column(Integer)
    filing_date = Column(Date)
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    status_description = Column(String(200))
    status_date = Column(Date)
    
    bankruptcy = relationship("Bankruptcy", back_populates="filings")
    company = relationship("Company")
    role_players = relationship("BankruptcyFilingRolePlayer", back_populates="filing", cascade="all, delete-orphan")


class BankruptcyFilingRolePlayer(Base):
    """Role players in bankruptcy filings."""
    __tablename__ = 'bankruptcy_filing_role_players'
    
    id = Column(Integer, primary_key=True)
    bankruptcy_filing_id = Column(Integer, ForeignKey('bankruptcy_filings.id'), nullable=False)
    
    role_player_type_desc = Column(String(200))
    role_player_type_dnb_code = Column(Integer)
    name = Column(String(500))
    employer_name = Column(String(500))
    duns = Column(String(9))
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    address_line1 = Column(String(500))
    address_line2 = Column(String(500))
    city = Column(String(200))
    region_name = Column(String(200))
    region_abbr = Column(String(50))
    postal_code = Column(String(50))
    country_name = Column(String(200))
    country_iso_alpha2_code = Column(String(2))
    telephone = Column(String(50))
    operating_status = Column(String(200))
    
    filing = relationship("BankruptcyFiling", back_populates="role_players")


class Claim(Base):
    """Claim event type."""
    __tablename__ = 'claims'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    open_count = Column(Integer)
    open_amount_value = Column(Numeric(precision=18, scale=2))
    open_amount_currency = Column(String(3))
    company = relationship("Company")
    filings = relationship("ClaimFiling", back_populates="claim", cascade="all, delete-orphan")


class ClaimFiling(Base):
    """Individual claim filing."""
    __tablename__ = 'claim_filings'
    
    id = Column(Integer, primary_key=True)
    claim_id = Column(Integer, ForeignKey('claims.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    is_stop_d = Column(Boolean)
    filing_type_description = Column(String(200))
    filing_type_dnb_code = Column(Integer)
    filing_date = Column(Date)
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    status_description = Column(String(200))
    status_date = Column(Date)
    
    claim = relationship("Claim", back_populates="filings")
    company = relationship("Company")
    role_players = relationship("ClaimFilingRolePlayer", back_populates="filing", cascade="all, delete-orphan")


class ClaimFilingRolePlayer(Base):
    """Role players in claim filings."""
    __tablename__ = 'claim_filing_role_players'
    
    id = Column(Integer, primary_key=True)
    claim_filing_id = Column(Integer, ForeignKey('claim_filings.id'), nullable=False)
    
    role_player_type_desc = Column(String(200))
    role_player_type_dnb_code = Column(Integer)
    name = Column(String(500))
    employer_name = Column(String(500))
    duns = Column(String(9))
    filing_amount_value = Column(Numeric(precision=18, scale=2))
    filing_amount_currency = Column(String(3))
    address_line1 = Column(String(500))
    address_line2 = Column(String(500))
    city = Column(String(200))
    region_name = Column(String(200))
    region_abbr = Column(String(50))
    postal_code = Column(String(50))
    country_name = Column(String(200))
    country_iso_alpha2_code = Column(String(2))
    telephone = Column(String(50))
    operating_status = Column(String(200))
    
    filing = relationship("ClaimFiling", back_populates="role_players")


class Insolvency(Base):
    __tablename__ = 'insolvencies'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship("Company")


class Liquidation(Base):
    __tablename__ = 'liquidations'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship("Company")


class OtherLegalEvent(Base):
    __tablename__ = 'other_legal_events'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship("Company")


# ============================================================================
# AWARDS MODELS
# ============================================================================

class AwardsSummary(Base):
    """Summary of all awards for a company."""
    __tablename__ = 'awards_summary'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, unique=True)
    
    has_contracts = Column(Boolean)
    has_loans = Column(Boolean)
    has_debts = Column(Boolean)
    has_grants = Column(Boolean)
    has_open_contracts = Column(Boolean)
    has_open_loans = Column(Boolean)
    has_open_debts = Column(Boolean)
    has_open_grants = Column(Boolean)
    obligated_contracts_amt_val = Column(Numeric(precision=18, scale=2))
    obligated_contracts_amt_curr = Column(String(3))
    current_contracts_amt_val = Column(Numeric(precision=18, scale=2))
    current_contracts_amt_curr = Column(String(3))
    total_open_contracts_count = Column(Integer)
    total_open_contracts_amt_val = Column(Numeric(precision=18, scale=2))
    total_open_contracts_amt_curr = Column(String(3))
    total_contracts_amt_val = Column(Numeric(precision=18, scale=2))
    total_contracts_amt_curr = Column(String(3))
    most_recent_contract_date = Column(Date)
    most_recent_loan_date = Column(Date)
    most_recent_debt_date = Column(Date)
    most_recent_grant_date = Column(Date)
    
    company = relationship("Company", back_populates="awards_summary")


class Contract(Base):
    """Contract award record."""
    __tablename__ = 'contracts'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    award_id = Column(String(500))
    award_description = Column(Text)
    award_modification_number = Column(String(50))
    contract_id = Column(String(200))
    contract_type_code = Column(String(50))
    contract_type_description = Column(String(200))
    contract_price_type_code = Column(String(50))
    contract_price_type_desc = Column(String(200))
    base_all_options_amt_value = Column(Numeric(precision=18, scale=2))
    base_all_options_amt_currency = Column(String(3))
    current_total_amt_value = Column(Numeric(precision=18, scale=2))
    current_total_amt_currency = Column(String(3))
    funding_agency_code = Column(String(50))
    funding_agency_description = Column(String(500))
    awarding_office_code = Column(String(50))
    awarding_office_description = Column(String(500))
    
    company = relationship("Company")
    actions = relationship("ContractAction", back_populates="contract", cascade="all, delete-orphan")
    characteristics = relationship("ContractCharacteristic", back_populates="contract", cascade="all, delete-orphan")


class ContractAction(Base):
    """Actions within a contract."""
    __tablename__ = 'contract_actions'
    
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    
    action_date = Column(Date)
    action_fiscal_year = Column(String(4))
    actions_count = Column(Integer)
    effective_date = Column(Date)
    expiration_date = Column(Date)
    federal_funding_amt_value = Column(Numeric(precision=18, scale=2))
    federal_funding_amt_currency = Column(String(3))
    
    contract = relationship("Contract", back_populates="actions")


class ContractCharacteristic(Base):
    """Characteristics of a contract."""
    __tablename__ = 'contract_characteristics'
    
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    
    description = Column(String(500))
    dnb_code = Column(Integer)
    
    contract = relationship("Contract", back_populates="characteristics")


# ============================================================================
# EXCLUSIONS MODELS
# ============================================================================

class ExclusionsSummary(Base):
    """Summary of exclusions for a company."""
    __tablename__ = 'exclusions_summary'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, unique=True)
    
    has_active_exclusions = Column(Boolean)
    has_inactive_exclusions = Column(Boolean)
    active_exclusions_count = Column(Integer)
    inactive_exclusions_count = Column(Integer)
    most_recent_active_exclusion_date = Column(Date)
    most_recent_inactive_exclusion_date = Column(Date)
    
    company = relationship("Company")


class ActiveExclusion(Base):
    """Active exclusion record."""
    __tablename__ = 'active_exclusions'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    sam_record_number = Column(String(200))
    cage_code = Column(String(50))
    classification_type_desc = Column(String(200))
    classification_type_dnb_code = Column(Integer)
    program_type_desc = Column(String(200))
    agency_name = Column(String(500))
    effective_date = Column(Date)
    expiration_date = Column(Date)
    sam_record_update_date = Column(Date)
    agency_comments = Column(Text)
    
    company = relationship("Company")


class InactiveExclusion(Base):
    """Inactive exclusion record."""
    __tablename__ = 'inactive_exclusions'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    sam_record_number = Column(String(200))
    cage_code = Column(String(50))
    classification_type_desc = Column(String(200))
    effective_date = Column(Date)
    expiration_date = Column(Date)
    agency_name = Column(String(500))
    
    company = relationship("Company")


# ============================================================================
# OTHER EVENT MODELS (PLACEHOLDERS)
# ============================================================================

class SignificantEventsSummary(Base):
    """Summary of significant events - boolean flags only."""
    __tablename__ = 'significant_events_summary'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, unique=True)
    
    # Boolean flags from JSON
    has_significant_events = Column(Boolean)
    has_operational_events = Column(Boolean)
    has_disastrous_events = Column(Boolean)
    has_burglary_occured = Column(Boolean)
    has_fire_occurred = Column(Boolean)
    has_business_discontinued = Column(Boolean)
    has_name_change = Column(Boolean)
    has_partner_change = Column(Boolean)
    has_ceo_change = Column(Boolean)
    has_control_change = Column(Boolean)
    
    company = relationship("Company", back_populates="significant_events_summary")


class SignificantEvent(Base):
    """Individual significant event record - direct from events array."""
    __tablename__ = 'significant_events'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    # Event details from JSON events array
    event_date = Column(Date)
    event_type_description = Column(String(200))
    event_type_dnb_code = Column(Integer)
    start_date = Column(Date)
    
    # Impact details
    impact_details = Column(Text)
    impact_amount_value = Column(Numeric(precision=18, scale=2))
    impact_amount_currency = Column(String(3))
    impacted_premises_type = Column(String(200))
    damaged_assets_class = Column(String(200))
    impacted_children = Column(Integer)
    insurance_claim_settlement_amount_value = Column(Numeric(precision=18, scale=2))
    insurance_claim_settlement_amount_currency = Column(String(3))
    
    # Data provider
    data_provider_description = Column(String(500))
    data_provider_dnb_code = Column(Integer)
    
    # Relationships
    company = relationship("Company")
    text_entries = relationship("SignificantEventTextEntry", back_populates="event", cascade="all, delete-orphan")


class SignificantEventTextEntry(Base):
    """Text entries for significant events."""
    __tablename__ = 'significant_event_text_entries'
    
    id = Column(Integer, primary_key=True)
    significant_event_id = Column(Integer, ForeignKey('significant_events.id'), nullable=False)
    
    text = Column(Text)
    priority = Column(Integer)
    type_description = Column(String(200))
    type_dnb_code = Column(Integer)
    
    event = relationship("SignificantEvent", back_populates="text_entries")


class FinancingEventsSummary(Base):
    """Summary of financing events."""
    __tablename__ = 'financing_events_summary'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, unique=True)
    
    has_financing_events = Column(Boolean)
    has_secured_filings = Column(Boolean)
    has_ucc_filings = Column(Boolean)
    most_recent_filing_date = Column(Date)
    total_filings_count = Column(Integer)
    total_secured_amount_value = Column(Numeric(precision=18, scale=2))
    total_secured_amount_currency = Column(String(3))
    
    company = relationship("Company", back_populates="financing_events_summary")


class FinancingEvent(Base):
    """Financing event record (UCC filings, secured transactions)."""
    __tablename__ = 'financing_events'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    filing_type_description = Column(String(200))
    filing_type_dnb_code = Column(Integer)
    most_recent_filing_date = Column(Date)
    total_filings_count = Column(Integer)
    
    company = relationship("Company")
    filings = relationship("FinancingEventFiling", back_populates="event", cascade="all, delete-orphan")


class FinancingEventFiling(Base):
    """Individual financing event filing (UCC, secured transaction)."""
    __tablename__ = 'financing_event_filings'
    
    id = Column(Integer, primary_key=True)
    financing_event_id = Column(Integer, ForeignKey('financing_events.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    # Filing details
    filing_number = Column(String(200))
    filing_date = Column(Date)
    filing_type_description = Column(String(200))
    filing_type_dnb_code = Column(Integer)
    filing_jurisdiction = Column(String(200))
    
    # Dates
    received_date = Column(Date)
    expiration_date = Column(Date)
    lapse_date = Column(Date)
    termination_date = Column(Date)
    
    # Secured party info
    secured_party_name = Column(String(500))
    secured_party_address = Column(String(500))
    
    # Debtor info
    debtor_name = Column(String(500))
    debtor_duns = Column(String(9))
    
    # Collateral
    collateral_description = Column(Text)
    collateral_value = Column(Numeric(precision=18, scale=2))
    collateral_currency = Column(String(3))
    
    # Status
    status_description = Column(String(200))
    status_dnb_code = Column(Integer)
    is_active = Column(Boolean)
    
    # Relationships
    event = relationship("FinancingEvent", back_populates="filings")
    company = relationship("Company")


class ViolationsSummary(Base):
    """Summary of violations."""
    __tablename__ = 'violations_summary'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, unique=True)
    
    has_epa_violations = Column(Boolean)
    has_osha_violations = Column(Boolean)
    has_fda_violations = Column(Boolean)
    has_other_violations = Column(Boolean)
    total_epa_violations_count = Column(Integer)
    total_osha_violations_count = Column(Integer)
    total_fda_violations_count = Column(Integer)
    most_recent_violation_date = Column(Date)
    
    company = relationship("Company", back_populates="violations_summary")


class Violation(Base):
    """Violation record (EPA, OSHA, FDA, etc.)."""
    __tablename__ = 'violations'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    # Violation type
    violation_type_description = Column(String(200))
    violation_type_dnb_code = Column(Integer)
    agency_name = Column(String(500))
    agency_code = Column(String(50))
    
    # Violation details
    violation_date = Column(Date)
    citation_number = Column(String(200))
    case_number = Column(String(200))
    severity_level = Column(String(100))
    
    # Violation description
    violation_description = Column(Text)
    regulation_violated = Column(String(500))
    standard_violated = Column(String(500))
    
    # Penalty information
    initial_penalty_value = Column(Numeric(precision=18, scale=2))
    initial_penalty_currency = Column(String(3))
    current_penalty_value = Column(Numeric(precision=18, scale=2))
    current_penalty_currency = Column(String(3))
    
    # Status
    status_description = Column(String(200))
    status_dnb_code = Column(Integer)
    status_date = Column(Date)
    is_contested = Column(Boolean)
    is_repeat_violation = Column(Boolean)
    
    # Resolution
    resolution_date = Column(Date)
    resolution_description = Column(Text)
    abatement_date = Column(Date)
    
    # Location
    facility_name = Column(String(500))
    facility_address = Column(String(500))
    facility_city = Column(String(200))
    facility_state = Column(String(50))
    facility_postal_code = Column(String(50))
    
    company = relationship("Company")


# ============================================================================
# FINANCIALS MODELS (BASIC STRUCTURE)
# ============================================================================

class FinancialStatement(Base):
    """Financial statement record - main header for a financial period."""
    __tablename__ = 'financial_statements'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    statement_type = Column(String(50))  # 'fiscal_latest' or 'other'
    financial_statement_to_date = Column(Date)
    financial_statement_from_date = Column(Date)
    financial_statement_duration = Column(String(20))  # e.g., 'P12M'
    filing_date = Column(Date)
    received_timestamp = Column(Date)
    approval_date = Column(Date)
    currency = Column(String(3))
    units = Column(String(50))
    
    # Data provider info
    data_provider_description = Column(String(500))
    data_provider_dnb_code = Column(Integer)
    
    # Statement template
    statement_template_description = Column(String(200))
    statement_template_dnb_code = Column(Integer)
    
    # Scope and reliability
    information_scope_description = Column(String(200))
    information_scope_dnb_code = Column(Integer)
    reliability_description = Column(String(200))
    reliability_dnb_code = Column(Integer)
    
    # Boolean flags
    is_fiscal = Column(Boolean)
    is_interim = Column(Boolean)
    is_audited = Column(Boolean)
    is_audit_unknown = Column(Boolean)
    is_final = Column(Boolean)
    is_opening = Column(Boolean)
    is_proforma = Column(Boolean)
    is_signed = Column(Boolean)
    is_qualified = Column(Boolean)
    is_restated = Column(Boolean)
    is_trial_balance = Column(Boolean)
    is_unbalanced = Column(Boolean)
    
    # Auditor info
    accountant_name = Column(String(500))
    not_audited_reason = Column(String(500))
    
    # Relationships
    company = relationship("Company")
    overview = relationship("FinancialOverview", back_populates="statement", uselist=False, cascade="all, delete-orphan")
    balance_sheet_items = relationship("BalanceSheetItem", back_populates="statement", cascade="all, delete-orphan")
    profit_loss_items = relationship("ProfitLossItem", back_populates="statement", cascade="all, delete-orphan")
    cash_flow_items = relationship("CashFlowItem", back_populates="statement", cascade="all, delete-orphan")
    financial_ratios = relationship("FinancialRatio", back_populates="statement", cascade="all, delete-orphan")


class FinancialOverview(Base):
    """Financial overview - summary-level financial metrics."""
    __tablename__ = 'financial_overview'
    
    id = Column(Integer, primary_key=True)
    statement_id = Column(Integer, ForeignKey('financial_statements.id'), nullable=False, unique=True)
    
    # Assets - Current
    cash_and_liquid_assets = Column(Numeric(precision=20, scale=2))
    marketable_securities = Column(Numeric(precision=20, scale=2))
    accounts_receivable = Column(Numeric(precision=20, scale=2))
    due_from_group_short_term = Column(Numeric(precision=20, scale=2))
    other_receivables = Column(Numeric(precision=20, scale=2))
    total_receivables = Column(Numeric(precision=20, scale=2))
    inventory = Column(Numeric(precision=20, scale=2))
    prepaid_deferred_short_term = Column(Numeric(precision=20, scale=2))
    other_current_assets = Column(Numeric(precision=20, scale=2))
    total_current_assets = Column(Numeric(precision=20, scale=2))
    
    # Assets - Long Term
    tangible_fixed_assets = Column(Numeric(precision=20, scale=2))
    due_from_group_long_term = Column(Numeric(precision=20, scale=2))
    investments_long_term = Column(Numeric(precision=20, scale=2))
    intangible_assets = Column(Numeric(precision=20, scale=2))
    other_long_term_assets = Column(Numeric(precision=20, scale=2))
    total_long_term_assets = Column(Numeric(precision=20, scale=2))
    other_unclassified_assets = Column(Numeric(precision=20, scale=2))
    total_assets = Column(Numeric(precision=20, scale=2))
    
    # Liabilities - Current
    accounts_payable = Column(Numeric(precision=20, scale=2))
    accruals_other_payables = Column(Numeric(precision=20, scale=2))
    short_term_debt = Column(Numeric(precision=20, scale=2))
    due_to_group_short_term = Column(Numeric(precision=20, scale=2))
    taxes_short_term = Column(Numeric(precision=20, scale=2))
    other_current_liabilities = Column(Numeric(precision=20, scale=2))
    total_current_liabilities = Column(Numeric(precision=20, scale=2))
    
    # Liabilities - Long Term
    long_term_debt = Column(Numeric(precision=20, scale=2))
    due_to_group_long_term = Column(Numeric(precision=20, scale=2))
    deferred_credit_income = Column(Numeric(precision=20, scale=2))
    deferred_taxes_long_term = Column(Numeric(precision=20, scale=2))
    other_long_term_liabilities = Column(Numeric(precision=20, scale=2))
    total_long_term_liabilities = Column(Numeric(precision=20, scale=2))
    provisions = Column(Numeric(precision=20, scale=2))
    other_unclassified_liabilities = Column(Numeric(precision=20, scale=2))
    total_liabilities = Column(Numeric(precision=20, scale=2))
    
    # Equity
    capital_stock = Column(Numeric(precision=20, scale=2))
    capital_surplus = Column(Numeric(precision=20, scale=2))
    retained_earnings = Column(Numeric(precision=20, scale=2))
    capital_reserves = Column(Numeric(precision=20, scale=2))
    other_unrestricted_reserves = Column(Numeric(precision=20, scale=2))
    restricted_equity = Column(Numeric(precision=20, scale=2))
    other_equity = Column(Numeric(precision=20, scale=2))
    minority_interest = Column(Numeric(precision=20, scale=2))
    net_worth = Column(Numeric(precision=20, scale=2))
    total_liabilities_equity = Column(Numeric(precision=20, scale=2))
    
    # Income Statement
    sales_revenue = Column(Numeric(precision=20, scale=2))
    cost_of_sales = Column(Numeric(precision=20, scale=2))
    gross_profit = Column(Numeric(precision=20, scale=2))
    operating_profit = Column(Numeric(precision=20, scale=2))
    profit_before_taxes = Column(Numeric(precision=20, scale=2))
    profit_after_tax = Column(Numeric(precision=20, scale=2))
    dividends = Column(Numeric(precision=20, scale=2))
    
    # Calculated Metrics
    total_indebtedness = Column(Numeric(precision=20, scale=2))
    working_capital = Column(Numeric(precision=20, scale=2))
    net_current_assets = Column(Numeric(precision=20, scale=2))
    tangible_net_worth = Column(Numeric(precision=20, scale=2))
    
    # Financial Ratios
    current_ratio = Column(Numeric(precision=10, scale=4))
    quick_ratio = Column(Numeric(precision=10, scale=4))
    current_liabilities_over_net_worth = Column(Numeric(precision=10, scale=4))
    total_liabilities_over_net_worth = Column(Numeric(precision=10, scale=4))
    
    # Relationship
    statement = relationship("FinancialStatement", back_populates="overview")


class BalanceSheetItem(Base):
    """Individual line item from balance sheet."""
    __tablename__ = 'balance_sheet_items'
    
    id = Column(Integer, primary_key=True)
    statement_id = Column(Integer, ForeignKey('financial_statements.id'), nullable=False)
    
    # Item identification
    item_description = Column(String(500))
    item_dnb_code = Column(Integer)
    
    # Item value and classification
    value = Column(Numeric(precision=20, scale=2))
    priority = Column(Integer)  # Sort order
    item_group_level = Column(Integer)  # Hierarchy level (10=highest, 40=detail)
    
    # Section identifier (assets/liabilities/equity)
    section = Column(String(50))  # 'assets', 'liabilities', 'equity'
    
    # Relationship
    statement = relationship("FinancialStatement", back_populates="balance_sheet_items")


class ProfitLossItem(Base):
    """Individual line item from profit & loss statement."""
    __tablename__ = 'profit_loss_items'
    
    id = Column(Integer, primary_key=True)
    statement_id = Column(Integer, ForeignKey('financial_statements.id'), nullable=False)
    
    # Item identification
    item_description = Column(String(500))
    item_dnb_code = Column(Integer)
    
    # Item value and classification
    value = Column(Numeric(precision=20, scale=2))
    priority = Column(Integer)  # Sort order
    item_group_level = Column(Integer)  # Hierarchy level
    
    # Relationship
    statement = relationship("FinancialStatement", back_populates="profit_loss_items")


class CashFlowItem(Base):
    """Individual line item from cash flow statement."""
    __tablename__ = 'cash_flow_items'
    
    id = Column(Integer, primary_key=True)
    statement_id = Column(Integer, ForeignKey('financial_statements.id'), nullable=False)
    
    # Item identification
    item_description = Column(String(500))
    item_dnb_code = Column(Integer)
    
    # Item value and classification
    value = Column(Numeric(precision=20, scale=2))
    priority = Column(Integer)  # Sort order
    item_group_level = Column(Integer)  # Hierarchy level
    
    # Relationship
    statement = relationship("FinancialStatement", back_populates="cash_flow_items")


class FinancialRatio(Base):
    """Financial ratios and performance metrics."""
    __tablename__ = 'financial_ratios'
    
    id = Column(Integer, primary_key=True)
    statement_id = Column(Integer, ForeignKey('financial_statements.id'), nullable=False)
    
    # Ratio identification
    ratio_description = Column(String(500))
    ratio_dnb_code = Column(Integer)
    
    # Ratio value and ranking
    value = Column(Numeric(precision=20, scale=6))
    relative_industry_rank = Column(Numeric(precision=10, scale=4))
    priority = Column(Integer)
    item_group_level = Column(Integer)
    
    # Relationship
    statement = relationship("FinancialStatement", back_populates="financial_ratios")


# ============================================================================
# COMPANY INFO MODELS (BASIC STRUCTURE)
# ============================================================================

class CompanyInfo(Base):
    """Company information and metadata."""
    __tablename__ = 'company_info'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, unique=True)
    
    is_fortune_1000_listed = Column(Boolean)
    is_forbes_listed = Column(Boolean)
    is_standalone = Column(Boolean)
    is_small_business = Column(Boolean)
    incorporated_date = Column(Date)
    fiscal_year_end = Column(String(10))
    
    company = relationship("Company", back_populates="company_info")
