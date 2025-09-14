import re
import pdfplumber

def parse_receipt(file_obj):
    """Extract label, category, and amount from a PDF receipt."""
    file_obj.seek(0)
    with pdfplumber.open(file_obj) as pdf:
        text = "\n".join(page.extract_text() or '' for page in pdf.pages)
    label_match = re.search(r'Label\s*:\s*(.*)', text)
    category_match = re.search(r'Category\s*:\s*(.*)', text)
    amount_match = re.search(r'Amount\s*:\s*([0-9.,]+)', text)
    label = label_match.group(1).strip() if label_match else 'Unknown'
    category = category_match.group(1).strip() if category_match else 'Unknown'
    amount = amount_match.group(1).replace(',', '.').strip() if amount_match else '0'
    try:
        amount_value = float(amount)
    except ValueError:
        amount_value = 0.0
    return label, category, amount_value
