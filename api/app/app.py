import logging
from flask import Flask
from flask_cors import CORS
import os


DEBUG = True if 'DEBUG' in os.environ else False
logging.basicConfig(level=logging.INFO)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
APP = Flask(__name__)
APP.debug = DEBUG

CORS(APP)
