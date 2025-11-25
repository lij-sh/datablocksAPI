"""
Parse PDF content to extract complete schema for v2.0 implementation
"""
import json
import re
from pathlib import Path

def extract_field_info(text, start_pattern, end_pattern=None):
    """
    Extract field information from PDF text between patterns
    """
    fields = {}
    lines = text.split('\n')
    
    current_field = None
    current_type = None
    current_desc = []
    
    for line in lines:
        # Match field definition lines like: organization.violations.hasEPAViolations [boolean] e.g.: true
        field_match = re.match(r'^(organization\.[^\[]+)\s*\[([^\]]+)\]', line)
        if field_match:
            # Save previous field if exists
            if current_field:
                fields[current_field] = {
                    'type': current_type,
                    'description': ' '.join(current_desc).strip()
                }
            
            current_field = field_match.group(1)
            current_type = field_match.group(2).strip()
            current_desc = []
            continue
        
        # Collect description lines
        if current_field and line.strip() and not line.startswith('====='):
            # Skip if it looks like a new section or field
            if not line.startswith('organization.'):
                current_desc.append(line.strip())
    
    # Save last field
    if current_field:
        fields[current_field] = {
            'type': current_type,
            'description': ' '.join(current_desc).strip()
        }
    
    return fields

def analyze_violations(pdf_text):
    """Extract all violation fields"""
    print("\n=== ANALYZING VIOLATIONS ===")
    
    # Find violations section
    violations_match = re.search(
        r'organization\.violations\s*\[object\](.*?)(?=\n===== PAGE \d+ =====.*?organization\.\w+\s*\[object\])',
        pdf_text,
        re.DOTALL
    )
    
    if violations_match:
        violations_text = violations_match.group(0)
        fields = extract_field_info(violations_text, 'organization.violations')
        
        print(f"Found {len(fields)} violation fields:")
        for field_name, info in sorted(fields.items()):
            print(f"  - {field_name.replace('organization.violations.', '')}: {info['type']}")
        
        return fields
    return {}

def analyze_financing_events(pdf_text):
    """Extract all financing event fields (UCC filings)"""
    print("\n=== ANALYZING FINANCING EVENTS (UCC) ===")
    
    # Find financing events section - use simpler pattern
    financing_match = re.search(
        r'organization\.financingEvents\.financingStatementFilings\.filings\s*\[array \(object\)\](.*?)organization\.financingEvents\.letterOfLiabilityFilings',
        pdf_text,
        re.DOTALL
    )
    
    if financing_match:
        financing_text = financing_match.group(0)
        fields = extract_field_info(financing_text, 'organization.financingEvents')
        
        print(f"Found {len(fields)} financing event fields:")
        # Group by category
        categories = {}
        for field_name, info in sorted(fields.items()):
            parts = field_name.replace('organization.financingEvents.financingStatementFilings.filings.', '').split('.')
            category = parts[0] if parts else 'root'
            if category not in categories:
                categories[category] = []
            categories[category].append((field_name, info))
        
        for category, fields_list in sorted(categories.items()):
            print(f"\n  {category.upper()}: ({len(fields_list)} fields)")
            for field_name, info in fields_list[:5]:  # Show first 5
                short_name = field_name.split('.')[-1]
                print(f"    - {short_name}: {info['type']}")
        
        return fields
    return {}

def analyze_insolvency(pdf_text):
    """Extract all insolvency fields"""
    print("\n=== ANALYZING INSOLVENCY ===")
    
    # Find insolvency filings section - use simpler pattern
    insolvency_match = re.search(
        r'organization\.legalEvents\.insolvency\.filings\s*\[array \(object\)\](.*?)organization\.legalEvents\.judgments',
        pdf_text,
        re.DOTALL
    )
    
    if insolvency_match:
        insolvency_text = insolvency_match.group(0)
        fields = extract_field_info(insolvency_text, 'organization.legalEvents.insolvency')
        
        print(f"Found {len(fields)} insolvency fields:")
        
        # Group by category
        categories = {}
        for field_name, info in sorted(fields.items()):
            parts = field_name.replace('organization.legalEvents.insolvency.filings.', '').split('.')
            category = parts[0] if parts else 'root'
            if category not in categories:
                categories[category] = []
            categories[category].append((field_name, info))
        
        for category, fields_list in sorted(categories.items()):
            print(f"\n  {category.upper()}: ({len(fields_list)} fields)")
            for field_name, info in fields_list[:5]:  # Show first 5
                short_name = field_name.split('.')[-1]
                print(f"    - {short_name}: {info['type']}")
        
        return fields
    return {}

def analyze_liquidation(pdf_text):
    """Extract liquidation fields (similar structure to insolvency)"""
    print("\n=== ANALYZING LIQUIDATION ===")
    
    # Search for liquidation section - use simpler pattern
    liquidation_match = re.search(
        r'organization\.legalEvents\.liquidation\.filings\s*\[array \(object\)\](.*?)organization\.legalEvents\.lien',
        pdf_text,
        re.DOTALL
    )
    
    if liquidation_match:
        liquidation_text = liquidation_match.group(0)
        fields = extract_field_info(liquidation_text, 'organization.legalEvents.liquidation')
        
        print(f"Found {len(fields)} liquidation fields")
        return fields
    else:
        print("Note: Liquidation likely uses similar structure to Insolvency")
        print("Will reuse Insolvency model structure for Liquidation")
        return {}

