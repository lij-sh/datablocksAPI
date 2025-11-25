import json

with open(r'c:\Users\jun\dataground\eventsfilings.json', encoding='utf-8') as f:
    events_data = json.load(f)

org = events_data['organization']

# Exhaustive check of legal events
print("=== ALL LEGAL EVENT TYPES ===\n")
legal = org.get('legalEvents', {})
print(f"Total keys in legalEvents: {len(legal.keys())}\n")

# Find all that are dicts with 'filings' arrays
event_types = []
for key, value in legal.items():
    if isinstance(value, dict) and 'filings' in value:
        event_types.append(key)
        filings = value['filings']
        print(f"{key}:")
        print(f"  Has 'filings' array: {len(filings)} records")
        print(f"  Keys: {list(value.keys())}")
        if filings:
            print(f"  Sample filing keys: {list(filings[0].keys())[:15]}")
        print()

print(f"\nEvent types with filings arrays: {event_types}")

# Check awards
print("\n\n=== ALL AWARD TYPES ===\n")
awards = org.get('awards', {})
print(f"Total keys in awards: {len(awards.keys())}\n")

award_types = []
for key, value in awards.items():
    if isinstance(value, list) and value:
        award_types.append(key)
        print(f"{key}:")
        print(f"  Array length: {len(value)}")
        print(f"  Sample record keys: {list(value[0].keys())[:20]}")
        print()

print(f"\nAward types with arrays: {award_types}")

# Check financing events
print("\n\n=== ALL FINANCING EVENT TYPES ===\n")
financing = org.get('financingEvents', {})
print(f"Total keys in financingEvents: {len(financing.keys())}\n")

financing_types = []
for key, value in financing.items():
    if isinstance(value, list) and value:
        financing_types.append(key)
        print(f"{key}:")
        print(f"  Array length: {len(value)}")
        print(f"  Sample record keys: {list(value[0].keys())[:15]}")
        print()

print(f"\nFinancing types with arrays: {financing_types}")

# Check significant events
print("\n\n=== SIGNIFICANT EVENTS ===\n")
sig = org.get('significantEvents', {})
print(f"Total keys in significantEvents: {len(sig.keys())}")
for key, value in sig.items():
    if isinstance(value, list) and value:
        print(f"\n{key}:")
        print(f"  Array length: {len(value)}")
        print(f"  Sample record keys: {list(value[0].keys())}")

# Check violations
print("\n\n=== ALL VIOLATION TYPES ===\n")
violations = org.get('violations', {})
print(f"Total keys in violations: {len(violations.keys())}\n")

violation_types = []
for key, value in violations.items():
    if isinstance(value, list) and value:
        violation_types.append(key)
        print(f"{key}:")
        print(f"  Array length: {len(value)}")
        print(f"  Sample record keys: {list(value[0].keys())[:15]}")
        print()

print(f"\nViolation types with arrays: {violation_types}")

# Check commercial collection claims
print("\n\n=== COMMERCIAL COLLECTION CLAIMS ===\n")
claims = org.get('commercialCollectionClaims', {})
print(f"Type: {type(claims)}")
print(f"Keys: {list(claims.keys()) if isinstance(claims, dict) else 'N/A'}")

# Check exclusions
print("\n\n=== EXCLUSIONS ===\n")
exclusions = org.get('exclusions', {})
print(f"Type: {type(exclusions)}")
print(f"Keys: {list(exclusions.keys()) if isinstance(exclusions, dict) else 'N/A'}")

# Check document filings
print("\n\n=== DOCUMENT FILINGS ===\n")
doc_filings = org.get('documentFilings', [])
print(f"Type: {type(doc_filings)}")
if isinstance(doc_filings, list):
    print(f"Array length: {len(doc_filings)}")
    if doc_filings:
        print(f"Sample record keys: {list(doc_filings[0].keys())}")
