"""
datablockAPI - Data Loader Module
Handles loading JSON data into the database.
"""

import json
from pathlib import Path
from typing import List, Union, Dict, Any
from datetime import datetime, date
from decimal import Decimal

from .database import get_session
from .models import (
    Company, LegalEventsSummary, Lien, LienFiling, LienFilingRolePlayer,
    LienFilingReferenceDate, LienFilingTextEntry,
    Judgment, JudgmentFiling, JudgmentFilingRolePlayer,
    Suit, SuitFiling, SuitFilingRolePlayer,
    Bankruptcy, BankruptcyFiling, BankruptcyFilingRolePlayer,
    Claim, ClaimFiling, ClaimFilingRolePlayer,
    AwardsSummary, Contract, ContractAction, ContractCharacteristic,
    ExclusionsSummary, ActiveExclusion, InactiveExclusion,
    SignificantEventsSummary, SignificantEvent, SignificantEventTextEntry,
    FinancingEventsSummary, ViolationsSummary,
    FinancialStatement, FinancialOverview, BalanceSheetItem, ProfitLossItem,
    CashFlowItem, FinancialRatio, CompanyInfo
)


def load(json_files: Union[str, List[str]]):
    """
    Load JSON data files into the database.
    
    Args:
        json_files: Single JSON file path or list of JSON file paths
    
    Examples:
        >>> import datablockAPI as api
        >>> api.load('companyinfo.json')
        >>> api.load(['companyinfo.json', 'companyfinancial.json', 'eventsfilings.json'])
    """
    if isinstance(json_files, str):
        json_files = [json_files]
    
    session = get_session()
    
    try:
        for json_file in json_files:
            print(f"\n📁 Loading: {json_file}")
            _load_json_file(session, json_file)
            print(f"✓ Completed: {json_file}")
        
        session.commit()
        print(f"\n✓ Successfully loaded {len(json_files)} file(s)")
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ Error loading data: {e}")
        raise
    finally:
        session.close()


def _load_json_file(session, json_file: str):
    """Load a single JSON file."""
    file_path = Path(json_file)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Determine file type by blockIDs
    block_ids = data.get('inquiryDetail', {}).get('blockIDs', [])
    
    if not block_ids:
        print(f"  ⚠ No blockIDs found in file")
        return
    
    block_id = block_ids[0]
    
    # Route to appropriate loader based on block ID
    if 'companyinfo' in block_id.lower():
        _load_company_info(session, data)
    elif 'companyfinancial' in block_id.lower():
        _load_company_financials(session, data)
    elif 'eventfiling' in block_id.lower():
        _load_events_filings(session, data)
    else:
        print(f"  ⚠ Unknown blockID: {block_id}")


def _get_or_create_company(session, org_data: Dict) -> Company:
    """Get existing company or create new one."""
    duns = org_data.get('duns')
    
    if not duns:
        raise ValueError("DUNS number is required")
    
    company = session.query(Company).filter_by(duns=duns).first()
    
    if not company:
        company = Company(
            duns=duns,
            primary_name=org_data.get('primaryName'),
            country_iso_alpha2_code=org_data.get('countryISOAlpha2Code')
        )
        session.add(company)
        session.flush()  # Get the ID
        print(f"  ✓ Created company: {duns} - {company.primary_name}")
    else:
        # Update basic info
        company.primary_name = org_data.get('primaryName', company.primary_name)
        company.country_iso_alpha2_code = org_data.get('countryISOAlpha2Code', company.country_iso_alpha2_code)
        company.updated_at = datetime.utcnow()
        print(f"  ✓ Found existing company: {duns} - {company.primary_name}")
    
    return company


def _load_company_info(session, data: Dict):
    """Load company info data."""
    org = data.get('organization', {})
    company = _get_or_create_company(session, org)
    
    # Check if company_info exists
    if not company.company_info:
        company_info = CompanyInfo(company_id=company.id)
        session.add(company_info)
    else:
        company_info = company.company_info
    
    # Update fields
    company_info.is_fortune_1000_listed = org.get('isFortune1000Listed')
    company_info.is_forbes_listed = org.get('isForbesLargestPrivateCompaniesListed')
    company_info.is_standalone = org.get('isStandalone')
    company_info.is_small_business = org.get('isSmallBusiness')
    
    # Parse dates
    inc_date_str = org.get('incorporatedDate')
    if inc_date_str:
        company_info.incorporated_date = _parse_date(inc_date_str)
    
    company_info.fiscal_year_end = org.get('fiscalYearEnd')
    
    print(f"  ✓ Updated company info")


