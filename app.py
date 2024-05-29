from CheckCredentials import CheckCredential
from GenerateTickets import GenerateTicket
from CheckMatrix import CheckMatrix

from flask import Flask, send_file, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return send_file("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cc = CheckCredential(username, password, "adimentional")

    if cc.logIn():
        return redirect(url_for("getAmount"))
    else:
        return "CREDENZIALI NON VALIDE"

@app.route('/getAmount')
def getAmount():
    return send_file("generate.html")

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    gen = GenerateTicket("adimentional", "778272")
    #amount = int(request.form['amount'])

    img_path = gen.generate()
    return send_file(img_path, as_attachment = True)


@app.route('/decode_qr', methods=['GET', 'POST'])
def decode_qr():
    data = request.json
    decoded_qr = data.get('code')
    cm = CheckMatrix(decoded_qr)

    if cm.check():
        return "APPROVATO"
    else:
        return "NON APPROVATO"

@app.route('/read')
def read():
    return send_file('camera.html')

