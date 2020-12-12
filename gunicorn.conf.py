import multiprocessing
from config import *

bind = "127.0.0.1:" + PORT
workers = multiprocessing.cpu_count() * 2