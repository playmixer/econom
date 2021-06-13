from flask import Blueprint, render_template

frontend = Blueprint(
    'frontend',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@frontend.route('/', defaults={'path': ''})
@frontend.route('/<path:path>')
def index(path):
    print(path)
    return render_template('frontend/index.html')
