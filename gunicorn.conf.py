from config import HOST, PORT, WORKERS, WORKER_TIMEOUT, LOGGER_LEVEL

bind = f"{HOST}:{PORT}"
workers = WORKERS
timeout = WORKER_TIMEOUT
loglevel = 'info'
reload = True
reload_engine = 'auto'