def _load_company_financials(session, data: Dict):
    """Load financial data with full details."""
    org = data.get('organization', {})
    company = _get_or_create_company(session, org)
    
    # Delete existing financial statements (Option A: Delete & Replace)
    # Must delete children first (bulk delete doesn't trigger cascades)
    stmt_ids_subq = session.query(FinancialStatement.id).filter_by(company_id=company.id)
    session.query(BalanceSheetItem).filter(BalanceSheetItem.statement_id.in_(stmt_ids_subq)).delete(synchronize_session=False)
    session.query(ProfitLossItem).filter(ProfitLossItem.statement_id.in_(stmt_ids_subq)).delete(synchronize_session=False)
    session.query(CashFlowItem).filter(CashFlowItem.statement_id.in_(stmt_ids_subq)).delete(synchronize_session=False)
    session.query(FinancialRatio).filter(FinancialRatio.statement_id.in_(stmt_ids_subq)).delete(synchronize_session=False)
    session.query(FinancialOverview).filter(FinancialOverview.statement_id.in_(stmt_ids_subq)).delete(synchronize_session=False)
    session.query(FinancialStatement).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.flush()  # Ensure deletes are executed before adding new records
    
    # Load latest fiscal financials
    latest_fiscal = org.get('latestFiscalFinancials')
    if latest_fiscal:
        _load_single_financial_statement(session, company, latest_fiscal, 'fiscal_latest')
        print(f"  ✓ Added latest fiscal financial statement")
    
    # Load other financials
    other_financials = org.get('otherFinancials', [])
    for fin in other_financials:
        _load_single_financial_statement(session, company, fin, 'other')
    
    if other_financials:
        print(f"  ✓ Added {len(other_financials)} other financial statements")


def _load_single_financial_statement(session, company: Company, fin_data: Dict, stmt_type: str):
    """Load a single financial statement with all its details."""
    
    # Create main financial statement record
    stmt = FinancialStatement(
        company_id=company.id,
        statement_type=stmt_type,
        financial_statement_to_date=_parse_date(fin_data.get('financialStatementToDate')),
        financial_statement_from_date=_parse_date(fin_data.get('financialStatementFromDate')),
        financial_statement_duration=fin_data.get('financialStatementDuration'),
        filing_date=_parse_date(fin_data.get('filingDate')),
        received_timestamp=_parse_date(fin_data.get('receivedTimestamp')),
        approval_date=_parse_date(fin_data.get('approvalDate')),
        currency=fin_data.get('currency'),
        units=fin_data.get('units'),
        
        # Data provider
        data_provider_description=_get_nested(fin_data, 'dataProvider', 'description'),
        data_provider_dnb_code=_get_nested(fin_data, 'dataProvider', 'dnbCode'),
        
        # Statement template
        statement_template_description=_get_nested(fin_data, 'statementTemplate', 'description'),
        statement_template_dnb_code=_get_nested(fin_data, 'statementTemplate', 'dnbCode'),
        
        # Scope and reliability
        information_scope_description=_get_nested(fin_data, 'informationScope', 'description'),
        information_scope_dnb_code=_get_nested(fin_data, 'informationScope', 'dnbCode'),
        reliability_description=_get_nested(fin_data, 'reliability', 'description'),
        reliability_dnb_code=_get_nested(fin_data, 'reliability', 'dnbCode'),
        
        # Boolean flags
        is_fiscal=fin_data.get('isFiscal'),
        is_interim=fin_data.get('isInterim'),
        is_audited=fin_data.get('isAudited'),
        is_audit_unknown=fin_data.get('isAuditUnknown'),
        is_final=fin_data.get('isFinal'),
        is_opening=fin_data.get('isOpening'),
        is_proforma=fin_data.get('isProforma'),
        is_signed=fin_data.get('isSigned'),
        is_qualified=fin_data.get('isQualified'),
        is_restated=fin_data.get('isRestated'),
        is_trial_balance=fin_data.get('isTrialBalance'),
        is_unbalanced=fin_data.get('isUnbalanced'),
        
        # Auditor info
        accountant_name=fin_data.get('accountantName'),
        not_audited_reason=fin_data.get('notAuditedReason')
    )
    session.add(stmt)
    session.flush()  # Get statement ID
    
    # Load overview section
    overview_data = fin_data.get('overview')
    if overview_data:
        overview = FinancialOverview(
            statement_id=stmt.id,
            
            # Assets - Current
            cash_and_liquid_assets=overview_data.get('cashAndLiquidAssets'),
            marketable_securities=overview_data.get('marketableSecurities'),
            accounts_receivable=overview_data.get('accountsReceivable'),
            due_from_group_short_term=overview_data.get('dueFromGroupShortTerm'),
            other_receivables=overview_data.get('otherReceivables'),
            total_receivables=overview_data.get('totalReceivables'),
            inventory=overview_data.get('inventory'),
            prepaid_deferred_short_term=overview_data.get('prepaidDeferredShortTerm'),
            other_current_assets=overview_data.get('otherCurrentAssets'),
            total_current_assets=overview_data.get('totalCurrentAssets'),
            
            # Assets - Long Term
            tangible_fixed_assets=overview_data.get('tangibleFixedAssets'),
            due_from_group_long_term=overview_data.get('dueFromGroupLongTerm'),
            investments_long_term=overview_data.get('investmentsLongTerm'),
            intangible_assets=overview_data.get('intangibleAssets'),
            other_long_term_assets=overview_data.get('otherLongTermAssets'),
            total_long_term_assets=overview_data.get('totalLongTermAssets'),
            other_unclassified_assets=overview_data.get('otherUnclassifiedAssets'),
            total_assets=overview_data.get('totalAssets'),
            
            # Liabilities - Current
            accounts_payable=overview_data.get('accountsPayable'),
            accruals_other_payables=overview_data.get('accrualsOtherPayables'),
            short_term_debt=overview_data.get('shortTermDebt'),
            due_to_group_short_term=overview_data.get('dueToGroupShortTerm'),
            taxes_short_term=overview_data.get('taxesShortTerm'),
            other_current_liabilities=overview_data.get('otherCurrentLiabilities'),
            total_current_liabilities=overview_data.get('totalCurrentLiabilities'),
            
            # Liabilities - Long Term
            long_term_debt=overview_data.get('longTermDebt'),
            due_to_group_long_term=overview_data.get('dueToGroupLongTerm'),
            deferred_credit_income=overview_data.get('deferredCreditIncome'),
            deferred_taxes_long_term=overview_data.get('deferredTaxesLongTerm'),
            other_long_term_liabilities=overview_data.get('otherLongTermLiabilities'),
            total_long_term_liabilities=overview_data.get('totalLongTermLiabilities'),
            provisions=overview_data.get('provisions'),
            other_unclassified_liabilities=overview_data.get('otherUnclassifiedLiabilities'),
            total_liabilities=overview_data.get('totalLiabilities'),
            
            # Equity
            capital_stock=overview_data.get('capitalStock'),
            capital_surplus=overview_data.get('capitalSurplus'),
            retained_earnings=overview_data.get('retainedEarnings'),
            capital_reserves=overview_data.get('capitalReserves'),
            other_unrestricted_reserves=overview_data.get('otherUnrestrictedReserves'),
            restricted_equity=overview_data.get('restrictedEquity'),
            other_equity=overview_data.get('otherEquity'),
            minority_interest=overview_data.get('minorityInterest'),
            net_worth=overview_data.get('netWorth'),
            total_liabilities_equity=overview_data.get('totalLiabilitiesEquity'),
            
            # Income Statement
            sales_revenue=overview_data.get('salesRevenue'),
            cost_of_sales=overview_data.get('costOfSales'),
            gross_profit=overview_data.get('grossProfit'),
            operating_profit=overview_data.get('operatingProfit'),
            profit_before_taxes=overview_data.get('profitBeforeTaxes'),
            profit_after_tax=overview_data.get('profitAfterTax'),
            dividends=overview_data.get('dividends'),
            
            # Calculated Metrics
            total_indebtedness=overview_data.get('totalIndebtedness'),
            working_capital=overview_data.get('workingCapital'),
            net_current_assets=overview_data.get('netCurrentAssets'),
            tangible_net_worth=overview_data.get('tangibleNetWorth'),
            
            # Financial Ratios
            current_ratio=overview_data.get('currentRatio'),
            quick_ratio=overview_data.get('quickRatio'),
            current_liabilities_over_net_worth=overview_data.get('currentLiabilitiesOverNetWorth'),
            total_liabilities_over_net_worth=overview_data.get('totalLiabilitiesOverNetWorth')
        )
        session.add(overview)
    
    # Load balance sheet items
    balance_sheet = fin_data.get('balanceSheet', {})
    _load_balance_sheet_items(session, stmt.id, balance_sheet)
    
    # Load profit & loss items
    profit_loss = fin_data.get('profitAndLossStatement', {})
    _load_profit_loss_items(session, stmt.id, profit_loss)
    
    # Load cash flow items
    cash_flow = fin_data.get('cashFlowStatement', {})
    if cash_flow:
        _load_cash_flow_items(session, stmt.id, cash_flow)
    
    # Load financial ratios
    ratios = fin_data.get('financialRatios', {})
    if ratios:
        _load_financial_ratios(session, stmt.id, ratios)


