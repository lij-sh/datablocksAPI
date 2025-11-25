import json

with open(r'c:\Users\jun\dataground\eventsfilings.json', encoding='utf-8') as f:
    events_data = json.load(f)

org = events_data['organization']

# Check exclusions in detail
print("=== EXCLUSIONS STRUCTURE ===\n")
exclusions = org.get('exclusions', {})
print(f"Type: {type(exclusions)}")
print(f"Total keys: {len(exclusions.keys()) if isinstance(exclusions, dict) else 'N/A'}")

if isinstance(exclusions, dict):
    print(f"\nAll keys:")
    for key in sorted(exclusions.keys()):
        value = exclusions[key]
        if isinstance(value, list):
            print(f"  {key}: array with {len(value)} items")
            if value:
                print(f"    First item type: {type(value[0]).__name__}")
                if isinstance(value[0], dict):
                    print(f"    First item keys: {list(value[0].keys())[:20]}")
        elif isinstance(value, dict):
            print(f"  {key}: dict with keys {list(value.keys())[:5]}")
        else:
            print(f"  {key}: {type(value).__name__} = {value}")

# Check commercial collection claims too
print("\n\n=== COMMERCIAL COLLECTION CLAIMS STRUCTURE ===\n")
claims = org.get('commercialCollectionClaims', {})
print(f"Type: {type(claims)}")
print(f"Total keys: {len(claims.keys()) if isinstance(claims, dict) else 'N/A'}")

if isinstance(claims, dict):
    print(f"\nAll keys:")
    for key in sorted(claims.keys()):
        value = claims[key]
        if isinstance(value, list):
            print(f"  {key}: array with {len(value)} items")
            if value:
                print(f"    First item type: {type(value[0]).__name__}")
                if isinstance(value[0], dict):
                    print(f"    First item keys: {list(value[0].keys())[:20]}")
        elif isinstance(value, dict):
            print(f"  {key}: dict with keys {list(value.keys())[:5]}")
        else:
            print(f"  {key}: {type(value).__name__} = {value}")

# Check if exclusions exists in legalEvents too
print("\n\n=== CHECK IF EXCLUSIONS IN LEGAL EVENTS ===\n")
legal = org.get('legalEvents', {})
if 'exclusions' in legal:
    print("Found 'exclusions' in legalEvents!")
    exc = legal['exclusions']
    print(f"Type: {type(exc)}")
    if isinstance(exc, dict) and 'filings' in exc:
        print(f"Has 'filings' array: {len(exc['filings'])} records")
        print(f"Keys: {list(exc.keys())}")
else:
    print("No 'exclusions' key in legalEvents")

# Check all top-level organization keys one more time
print("\n\n=== ALL ORGANIZATION KEYS ===")
print(sorted(org.keys()))
