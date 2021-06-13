from .auth import Auth
from flask import redirect, url_for, request
from functools import wraps
import base64
import json
import datetime


def role_required(role: str):
    def wrapper(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            find_role = Auth.find_role(role_str=role)
            if find_role:
                return f(*args, **kwargs)

            return 'No access'

        return wrap

    return wrapper


def login_required_api(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth = Auth()
        if auth.is_authenticated():
            return f(*args, **kwargs)

        return {'Ok': False, 'Message': '401 Unauthorized'}, 401

    return wrap


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth = Auth()
        if auth.is_authenticated():
            return f(*args, **kwargs)

        return redirect(url_for('auth.login', next=request.path))

    return wrap


def authenticated_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')

            if not Auth.is_authenticated():

                if not auth_header or not auth_header.startswith('Bearer'):
                    return '401 Unauthorized', 401

                _, token = auth_header.split(' ')
                if not Auth.verify_jwt(token):
                    return '401 Unauthorized', 401

                _, b64_payload, _ = token.split('.')
                payload = json.loads(base64.b64decode(b64_payload).decode())
                exp = datetime.datetime.strptime(payload['exp'], '%Y-%m-%dT%H:%M:%S')
                if exp < datetime.datetime.utcnow():
                    return '401 Unauthorized', 401

            return f(*args, **kwargs)
        except Exception as err:
            return '401 Unauthorized', 401

    return wrap