def generate_enhancement_plan(violations, financing, insolvency, liquidation):
    """Generate a structured plan for v2.0 implementation"""
    print("\n" + "="*80)
    print("V2.0 ENHANCEMENT PLAN")
    print("="*80)
    
    plan = {
        "version": "2.0.0",
        "enhancements": []
    }
    
    # Violations enhancement
    if violations:
        violation_summary = {
            "model": "Violation",
            "action": "Enhance existing model with complete EPA/OSHA/GCL/DOL/Medicare fields",
            "field_count": len(violations),
            "key_additions": [
                "totalEPAViolationsCount",
                "totalEPAViolationsAmount",
                "mostRecentEPAViolationDate",
                "totalOSHAViolationsCount",
                "totalOSHAViolationsAmount",
                "mostRecentOSHAViolationDate",
                "totalGCLCitationsCount",
                "totalDOLWagesHoursViolationsCount",
                "totalMedicareNursingHomeViolationsCount"
            ],
            "loader": "Needs implementation in loader.py"
        }
        plan["enhancements"].append(violation_summary)
        
        print("\n1. VIOLATIONS MODEL")
        print(f"   - Current: Basic boolean flags only")
        print(f"   - Enhanced: {len(violations)} fields covering:")
        print(f"     * EPA violations (count, amount, dates)")
        print(f"     * OSHA violations (count, amount, dates)")
        print(f"     * GCL citations (count, amount, dates)")
        print(f"     * DOL wage/hour violations")
        print(f"     * Medicare nursing home violations")
        print(f"     * Canadian environmental violations")
    
    # Financing Events enhancement
    if financing:
        financing_summary = {
            "model": "FinancingEvent (UCC Filings)",
            "action": "Complete model with full UCC filing details",
            "field_count": len(financing),
            "key_structures": [
                "collaterals (array) - asset details, types, quantities",
                "rolePlayers (array) - debtors, secured parties",
                "contactEvents (array) - contact information",
                "filing details - dates, amounts, references, types",
                "status and results information"
            ],
            "loader": "Needs implementation in loader.py"
        }
        plan["enhancements"].append(financing_summary)
        
        print("\n2. FINANCING EVENTS MODEL (UCC Filings)")
        print(f"   - Current: Model exists but no loader")
        print(f"   - Enhanced: {len(financing)} fields covering:")
        print(f"     * Collateral details (vehicles, equipment, property)")
        print(f"     * Role players (debtors, secured parties)")
        print(f"     * Filing information (dates, amounts, references)")
        print(f"     * Document types and statuses")
        print(f"     * Contact events and results")
    
    # Insolvency enhancement
    if insolvency:
        insolvency_summary = {
            "model": "Insolvency",
            "action": "Complete model with comprehensive bankruptcy/insolvency details",
            "field_count": len(insolvency),
            "key_structures": [
                "activities (array) - bankruptcy proceedings",
                "collaterals (array) - secured assets",
                "assetClass (array) - asset categorization",
                "contactEvents (array) - trustee/lawyer contacts",
                "rolePlayers (array) - creditors, debtors, trustees",
                "courtAddress - full court location details",
                "amounts - awarded, filed amounts"
            ],
            "loader": "Needs enhancement in loader.py"
        }
        plan["enhancements"].append(insolvency_summary)
        
        print("\n3. INSOLVENCY MODEL")
        print(f"   - Current: Minimal structure")
        print(f"   - Enhanced: {len(insolvency)} fields covering:")
        print(f"     * Activities and proceedings")
        print(f"     * Collateral and asset details")
        print(f"     * Contact events (trustees, lawyers)")
        print(f"     * Role players (creditors, debtors)")
        print(f"     * Court information and addresses")
        print(f"     * Amounts and dates")
    
    # Liquidation enhancement
    liquidation_summary = {
        "model": "Liquidation",
        "action": "Complete model using Insolvency structure (similar data model)",
        "field_count": "Same as Insolvency",
        "key_structures": [
            "Same structure as Insolvency",
            "Specific to company winding-up/liquidation events"
        ],
        "loader": "Needs enhancement in loader.py"
    }
    plan["enhancements"].append(liquidation_summary)
    
    print("\n4. LIQUIDATION MODEL")
    print(f"   - Current: Minimal structure")
    print(f"   - Enhanced: Similar to Insolvency (~{len(insolvency)} fields)")
    print(f"     * Company winding-up details")
    print(f"     * Asset liquidation information")
    print(f"     * Liquidator/administrator contacts")
    print(f"     * Creditor information")
    
    print("\n" + "="*80)
    print("IMPLEMENTATION PRIORITY")
    print("="*80)
    print("1. Violations - Clear structure, straightforward implementation")
    print("2. Insolvency/Liquidation - Similar models, can implement together")
    print("3. Financing Events - Most complex (UCC filings with collateral details)")
    print("\n" + "="*80)
    
    return plan

def main():
    # Read PDF content
    pdf_file = Path('pdf_full_content.txt')
    if not pdf_file.exists():
        print("ERROR: pdf_full_content.txt not found")
        return
    
    print(f"Reading {pdf_file.name}...")
    pdf_text = pdf_file.read_text(encoding='utf-8')
    print(f"Loaded {len(pdf_text)} characters")
    
    # Analyze each section
    violations = analyze_violations(pdf_text)
    financing = analyze_financing_events(pdf_text)
    insolvency = analyze_insolvency(pdf_text)
    liquidation = analyze_liquidation(pdf_text)
    
    # Generate enhancement plan
    plan = generate_enhancement_plan(violations, financing, insolvency, liquidation)
    
    # Save detailed field definitions
    output = {
        "violations": violations,
        "financing_events": financing,
        "insolvency": insolvency,
        "liquidation": liquidation,
        "enhancement_plan": plan
    }
    
    output_file = Path('schema_enhancement_v2.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Detailed field definitions saved to {output_file}")
    print(f"✓ Ready to begin v2.0 implementation")

if __name__ == '__main__':
    main()
