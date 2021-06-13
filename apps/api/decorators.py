from .lib import response_json
from functools import wraps


def exception(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as err:
            return response_json(False, message=str(err))

    return wrapper