def _load_balance_sheet_items(session, statement_id: int, balance_sheet: Dict):
    """Load balance sheet line items."""
    
    # Assets items
    assets = balance_sheet.get('assets', {})
    asset_items = assets.get('statementItems', [])
    for item in asset_items:
        bs_item = BalanceSheetItem(
            statement_id=statement_id,
            section='assets',
            item_description=_get_nested(item, 'itemKey', 'description'),
            item_dnb_code=_get_nested(item, 'itemKey', 'dnbCode'),
            value=item.get('value'),
            priority=item.get('priority'),
            item_group_level=item.get('itemGroupLevel')
        )
        session.add(bs_item)
    
    # Liabilities items
    liabilities = balance_sheet.get('liabilities', {})
    liab_items = liabilities.get('statementItems', [])
    for item in liab_items:
        bs_item = BalanceSheetItem(
            statement_id=statement_id,
            section='liabilities',
            item_description=_get_nested(item, 'itemKey', 'description'),
            item_dnb_code=_get_nested(item, 'itemKey', 'dnbCode'),
            value=item.get('value'),
            priority=item.get('priority'),
            item_group_level=item.get('itemGroupLevel')
        )
        session.add(bs_item)
    
    # Top-level balance sheet items (if any)
    top_items = balance_sheet.get('statementItems', [])
    for item in top_items:
        bs_item = BalanceSheetItem(
            statement_id=statement_id,
            section='other',
            item_description=_get_nested(item, 'itemKey', 'description'),
            item_dnb_code=_get_nested(item, 'itemKey', 'dnbCode'),
            value=item.get('value'),
            priority=item.get('priority'),
            item_group_level=item.get('itemGroupLevel')
        )
        session.add(bs_item)


