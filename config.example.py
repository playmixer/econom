from datetime import timedelta
import logging

# Db
sql_user = 'root'
sql_pass = 'root'

# Logger
LOGGER_LEVEL = logging.INFO

# Gunicorn
HOST = '127.0.0.1'
PORT = '8000'
WORKERS = 3
WORKER_TIMEOUT = 30
SUBDIRECTORY = '/econom'

# Flask
SQLALCHEMY_DATABASE_URI = f'mysql://{sql_user}:{sql_pass}@localhost/econom'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'econom_secret_key_for_secure'
UPLOAD_FOLDER = 'uploads'
APPLICATION_ROOT = SUBDIRECTORY

PERMANENT_SESSION_LIFETIME = timedelta(days=1)
