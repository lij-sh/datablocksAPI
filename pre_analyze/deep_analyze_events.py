import json

# Deep analysis of events structure
with open(r'c:\Users\jun\dataground\eventsfilings.json', encoding='utf-8') as f:
    events_data = json.load(f)

org = events_data['organization']

print("=== TOP-LEVEL ORGANIZATION KEYS ===")
for key in sorted(org.keys()):
    print(f"\n{key}:")
    value = org[key]
    if isinstance(value, dict):
        print(f"  Type: dict with {len(value.keys())} keys")
        print(f"  Keys: {list(value.keys())[:10]}")  # First 10 keys
        # Check if it has arrays underneath
        for subkey, subvalue in list(value.items())[:3]:
            if isinstance(subvalue, list) and subvalue:
                print(f"    {subkey}: array with {len(subvalue)} items")
                if isinstance(subvalue[0], dict):
                    print(f"      First item keys: {list(subvalue[0].keys())[:10]}")
    elif isinstance(value, list):
        print(f"  Type: array with {len(value)} items")
        if value and isinstance(value[0], dict):
            print(f"  First item keys: {list(value[0].keys())[:10]}")
    else:
        print(f"  Type: {type(value).__name__} = {value}")

# Deep dive into legal events if present
if 'legalEvents' in org:
    print("\n\n=== LEGAL EVENTS STRUCTURE ===")
    legal = org['legalEvents']
    print(f"LegalEvents type: {type(legal).__name__}")
    if isinstance(legal, dict):
        print(f"\nLegalEvents keys: {list(legal.keys())}")
        for key, value in legal.items():
            if isinstance(value, list) and value:
                print(f"\n{key}:")
                print(f"  Array length: {len(value)}")
                print(f"  First item type: {type(value[0]).__name__}")
                if isinstance(value[0], dict):
                    print(f"  First item keys: {list(value[0].keys())}")

# Deep dive into awards structure
if 'awards' in org:
    print("\n\n=== AWARDS STRUCTURE ===")
    awards = org['awards']
    print(f"Awards type: {type(awards).__name__}")
    if isinstance(awards, dict):
        print(f"\nAwards keys: {list(awards.keys())}")
        for key, value in awards.items():
            if isinstance(value, list) and value:
                print(f"\n{key}:")
                print(f"  Array length: {len(value)}")
                print(f"  First item type: {type(value[0]).__name__}")
                if isinstance(value[0], dict):
                    print(f"  First item keys: {list(value[0].keys())[:15]}")

# Check significant events
if 'significantEvents' in org:
    print("\n\n=== SIGNIFICANT EVENTS STRUCTURE ===")
    sig = org['significantEvents']
    print(f"SignificantEvents type: {type(sig).__name__}")
    if isinstance(sig, dict):
        print(f"\nSignificantEvents keys: {list(sig.keys())}")
        for key, value in sig.items():
            if isinstance(value, list) and value:
                print(f"\n{key}:")
                print(f"  Array length: {len(value)}")
                if isinstance(value[0], dict):
                    print(f"  First item keys: {list(value[0].keys())[:10]}")
