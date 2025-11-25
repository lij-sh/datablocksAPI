import json

with open(r'c:\Users\jun\dataground\eventsfilings.json', encoding='utf-8') as f:
    events_data = json.load(f)

org = events_data['organization']

# Show legal events hierarchy
print("=== LEGAL EVENTS HIERARCHY ===\n")
legal = org['legalEvents']

# Show boolean flags
print("Flags:")
for key in ['hasLegalEvents', 'hasOpenLegalEvents', 'hasLiens', 'hasJudgments', 'hasBankruptcy', 'hasClaims', 'hasSuits']:
    if key in legal:
        print(f"  {key}: {legal[key]}")

# Show the arrays under legalEvents
print("\nArray fields:")
for key in ['liens', 'judgments', 'bankruptcy', 'suits', 'claims', 'debarments', 'insolvency', 'liquidation', 'otherLegalEvents']:
    if key in legal and isinstance(legal[key], list):
        print(f"  {key}: {len(legal[key])} items")
        if legal[key]:
            print(f"    First item keys: {list(legal[key][0].keys())[:10]}")

# Sample lien structure
if 'liens' in legal and legal['liens']:
    print("\n\n=== SAMPLE LIEN STRUCTURE ===")
    print(json.dumps(legal['liens'][0], indent=2, default=str)[:1500])

# Sample judgment structure  
if 'judgments' in legal and legal['judgments']:
    print("\n\n=== SAMPLE JUDGMENT STRUCTURE ===")
    print(json.dumps(legal['judgments'][0], indent=2, default=str)[:1500])

# Show awards hierarchy
print("\n\n=== AWARDS HIERARCHY ===\n")
awards = org['awards']

print("Flags:")
for key in ['hasContracts', 'hasLoans', 'hasDebts', 'hasGrants']:
    if key in awards:
        print(f"  {key}: {awards[key]}")

print("\nArray fields:")
for key in ['contracts', 'loans', 'debts', 'grants']:
    if key in awards and isinstance(awards[key], list):
        print(f"  {key}: {len(awards[key])} items")
        if awards[key]:
            print(f"    First item keys: {list(awards[key][0].keys())[:15]}")

# Show financing events hierarchy
print("\n\n=== FINANCING EVENTS HIERARCHY ===\n")
financing = org.get('financingEvents', {})

print("Flags:")
for key in ['hasFinancingEvents', 'hasSecuredFilings', 'hasOpenSecuredFilings']:
    if key in financing:
        print(f"  {key}: {financing[key]}")

print("\nArray fields:")
for key in ['financingStatementFilings', 'mortgagesAndCharges']:
    if key in financing and isinstance(financing[key], list):
        print(f"  {key}: {len(financing[key])} items")
        if financing[key]:
            print(f"    First item keys: {list(financing[key][0].keys())[:10]}")

# Show significant events hierarchy
print("\n\n=== SIGNIFICANT EVENTS HIERARCHY ===\n")
sig_events = org.get('significantEvents', {})

print("Flags:")
for key in ['hasSignificantEvents', 'hasOperationalEvents', 'hasDisastrousEvents']:
    if key in sig_events:
        print(f"  {key}: {sig_events[key]}")

if 'events' in sig_events and sig_events['events']:
    print(f"\nevents: {len(sig_events['events'])} items")
    print(f"  First item keys: {list(sig_events['events'][0].keys())}")
    print(f"\n  Sample event:")
    print(json.dumps(sig_events['events'][0], indent=2, default=str)[:800])

# Show violations hierarchy
print("\n\n=== VIOLATIONS HIERARCHY ===\n")
violations = org.get('violations', {})

print("Flags:")
for key in ['hasEPAViolations', 'hasOSHAViolations', 'hasDOLWagesHoursViolations']:
    if key in violations:
        print(f"  {key}: {violations[key]}")

print("\nArray fields:")
for key in violations.keys():
    if isinstance(violations[key], list) and violations[key]:
        print(f"  {key}: {len(violations[key])} items")
        print(f"    First item keys: {list(violations[key][0].keys())[:10]}")
