from PyPDF2 import PdfReader
from flask import Flask, request

app = Flask(__name__)


@app.route("/parse_pdf", methods=['POST'])
def parse_pdf():
    file = request.files['pdf_file']
    text = extract_text_from_file(file)

    invoice_start_index = text.index('Invoice')
    invoice_end_index = text.index('Tax')

    booking_no_string = 'Booking No.'
    booking_no_index = text.index(booking_no_string)
    booking_no_index = booking_no_index + len(booking_no_string)

    invoice_labels = text[invoice_start_index:booking_no_index]
    invoice_values = text[booking_no_index:invoice_end_index]

    table_start_index = text.index('Flight')
    table_end_index = text.index('Other')

    table = text[table_start_index:table_end_index:1]

    values = {'table': table, 'invoice_labels': invoice_labels, 'invoice_values': invoice_values}
    return values


@app.route("/read_pdf", methods=['POST'])
def read_pdf():
    file = request.files['pdf_file']
    text = extract_text_from_file(file)
    return {'text': text}


def extract_text_from_file(file):
    reader = PdfReader(file)
    page = reader.pages[0]
    return page.extract_text()


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=False)