def _load_profit_loss_items(session, statement_id: int, profit_loss: Dict):
    """Load profit & loss line items."""
    items = profit_loss.get('statementItems', [])
    
    for item in items:
        pl_item = ProfitLossItem(
            statement_id=statement_id,
            item_description=_get_nested(item, 'itemKey', 'description'),
            item_dnb_code=_get_nested(item, 'itemKey', 'dnbCode'),
            value=item.get('value'),
            priority=item.get('priority'),
            item_group_level=item.get('itemGroupLevel')
        )
        session.add(pl_item)


def _load_cash_flow_items(session, statement_id: int, cash_flow: Dict):
    """Load cash flow line items."""
    items = cash_flow.get('statementItems', [])
    
    for item in items:
        cf_item = CashFlowItem(
            statement_id=statement_id,
            item_description=_get_nested(item, 'itemKey', 'description'),
            item_dnb_code=_get_nested(item, 'itemKey', 'dnbCode'),
            value=item.get('value'),
            priority=item.get('priority'),
            item_group_level=item.get('itemGroupLevel')
        )
        session.add(cf_item)


def _load_financial_ratios(session, statement_id: int, ratios: Dict):
    """Load financial ratios."""
    items = ratios.get('statementItems', [])
    
    for item in items:
        ratio = FinancialRatio(
            statement_id=statement_id,
            ratio_description=_get_nested(item, 'itemKey', 'description'),
            ratio_dnb_code=_get_nested(item, 'itemKey', 'dnbCode'),
            value=item.get('value'),
            relative_industry_rank=item.get('relativeIndustryRank'),
            priority=item.get('priority'),
            item_group_level=item.get('itemGroupLevel')
        )
        session.add(ratio)


def _load_events_filings(session, data: Dict):
    """Load events and filings data."""
    org = data.get('organization', {})
    company = _get_or_create_company(session, org)
    
    # Load legal events
    legal_events = org.get('legalEvents', {})
    if legal_events:
        _load_legal_events(session, company, legal_events)
    
    # Load awards
    awards = org.get('awards', {})
    if awards:
        _load_awards(session, company, awards)
    
    # Load exclusions
    exclusions = org.get('exclusions', {})
    if exclusions:
        _load_exclusions(session, company, exclusions)
    
    # Load significant events
    significant_events = org.get('significantEvents', {})
    if significant_events:
        _load_significant_events(session, company, significant_events)


