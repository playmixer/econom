from apps.auth.auth import Auth
from datetime import datetime, timedelta


def date_now(d: int = 0):
    return datetime.utcnow() + timedelta(days=d)


def init_app(app):
    @app.context_processor
    def add_processor():

        return dict(
            auth=Auth,
        )
