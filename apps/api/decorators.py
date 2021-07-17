from .lib import response_json
from functools import wraps
from . import exceptions


def exception(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as err:
            print(f"error function {f.__name__}: {args}, {kwargs} \n {str(err)}")
            return response_json(False, error=str(err))

    return wrapper
