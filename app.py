from io import BytesIO
from backEnd.CheckCredentials import CheckCredential
from backEnd.GenerateTickets import GenerateTicket

from PyPDF2 import PdfWriter
from PIL import Image
from io import BytesIO

import os

from flask import Flask, send_file, request, url_for, redirect, send_from_directory
app = Flask(__name__)

@app.route("/")
def index():
    return send_file("C:\\Users\\ade59\\OneDrive\\Desktop\\TicketLine_WebApp\\tamplate\\login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cc = CheckCredential(username, password, "adimentional")

    if cc.logIn():
        return redirect(url_for("gatAmount"))
    else:
        return "CREDENZIALI NON VALIDE"
    
@app.route('/getAmount')
def gatAmount():
    return send_file("C:\\Users\\ade59\\OneDrive\\Desktop\\TicketLine_WebApp\\tamplate\\generate.html")

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    gen = GenerateTicket("adimentional", "778272")
    amount = int(request.form['amount'])
    elements = []

    pdf_buffer = BytesIO()
    pdf_writer = PdfWriter()

    for i in range(amount):
        # Generazione del biglietto
        gen.generate(i)
        img_name = "ticket" + str(i) + ".jpeg"
        img_path = os.path.join(app.root_path, img_name)
        img = Image.open(img_path)
        img_pdf = BytesIO()
        img.save(img_pdf, format='PDF')
        pdf_writer.append(img_pdf)

    pdf_writer.write(pdf_buffer)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,download_name='tickets.pdf'
    )

     

if __name__ == "__main__":
    #app.run(host="192.168.1.8",debug = True)
    app.run(debug = True)