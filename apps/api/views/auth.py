from flask import request
from apps.auth.auth import Auth
from ..lib import response_json
from ..serialization.auth import Source, User


def init_auth(app):
    @app.route('/auth/source')
    def source():
        user = Auth.get_user()
        if user:
            data = Source(isAuth=True, model=User(username=user.username))
            return response_json(data=data.dict())

        data = Source(isAuth=False)
        return response_json(data=data.dict(exclude={'user'}))

    @app.route('/auth/signin', methods=['POST'])
    def signin():
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')
        if username is password is None:
            return response_json(ok=False)

        user = Auth.login(username, password)
        if not user:
            return response_json(ok=False)

        data = User(username=user.username)
        return response_json(data=data.dict())

    @app.route('/auth/logout')
    def logout():
        user = Auth.get_user()
        if user:
            Auth.logout()
        return response_json()
