import asyncio
import os

import quart
from quart import jsonify, render_template, request, websocket

from zemailer.server.connections import RedisConnection
from zemailer.server.decorators import authenticate
from zemailer.server.loggers import base_logger
from zemailer.validation import validate_email

app = quart.Quart(__name__)
app.logger.addHandler(base_logger.handler)

redis = RedisConnection()


async def websocket_receive():
    message = await websocket.receive()
    print('message', message)
    # while True:


@app.route('/', methods=['get'])
async def home():
    return await render_template('home.html')


@app.route('/testing', methods=['post'])
async def test_something(data=None):
    return jsonify(data)
