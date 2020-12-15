import shutil
import os

BASE_DIR = os.path.dirname(__file__)

BUILD_STATIC_DIR = os.path.join(BASE_DIR, '../build/static/js')
BUILD_INDEX_FILE = os.path.join(BASE_DIR, '../build/index.html')

STATIC_DIR = os.path.join(BASE_DIR, '../static/js')
TEMPLATES_INDEX_FILE = os.path.join(BASE_DIR, '../templates/frontend/index.html')

shutil.copy(BUILD_INDEX_FILE, TEMPLATES_INDEX_FILE)
print("copied index.html")

shutil.rmtree(STATIC_DIR)
print("cleaned static")

shutil.copytree(BUILD_STATIC_DIR, STATIC_DIR)
print("copied static")
print("ALL SUCCESSFULLY")