def _load_legal_events(session, company: Company, legal_events: Dict):
    """Load legal events data."""
    # Delete existing legal events data (Option A: Delete & Replace)
    # Must delete children first, then parents (bulk delete doesn't trigger cascades)
    session.query(LienFiling).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.query(JudgmentFiling).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.query(SuitFiling).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.query(BankruptcyFiling).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.query(ClaimFiling).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.query(Lien).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.query(Judgment).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.query(Suit).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.query(Bankruptcy).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.query(Claim).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.flush()  # Ensure deletes are executed before adding new records
    
    # Create or update summary
    if not company.legal_events_summary:
        summary = LegalEventsSummary(company_id=company.id)
        session.add(summary)
    else:
        summary = company.legal_events_summary
    
    # Update summary flags
    summary.has_legal_events = legal_events.get('hasLegalEvents')
    summary.has_liens = legal_events.get('hasLiens')
    summary.has_judgments = legal_events.get('hasJudgments')
    summary.has_suits = legal_events.get('hasSuits')
    summary.has_bankruptcy = legal_events.get('hasBankruptcy')
    summary.has_claims = legal_events.get('hasClaims')
    
    # Load liens
    liens_data = legal_events.get('liens', {})
    if isinstance(liens_data, dict) and 'filings' in liens_data:
        lien = Lien(
            company_id=company.id,
            most_recent_filing_date=_parse_date(liens_data.get('mostRecentFilingDate')),
            open_count=liens_data.get('openCount'),
            open_amount_value=_get_amount_value(liens_data.get('openAmount')),
            open_amount_currency=_get_amount_currency(liens_data.get('openAmount')),
            period_summary_json=liens_data.get('periodSummary')
        )
        session.add(lien)
        session.flush()
        
        # Load lien filings
        for filing_data in liens_data.get('filings', []):
            filing = LienFiling(
                lien_id=lien.id,
                company_id=company.id,
                is_stop_d=filing_data.get('isStopD'),
                filing_type_description=_get_nested(filing_data, 'filingType', 'description'),
                filing_type_dnb_code=_get_nested(filing_data, 'filingType', 'dnbCode'),
                filing_date=_parse_date(filing_data.get('filingDate')),
                filing_amount_value=_get_amount_value(filing_data.get('filingAmount')),
                filing_amount_currency=_get_amount_currency(filing_data.get('filingAmount')),
                status_description=_get_nested(filing_data, 'status', 'description'),
                status_date=_parse_date(filing_data.get('statusDate'))
            )
            session.add(filing)
            session.flush()
            
            # Load role players
            for rp_data in filing_data.get('rolePlayers', []):
                role_player = LienFilingRolePlayer(
                    lien_filing_id=filing.id,
                    role_player_type_desc=_get_nested(rp_data, 'rolePlayerType', 'description'),
                    role_player_type_dnb_code=_get_nested(rp_data, 'rolePlayerType', 'dnbCode'),
                    name=rp_data.get('name'),
                    duns=rp_data.get('duns'),
                    address_line1=_get_nested(rp_data, 'address', 'streetAddress', 'line1'),
                    city=_get_nested(rp_data, 'address', 'addressLocality', 'name'),
                    region_name=_get_nested(rp_data, 'address', 'addressRegion', 'name'),
                    postal_code=_get_nested(rp_data, 'address', 'postalCode'),
                    country_iso_alpha2_code=_get_nested(rp_data, 'address', 'addressCountry', 'isoAlpha2Code')
                )
                session.add(role_player)
        
        print(f"  ✓ Loaded {len(liens_data.get('filings', []))} lien filings")
    
    # Load judgments (similar structure)
    judgments_data = legal_events.get('judgments', {})
    if isinstance(judgments_data, dict) and 'filings' in judgments_data:
        judgment = Judgment(
            company_id=company.id,
            most_recent_filing_date=_parse_date(judgments_data.get('mostRecentFilingDate')),
            open_count=judgments_data.get('openCount'),
            open_amount_value=_get_amount_value(judgments_data.get('openAmount')),
            open_amount_currency=_get_amount_currency(judgments_data.get('openAmount')),
            period_summary_json=judgments_data.get('periodSummary')
        )
        session.add(judgment)
        session.flush()
        
        for filing_data in judgments_data.get('filings', []):
            filing = JudgmentFiling(
                judgment_id=judgment.id,
                company_id=company.id,
                is_stop_d=filing_data.get('isStopD'),
                filing_type_description=_get_nested(filing_data, 'filingType', 'description'),
                filing_type_dnb_code=_get_nested(filing_data, 'filingType', 'dnbCode'),
                filing_date=_parse_date(filing_data.get('filingDate')),
                filing_amount_value=_get_amount_value(filing_data.get('filingAmount')),
                filing_amount_currency=_get_amount_currency(filing_data.get('filingAmount')),
                status_description=_get_nested(filing_data, 'status', 'description'),
                status_date=_parse_date(filing_data.get('statusDate'))
            )
            session.add(filing)
            session.flush()
            
            for rp_data in filing_data.get('rolePlayers', []):
                role_player = JudgmentFilingRolePlayer(
                    judgment_filing_id=filing.id,
                    role_player_type_desc=_get_nested(rp_data, 'rolePlayerType', 'description'),
                    role_player_type_dnb_code=_get_nested(rp_data, 'rolePlayerType', 'dnbCode'),
                    name=rp_data.get('name'),
                    duns=rp_data.get('duns'),
                    address_line1=_get_nested(rp_data, 'address', 'streetAddress', 'line1'),
                    city=_get_nested(rp_data, 'address', 'addressLocality', 'name'),
                    region_name=_get_nested(rp_data, 'address', 'addressRegion', 'name'),
                    postal_code=_get_nested(rp_data, 'address', 'postalCode'),
                    country_iso_alpha2_code=_get_nested(rp_data, 'address', 'addressCountry', 'isoAlpha2Code')
                )
                session.add(role_player)
        
        print(f"  ✓ Loaded {len(judgments_data.get('filings', []))} judgment filings")
    
    # Load suits (similar structure)
    suits_data = legal_events.get('suits', {})
    if isinstance(suits_data, dict) and 'filings' in suits_data:
        suit = Suit(
            company_id=company.id,
            most_recent_filing_date=_parse_date(suits_data.get('mostRecentFilingDate')),
            open_count=suits_data.get('openCount'),
            open_amount_value=_get_amount_value(suits_data.get('openAmount')),
            open_amount_currency=_get_amount_currency(suits_data.get('openAmount')),
            period_summary_json=suits_data.get('periodSummary')
        )
        session.add(suit)
        session.flush()
        
        for filing_data in suits_data.get('filings', []):
            filing = SuitFiling(
                suit_id=suit.id,
                company_id=company.id,
                is_stop_d=filing_data.get('isStopD'),
                filing_type_description=_get_nested(filing_data, 'filingType', 'description'),
                filing_type_dnb_code=_get_nested(filing_data, 'filingType', 'dnbCode'),
                filing_date=_parse_date(filing_data.get('filingDate')),
                filing_amount_value=_get_amount_value(filing_data.get('filingAmount')),
                filing_amount_currency=_get_amount_currency(filing_data.get('filingAmount')),
                status_description=_get_nested(filing_data, 'status', 'description'),
                status_date=_parse_date(filing_data.get('statusDate'))
            )
            session.add(filing)
            session.flush()
            
            for rp_data in filing_data.get('rolePlayers', []):
                role_player = SuitFilingRolePlayer(
                    suit_filing_id=filing.id,
                    role_player_type_desc=_get_nested(rp_data, 'rolePlayerType', 'description'),
                    role_player_type_dnb_code=_get_nested(rp_data, 'rolePlayerType', 'dnbCode'),
                    name=rp_data.get('name'),
                    duns=rp_data.get('duns'),
                    address_line1=_get_nested(rp_data, 'address', 'streetAddress', 'line1'),
                    city=_get_nested(rp_data, 'address', 'addressLocality', 'name'),
                    region_name=_get_nested(rp_data, 'address', 'addressRegion', 'name'),
                    postal_code=_get_nested(rp_data, 'address', 'postalCode'),
                    country_iso_alpha2_code=_get_nested(rp_data, 'address', 'addressCountry', 'isoAlpha2Code')
                )
                session.add(role_player)
        
        print(f"  ✓ Loaded {len(suits_data.get('filings', []))} suit filings")
    
    # Load bankruptcy
    bankruptcy_data = legal_events.get('bankruptcy', {})
    if isinstance(bankruptcy_data, dict) and 'filings' in bankruptcy_data:
        bankruptcy = Bankruptcy(
            company_id=company.id,
            most_recent_filing_date=_parse_date(bankruptcy_data.get('mostRecentFilingDate')),
            period_summary_json=bankruptcy_data.get('periodSummary')
        )
        session.add(bankruptcy)
        session.flush()
        
        for filing_data in bankruptcy_data.get('filings', []):
            filing = BankruptcyFiling(
                bankruptcy_id=bankruptcy.id,
                company_id=company.id,
                is_stop_d=filing_data.get('isStopD'),
                filing_type_description=_get_nested(filing_data, 'filingType', 'description'),
                filing_type_dnb_code=_get_nested(filing_data, 'filingType', 'dnbCode'),
                filing_date=_parse_date(filing_data.get('filingDate')),
                filing_amount_value=_get_amount_value(filing_data.get('filingAmount')),
                filing_amount_currency=_get_amount_currency(filing_data.get('filingAmount')),
                status_description=_get_nested(filing_data, 'status', 'description'),
                status_date=_parse_date(filing_data.get('statusDate'))
            )
            session.add(filing)
            session.flush()
            
            for rp_data in filing_data.get('rolePlayers', []):
                role_player = BankruptcyFilingRolePlayer(
                    bankruptcy_filing_id=filing.id,
                    role_player_type_desc=_get_nested(rp_data, 'rolePlayerType', 'description'),
                    role_player_type_dnb_code=_get_nested(rp_data, 'rolePlayerType', 'dnbCode'),
                    name=rp_data.get('name'),
                    duns=rp_data.get('duns'),
                    address_line1=_get_nested(rp_data, 'address', 'streetAddress', 'line1'),
                    city=_get_nested(rp_data, 'address', 'addressLocality', 'name'),
                    region_name=_get_nested(rp_data, 'address', 'addressRegion', 'name'),
                    postal_code=_get_nested(rp_data, 'address', 'postalCode'),
                    country_iso_alpha2_code=_get_nested(rp_data, 'address', 'addressCountry', 'isoAlpha2Code')
                )
                session.add(role_player)
        
        print(f"  ✓ Loaded {len(bankruptcy_data.get('filings', []))} bankruptcy filings")
    
    # Load claims
    claims_data = legal_events.get('claims', {})
    if isinstance(claims_data, dict) and 'filings' in claims_data:
        claim = Claim(
            company_id=company.id,
            open_count=claims_data.get('openCount'),
            open_amount_value=_get_amount_value(claims_data.get('openAmount')),
            open_amount_currency=_get_amount_currency(claims_data.get('openAmount'))
        )
        session.add(claim)
        session.flush()
        
        for filing_data in claims_data.get('filings', []):
            filing = ClaimFiling(
                claim_id=claim.id,
                company_id=company.id,
                is_stop_d=filing_data.get('isStopD'),
                filing_type_description=_get_nested(filing_data, 'filingType', 'description'),
                filing_type_dnb_code=_get_nested(filing_data, 'filingType', 'dnbCode'),
                filing_date=_parse_date(filing_data.get('filingDate')),
                filing_amount_value=_get_amount_value(filing_data.get('filingAmount')),
                filing_amount_currency=_get_amount_currency(filing_data.get('filingAmount')),
                status_description=_get_nested(filing_data, 'status', 'description'),
                status_date=_parse_date(filing_data.get('statusDate'))
            )
            session.add(filing)
            session.flush()
            
            for rp_data in filing_data.get('rolePlayers', []):
                role_player = ClaimFilingRolePlayer(
                    claim_filing_id=filing.id,
                    role_player_type_desc=_get_nested(rp_data, 'rolePlayerType', 'description'),
                    role_player_type_dnb_code=_get_nested(rp_data, 'rolePlayerType', 'dnbCode'),
                    name=rp_data.get('name'),
                    duns=rp_data.get('duns'),
                    address_line1=_get_nested(rp_data, 'address', 'streetAddress', 'line1'),
                    city=_get_nested(rp_data, 'address', 'addressLocality', 'name'),
                    region_name=_get_nested(rp_data, 'address', 'addressRegion', 'name'),
                    postal_code=_get_nested(rp_data, 'address', 'postalCode'),
                    country_iso_alpha2_code=_get_nested(rp_data, 'address', 'addressCountry', 'isoAlpha2Code')
                )
                session.add(role_player)
        
        print(f"  ✓ Loaded {len(claims_data.get('filings', []))} claim filings")


