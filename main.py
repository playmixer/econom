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

    from apps.auth import auth_app
    from apps.econom import econom_app

    app.register_blueprint(econom_app, url_prefix=config.SUBDIRECTORY + '/')
    app.register_blueprint(auth_app, url_prefix=config.SUBDIRECTORY + '/auth')

    processor.init_app(app)

    @app.errorhandler(404)
    def err_404(err):
        return render_template('404.html')

    return app


if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0')
