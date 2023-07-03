
import os
from functools import wraps

from quart import jsonify, request


def authenticate(func):
    """Authenticates an Authorization token
      against an incoming request"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        # Actual value is "Bearer xxx"
        name, token = token.split(' ', maxsplit=1)
        if token == os.getenv('AUTHENTICATION_TOKEN'):
            return await func(*args, **kwargs)
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    return wrapper