def _load_awards(session, company: Company, awards: Dict):
    """Load awards data."""
    # Delete existing contracts data (Option A: Delete & Replace)
    # Must delete children first (bulk delete doesn't trigger cascades)
    session.query(ContractAction).filter(ContractAction.contract_id.in_(
        session.query(Contract.id).filter_by(company_id=company.id)
    )).delete(synchronize_session=False)
    session.query(ContractCharacteristic).filter(ContractCharacteristic.contract_id.in_(
        session.query(Contract.id).filter_by(company_id=company.id)
    )).delete(synchronize_session=False)
    session.query(Contract).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.flush()  # Ensure deletes are executed before adding new records
    
    # Create or update summary
    if not company.awards_summary:
        summary = AwardsSummary(company_id=company.id)
        session.add(summary)
    else:
        summary = company.awards_summary
    
    # Update summary flags
    summary.has_contracts = awards.get('hasContracts')
    summary.has_loans = awards.get('hasLoans')
    summary.has_grants = awards.get('hasGrants')
    summary.has_debts = awards.get('hasDebts')
    summary.has_open_contracts = awards.get('hasOpenContracts')
    summary.has_open_loans = awards.get('hasOpenLoans')
    summary.has_open_grants = awards.get('hasOpenGrants')
    summary.has_open_debts = awards.get('hasOpenDebts')
    
    # Update summary amounts with currency
    summary.obligated_contracts_amt_val = _get_amount_value(awards.get('obligatedContractsAmount'))
    summary.obligated_contracts_amt_curr = _get_amount_currency(awards.get('obligatedContractsAmount'))
    summary.current_contracts_amt_val = _get_amount_value(awards.get('currentContractsAmount'))
    summary.current_contracts_amt_curr = _get_amount_currency(awards.get('currentContractsAmount'))
    summary.total_open_contracts_amt_val = _get_amount_value(awards.get('totalOpenContractsAmount'))
    summary.total_contracts_amt_val = _get_amount_value(awards.get('totalContractsAmount'))
    
    # Update summary counts and dates
    summary.total_open_contracts_count = awards.get('totalOpenContractsCount')
    summary.most_recent_contract_date = _parse_date(awards.get('mostRecentContractDate'))
    summary.most_recent_loan_date = _parse_date(awards.get('mostRecentLoanDate'))
    summary.most_recent_grant_date = _parse_date(awards.get('mostRecentGrantDate'))
    summary.most_recent_debt_date = _parse_date(awards.get('mostRecentDebtDate'))
    
    # Load contracts
    contracts_data = awards.get('contracts', [])
    for contract_data in contracts_data:
        contract = Contract(
            company_id=company.id,
            award_id=contract_data.get('awardID'),
            award_description=contract_data.get('awardDescription'),
            contract_id=contract_data.get('contractID'),
            contract_type_code=_get_nested(contract_data, 'contractType', 'code'),
            contract_type_description=_get_nested(contract_data, 'contractType', 'description'),
            base_all_options_amt_value=_get_amount_value(contract_data.get('baseAndAllOptionsAmount')),
            base_all_options_amt_currency=_get_amount_currency(contract_data.get('baseAndAllOptionsAmount')),
            current_total_amt_value=_get_amount_value(contract_data.get('currentTotalAmount')),
            current_total_amt_currency=_get_amount_currency(contract_data.get('currentTotalAmount')),
            funding_agency_code=_get_nested(contract_data, 'fundingAgency', 'code'),
            funding_agency_description=_get_nested(contract_data, 'fundingAgency', 'description')
        )
        session.add(contract)
        session.flush()
        
        # Load actions
        for action_data in contract_data.get('actions', []):
            action = ContractAction(
                contract_id=contract.id,
                action_date=_parse_date(action_data.get('actionDate')),
                action_fiscal_year=action_data.get('actionFiscalYear'),
                federal_funding_amt_value=_get_amount_value(action_data.get('federalFundingAmount')),
                federal_funding_amt_currency=_get_amount_currency(action_data.get('federalFundingAmount'))
            )
            session.add(action)
        
        # Load characteristics
        for char_data in contract_data.get('characteristics', []):
            char = ContractCharacteristic(
                contract_id=contract.id,
                description=char_data.get('description'),
                dnb_code=char_data.get('dnbCode')
            )
            session.add(char)
    
    if contracts_data:
        print(f"  ✓ Loaded {len(contracts_data)} contracts")


