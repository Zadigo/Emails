from flask import Flask, jsonify, request
import csv
from flask.templating import render_template
from werkzeug.utils import secure_filename
from zemailer.validation.validators import validate

app = Flask(__name__)


@app.route('/', methods=['get'])
def home():
    return render_template('home.html')


@app.route('/verify', methods=['post'])
def verify_email():
    email = request.form.get('email', None)
    if email is not None:
        print('email', email)
    return jsonify({'test': True})


@app.route('/verify-emails', methods=['post'])
def verify_emails():
    file = request.files['email_file']
    if file.content_type != 'text/csv':
        return jsonify({'error': 'File not valid'})
    
    filename = secure_filename(file.filename)

    csv_reader = csv.reader(file)
    csv_data = []
    for row in csv_reader:
        csv_data.append(row)
    return jsonify({'test': True})

# python -m flask --app zemailer/server/app --debug run
