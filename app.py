from flask import Flask, request, render_template, send_file
from io import BytesIO
import pandas as pd
from receipts_parser import parse_receipt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        records = []
        for f in files:
            if not f.filename.lower().endswith('.pdf'):
                continue
            f.stream.seek(0)
            label, category, amount = parse_receipt(f)
            records.append({'Label': label, 'Category': category, 'Amount': amount})
        if not records:
            return 'No valid PDF receipts uploaded.', 400
        df = pd.DataFrame(records)
        total = df['Amount'].sum()
        total_row = pd.DataFrame({'Label': ['Total'], 'Category': [''], 'Amount': [total]})
        df = pd.concat([df, total_row], ignore_index=True)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return send_file(
            output,
            as_attachment=True,
            download_name='receipts.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
