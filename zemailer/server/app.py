import csv

import quart
from quart import jsonify, render_template, request, websocket
from quart.templating import render_template
from werkzeug.utils import secure_filename

from zemailer.server.connections import RedisConnection
from zemailer.server.loggers import base_logger
from zemailer.validation.validators import validate

app = quart.Quart(__name__)
app.logger.addHandler(base_logger.handler)
app.secret_key = 'test'

redis = RedisConnection()


@app.route('/', methods=['get'])
async def home():
    return await render_template('home.html')


@app.route('/verify', methods=['post'])
async def verify_email():
    email = request.form.get('email', None)
    if email is not None:
        print('email', email)
    return jsonify({'test': True})


@app.route('/verify-emails', methods=['post'])
async def verify_emails():
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
