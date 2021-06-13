from flask import Flask, render_template
import config
from core.template import processor

from apps.econom.models import *


def create_app():
    app = Flask(
        __name__,
        static_url_path='/'.join([config.SUBDIRECTORY, 'static'])
    )
    app.config.from_pyfile('config.flask.py')

    from core.database import db
    db.init_app(app)

    # from apps.auth import auth_app
    # from apps.econom import econom_app
    from apps.frontend.views import frontend
    from apps.api import api

    # app.register_blueprint(econom_app, url_prefix=config.SUBDIRECTORY + '/econom')
    # app.register_blueprint(auth_app, url_prefix=config.SUBDIRECTORY + '/auth')
    app.register_blueprint(api, url_prefix=config.SUBDIRECTORY + '/api/v0')
    app.register_blueprint(frontend, url_prefix="/")

    processor.init_app(app)

    @app.errorhandler(404)
    def err_404(err):
        return '404'  # render_template('404.html')

    return app


if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0')
