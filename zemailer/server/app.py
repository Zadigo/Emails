import csv
import secrets

import quart
from quart import jsonify, render_template, request, websocket
from quart.templating import render_template
from werkzeug.utils import secure_filename

from zemailer.server.connections import RedisConnection
from zemailer.server.loggers import base_logger
from zemailer.validation.iterators import verify_from_file
from zemailer.validation.validators import validate
from zemailer.patterns import Emails

app = quart.Quart(__name__)
app.logger.addHandler(base_logger.handler)
app.secret_key = 'test'
redis = RedisConnection().get_connection


@app.route('/', methods=['get'])
async def home():
    return await render_template('home.html')


@app.route('/verify', methods=['post'])
async def verify_email():
    data = await request.files
    if data:
        file = data['emails']
        filename = secure_filename(file.filename)
        new_file_name = secrets.token_hex(15)
        with open(f'{app.root_path}/downloads/{new_file_name}.csv', mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            print(writer)
            with open(file, mode='r', encoding='utf-8') as d:
                reader = csv.reader(d)
                print(reader)   
        return jsonify({'result': True})
    else:
        result = False
        response = {}
        data = await request.form
        email = data.get('email', None)
        if email is not None:
            result, email_object = validate(email)
            if email_object is not None:
                response = email_object.get_json_response()
        return jsonify({'email': email, 'is_valid': result, 'validation': response})


@app.route('/generate', methods=['post'])
async def generate_emails_view():
    data = await request.form
    instance = Emails(
        data['firstname'],
        data['lastname'],
        domain=data['domain'],
        pattern_only=data['pattern_only']
    )
    emails = list(map(lambda x: str(x), instance))
    return jsonify({'items': emails, 'count': len(emails)})
