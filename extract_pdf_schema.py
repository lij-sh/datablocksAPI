import PyPDF2
import json
import re

# Extract text from PDF
pdf_file = open('Material/openApiSpec-dataBlocks.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

print(f"Total pages: {len(pdf_reader.pages)}\n")

# Extract table of contents or key sections
for i in range(min(10, len(pdf_reader.pages))):
    text = pdf_reader.pages[i].extract_text()
    if 'Table of Contents' in text or 'Contents' in text:
        print(f"=== Page {i+1} (TOC) ===")
        print(text[:2000])
        print("\n...")
        break

# Look for schema definitions
print("\n=== Searching for key sections ===")
sections_found = {}

for i, page in enumerate(pdf_reader.pages):
    text = page.extract_text()
    
    # Look for key event types
    if 'insolvency' in text.lower() and 'insolvency' not in sections_found:
        sections_found['insolvency'] = i + 1
    if 'liquidation' in text.lower() and 'liquidation' not in sections_found:
        sections_found['liquidation'] = i + 1
    if 'financing' in text.lower() and 'ucc' in text.lower() and 'financing' not in sections_found:
        sections_found['financing'] = i + 1
    if 'violation' in text.lower() and 'epa' in text.lower() and 'violations' not in sections_found:
        sections_found['violations'] = i + 1
    
    if len(sections_found) >= 4:
        break

print("\nSections found:")
for section, page_num in sorted(sections_found.items(), key=lambda x: x[1]):
    print(f"  {section}: page {page_num}")

pdf_file.close()
