from flask import Blueprint, render_template
import config

frontend = Blueprint(
    'frontend',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=config.SUBDIRECTORY + '/frontend/static'
)


@frontend.route('/', defaults={'path': ''})
@frontend.route('/<path:path>')
def index(path):
    print(path)
    return render_template('frontend/index.html')
