import json

with open(r'c:\Users\jun\dataground\companyfinancial.json', encoding='utf-8') as f:
    financial_data = json.load(f)

org = financial_data['organization']

print("=== FINANCIAL DATA STRUCTURE ===\n")
print(f"Organization keys: {list(org.keys())}\n")

# Check latestFiscalFinancials
if 'latestFiscalFinancials' in org and org['latestFiscalFinancials']:
    print("latestFiscalFinancials:")
    latest = org['latestFiscalFinancials']
    print(f"  Type: {type(latest)}")
    print(f"  Keys ({len(latest.keys())} total):")
    for key in sorted(latest.keys())[:30]:
        value = latest[key]
        if isinstance(value, list) and value:
            print(f"    {key}: array[{len(value)}]")
        elif isinstance(value, dict) and value:
            print(f"    {key}: dict with {list(value.keys())[:5]}")
        else:
            print(f"    {key}: {type(value).__name__}")
    print()

# Check otherFinancials
if 'otherFinancials' in org and org['otherFinancials']:
    print(f"\notherFinancials: array with {len(org['otherFinancials'])} records")
    first = org['otherFinancials'][0]
    print(f"  Each financial record has {len(first.keys())} keys:")
    for key in sorted(first.keys()):
        value = first[key]
        if isinstance(value, list) and value:
            print(f"    {key}: array[{len(value)}] - first item type: {type(value[0]).__name__}")
        elif isinstance(value, dict) and value:
            print(f"    {key}: dict - keys: {list(value.keys())[:5]}")
        else:
            print(f"    {key}: {type(value).__name__}")
    
    # Check nested structures
    print("\n  Nested financial structures:")
    if 'balanceSheet' in first and first['balanceSheet']:
        bs = first['balanceSheet']
        print(f"    balanceSheet: {type(bs).__name__} with {len(bs.keys())} keys")
        print(f"      Keys: {list(bs.keys())[:10]}")
    
    if 'profitAndLossStatement' in first and first['profitAndLossStatement']:
        pl = first['profitAndLossStatement']
        print(f"    profitAndLossStatement: {type(pl).__name__} with {len(pl.keys())} keys")
        print(f"      Keys: {list(pl.keys())[:10]}")
    
    if 'cashFlowStatement' in first and first['cashFlowStatement']:
        cf = first['cashFlowStatement']
        print(f"    cashFlowStatement: {type(cf).__name__} with {len(cf.keys())} keys")
        print(f"      Keys: {list(cf.keys())[:10]}")

# Check company info financials
with open(r'c:\Users\jun\dataground\companyinfo.json', encoding='utf-8') as f:
    info_data = json.load(f)

org_info = info_data['organization']
if 'financials' in org_info and org_info['financials']:
    print("\n\n=== COMPANY INFO - FINANCIALS ===\n")
    fin = org_info['financials']
    print(f"Type: {type(fin)}")
    if isinstance(fin, dict):
        print(f"Keys: {list(fin.keys())}")
        for key, value in fin.items():
            if isinstance(value, list):
                print(f"  {key}: array[{len(value)}]")
            elif isinstance(value, dict):
                print(f"  {key}: dict with keys {list(value.keys())[:5]}")
            else:
                print(f"  {key}: {type(value).__name__} = {value}")