def _load_exclusions(session, company: Company, exclusions: Dict):
    """Load exclusions data."""
    if not exclusions:
        return
    
    # Delete existing exclusions data (Option A: Delete & Replace)
    session.query(ActiveExclusion).filter_by(company_id=company.id).delete()
    session.flush()  # Ensure deletes are executed before adding new records
    
    # Create or update summary
    if not company.exclusions_summary:
        summary = ExclusionsSummary(company_id=company.id)
        session.add(summary)
    else:
        summary = company.exclusions_summary
    
    summary.has_active_exclusions = exclusions.get('hasActiveExclusions')
    summary.has_inactive_exclusions = exclusions.get('hasInactiveExclusions')
    summary.active_exclusions_count = exclusions.get('activeExclusionsCount')
    summary.inactive_exclusions_count = exclusions.get('inactiveExclusionsCount')
    
    # Load active exclusions
    for excl_data in exclusions.get('activeExclusions', []):
        excl = ActiveExclusion(
            company_id=company.id,
            sam_record_number=excl_data.get('samRecordNumber'),
            cage_code=excl_data.get('cageCode'),
            classification_type_desc=_get_nested(excl_data, 'classificationType', 'description'),
            agency_name=excl_data.get('agencyName'),
            effective_date=_parse_date(excl_data.get('effectiveDate')),
            expiration_date=_parse_date(excl_data.get('expirationDate'))
        )
        session.add(excl)
    
    print(f"  ✓ Loaded exclusions")


