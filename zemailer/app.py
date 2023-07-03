import asyncio
import os

import quart
from quart import jsonify, render_template, request, websocket
# from quart_schema import QuartSchema, validate_request, validate_response

from zemailer import models
from zemailer.connections import RedisConnection
from zemailer.decorators import authenticate
from zemailer.loggers import base_logger


app = quart.Quart(__name__)
app.logger.addHandler(base_logger.handler)

# QuartSchema(app)

redis = RedisConnection()


async def websocket_receive():
    message = await websocket.receive()
    print('message', message)
    # while True:


@app.route('/', methods=['get'])
async def home():
    return await render_template('home.html')


# @validate_request(models.TodoIn)
# @validate_response(models.Todo)
@app.route('/testing', methods=['post'])
async def test_something(data=None):
    instance = TestOpenDataSoft()
    await instance.send(app=app)
    data = instance.response_data
    return jsonify(data)


@app.websocket('/ws')
async def some_socket():
    # loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(websocket_receive())
    future = await asyncio.gather(task)

    # loop.run_until_complete(future)
    print('future', future)
    # loop.close()

    instance = SearchAddress('36 rue de Suède', post_code=59000)
    await instance.send()
    data = instance.response_data
    w = await websocket.send_json(response=data)

    # try:
    #     task = asyncio.ensure_future(websocket_receive())
    # except:
    #     pass
    # else:
    #     t = await websocket.send('Message received')
    #     # task.cancel()
    #     await task
    #     # print(t)


@app.route('/health')
@authenticate
async def healthcheck():
    app.logger.info('Health check completed')
    return jsonify({'state': True})
