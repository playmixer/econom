from flask import Flask, render_template
from core.database import db
import config
from core.template import processor


def create_app():
    app = Flask(
        __name__,
        static_url_path='/'.join([config.SUBDIRECTORY, 'static'])
    )
    app.config.from_pyfile('config.flask.py')

    db.init_app(app)
    from apps.econom import models

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
    create_app().run(debug=True)