def _load_significant_events(session, company: Company, significant_events: Dict):
    """Load significant events data."""
    if not significant_events:
        return
    
    # Delete existing significant events data (Option A: Delete & Replace)
    session.query(SignificantEventTextEntry).filter(SignificantEventTextEntry.significant_event_id.in_(
        session.query(SignificantEvent.id).filter_by(company_id=company.id)
    )).delete(synchronize_session=False)
    session.query(SignificantEvent).filter_by(company_id=company.id).delete(synchronize_session=False)
    session.flush()
    
    # Create or update summary
    if not company.significant_events_summary:
        summary = SignificantEventsSummary(company_id=company.id)
        session.add(summary)
    else:
        summary = company.significant_events_summary
    
    summary.has_significant_events = significant_events.get('hasSignificantEvents')
    summary.has_operational_events = significant_events.get('hasOperationalEvents')
    summary.has_disastrous_events = significant_events.get('hasDisastrousEvents')
    summary.has_burglary_occured = significant_events.get('hasBurglaryOccured')
    summary.has_fire_occurred = significant_events.get('hasFireOccurred')
    summary.has_business_discontinued = significant_events.get('hasBusinessDiscontinued')
    summary.has_name_change = significant_events.get('hasNameChange')
    summary.has_partner_change = significant_events.get('hasPartnerChange')
    summary.has_ceo_change = significant_events.get('hasCEOChange')
    summary.has_control_change = significant_events.get('hasControlChange')
    
    # Load individual events
    events_count = 0
    for event_data in significant_events.get('events', []):
        event = SignificantEvent(
            company_id=company.id,
            event_date=_parse_date(event_data.get('eventDate')),
            event_type_description=_get_nested(event_data, 'eventType', 'description'),
            event_type_dnb_code=_get_nested(event_data, 'eventType', 'dnbCode'),
            start_date=_parse_date(event_data.get('startDate')),
            impact_details=event_data.get('impactDetails'),
            impact_amount_value=_get_amount_value(event_data.get('impactAmount')),
            impact_amount_currency=_get_amount_currency(event_data.get('impactAmount')),
            impacted_premises_type=event_data.get('impactedPremisesType'),
            damaged_assets_class=event_data.get('damagedAssetsClass'),
            impacted_children=event_data.get('impactedChildren'),
            insurance_claim_settlement_amount_value=_get_amount_value(event_data.get('insuranceClaimSettlementAmount')),
            insurance_claim_settlement_amount_currency=_get_amount_currency(event_data.get('insuranceClaimSettlementAmount')),
            data_provider_description=_get_nested(event_data, 'dataProvider', 'description'),
            data_provider_dnb_code=_get_nested(event_data, 'dataProvider', 'dnbCode')
        )
        session.add(event)
        session.flush()
        
        # Load text entries
        for text_data in event_data.get('textEntry', []):
            text_entry = SignificantEventTextEntry(
                significant_event_id=event.id,
                text=text_data.get('text'),
                priority=text_data.get('priority'),
                type_description=text_data.get('typeDescription'),
                type_dnb_code=text_data.get('typeDnBCode')
            )
            session.add(text_entry)
        
        events_count += 1
    
    if events_count > 0:
        print(f"  ✓ Loaded {events_count} significant events")


# Helper functions
def _parse_date(date_str: str) -> date:
    """Parse date string to date object."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        try:
            return datetime.strptime(date_str, '%Y-%m').date()
        except:
            return None


def _get_amount_value(amount_dict: Dict) -> Decimal:
    """Extract value from amount dictionary."""
    if not amount_dict or not isinstance(amount_dict, dict):
        return None
    value = amount_dict.get('value')
    return Decimal(str(value)) if value is not None else None


def _get_amount_currency(amount_dict: Dict) -> str:
    """Extract currency from amount dictionary."""
    if not amount_dict or not isinstance(amount_dict, dict):
        return None
    return amount_dict.get('currency')


def _get_nested(data: Dict, *keys):
    """Safely get nested dictionary values."""
    for key in keys:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
        if data is None:
            return None
    return data
