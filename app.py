from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
import datetime

app = Flask(__name__)

# Create folder to save PDFs
if not os.path.exists('generated_invoices'):
    os.makedirs('generated_invoices')

class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Travel Invoice', ln=True, align='C')
        self.ln(5)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Samarth Tours and Travels ( Taxi/Cab services)', ln=True, align='C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, 'Gawane Chowk, near PCMC Bus stand, Bhosari, Pune, Pimpri-Chinchwad, Maharashtra 411039', ln=True, align='C')
        self.cell(0, 10, 'Contact: 9665444011', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    data = request.form
    customer_name = data['customer_name']
    pickup_location = data['pickup_location']
    drop_location = data['drop_location']
    travel_date = data['travel_date']
    km = float(data['km'])
    rate_per_km = float(data['rate_per_km'])
    toll_charges = float(data['toll_charges'])
    driver_allowance = float(data['driver_allowance'])

    base_amount = km * rate_per_km
    total_amount = base_amount + toll_charges + driver_allowance

    invoice_number = f"INV{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    invoice_date = datetime.date.today().strftime("%d-%m-%Y")

    pdf = InvoicePDF()
    pdf.add_page()

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Invoice Number: {invoice_number}", ln=True)
    pdf.cell(0, 10, f"Invoice Date: {invoice_date}", ln=True)
    pdf.cell(0, 10, f"Bill To: {customer_name}", ln=True)
    pdf.cell(0, 10, f"Travel Date: {travel_date}", ln=True)
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(20, 10, "S.No", border=1)
    pdf.cell(60, 10, "Description", border=1)
    pdf.cell(30, 10, "KM", border=1)
    pdf.cell(30, 10, "Rate/KM", border=1)
    pdf.cell(40, 10, "Total", border=1)
    pdf.ln()

    pdf.set_font('Arial', '', 12)
    pdf.cell(20, 10, "1", border=1)
    description = f"{pickup_location} to {drop_location}"
    pdf.cell(60, 10, description, border=1)
    pdf.cell(30, 10, str(km), border=1)
    pdf.cell(30, 10, str(rate_per_km), border=1)
    pdf.cell(40, 10, f"{base_amount:.2f}", border=1)
    pdf.ln()

    # Toll charges row
    pdf.cell(20, 10, "2", border=1)
    pdf.cell(60, 10, "Toll Charges", border=1)
    pdf.cell(30, 10, "-", border=1)
    pdf.cell(30, 10, "-", border=1)
    pdf.cell(40, 10, f"{toll_charges:.2f}", border=1)
    pdf.ln()

    # Driver allowance row
    pdf.cell(20, 10, "3", border=1)
    pdf.cell(60, 10, "Driver Allowance", border=1)
    pdf.cell(30, 10, "-", border=1)
    pdf.cell(30, 10, "-", border=1)
    pdf.cell(40, 10, f"{driver_allowance:.2f}", border=1)
    pdf.ln()

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(140, 10, "Total Amount", border=1)
    pdf.cell(40, 10, f"{total_amount:.2f}", border=1)
    
    filename = f"generated_invoices/{invoice_number}.pdf"
    pdf.output(filename)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
