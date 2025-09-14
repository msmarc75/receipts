import re
import pdfplumber


def parse_receipt(file_obj):
    """Extract label, category, and amount from a PDF receipt.

    Expected fields in the receipt text:
      - Encaisseur: merchant or transaction label
      - Code de catégorie du marchand: transaction category
      - Montant: amount value
    """
    file_obj.seek(0)
    with pdfplumber.open(file_obj) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    label_match = re.search(r"Encaisseur\s*:\s*(.*)", text)
    category_match = re.search(r"Code de catégorie du marchand\s*:\s*(.*)", text)
    amount_match = re.search(r"Montant\s*:\s*([0-9]+(?:[.,][0-9]+)?)", text)

    label = label_match.group(1).strip() if label_match else "Unknown"
    category = category_match.group(1).strip() if category_match else "Unknown"
    amount_text = amount_match.group(1) if amount_match else "0"
    amount_text = amount_text.replace(",", ".").strip()

    try:
        amount_value = float(amount_text)
    except ValueError:
        amount_value = 0.0

    return label, category, amount_value
