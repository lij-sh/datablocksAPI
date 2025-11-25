import json

# Analyze companyinfo.json
with open(r'c:\Users\jun\dataground\companyinfo.json', encoding='utf-8') as f:
    company_info = json.load(f)
    
print("=== COMPANY INFO STRUCTURE ===")
print(f"Top-level keys: {list(company_info.keys())}")
print(f"\nOrganization keys ({len(company_info['organization'].keys())} total):")
for key in sorted(company_info['organization'].keys()):
    print(f"  - {key}")

# Analyze companyfinancial.json
with open(r'c:\Users\jun\dataground\companyfinancial.json', encoding='utf-8') as f:
    financial_data = json.load(f)
    
print("\n\n=== COMPANY FINANCIAL STRUCTURE ===")
print(f"Top-level keys: {list(financial_data.keys())}")
org = financial_data['organization']
print(f"\nOrganization keys: {list(org.keys())}")

if 'otherFinancials' in org and org['otherFinancials']:
    print(f"\nFinancial record keys ({len(org['otherFinancials'][0].keys())} total):")
    for key in sorted(org['otherFinancials'][0].keys()):
        print(f"  - {key}")

# Analyze eventsfilings.json
with open(r'c:\Users\jun\dataground\eventsfilings.json', encoding='utf-8') as f:
    events_data = json.load(f)
    
print("\n\n=== EVENTS FILINGS STRUCTURE ===")
print(f"Top-level keys: {list(events_data.keys())}")
org = events_data['organization']
print(f"\nOrganization keys ({len(org.keys())} total):")
for key in sorted(org.keys()):
    print(f"  - {key}")
