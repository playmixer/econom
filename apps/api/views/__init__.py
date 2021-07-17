from flask import Blueprint
from .auth import init_auth
from .econom import init_econom

api = Blueprint(
    __name__,
    'api'
)

init_auth(api)
init_econom(api)
