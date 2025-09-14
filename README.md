# Receipts Web App

This simple Flask application lets you upload PDF receipts and generates an Excel file listing each receipt's transaction label, category, and amount. A total of all amounts is added at the bottom of the spreadsheet.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open your browser at `http://localhost:5000` and upload your PDF receipts.

The generated Excel file will download automatically after processing.
