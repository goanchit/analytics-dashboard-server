from flask import Flask, request, jsonify
from app.config.config import load_config
from app.config.db import connect_db, close_db_connection
import ssl
import pytz
import signal
import sys
from flask_cors import CORS
from app.utils.custom_logger import logger

from app.api.handler import router

utc = pytz.UTC
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

application = Flask(__name__, instance_relative_config=True)
CORS(application, resources={r"/*": {"origins": "*"}})

with application.app_context():
    logger.info("Establishing DB Connection")
    connect_db()

@application.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Routing
application.register_blueprint(router, url_prefix="/api")

def graceful_shutdown(signum, frame):
    logger.warning("Received signal {}, gracefully shutting down...".format(signum))
    # app.logger.warning("Closing Database Connection")
    # close_db_connection()
    # app.logger.info("Closed Database Connection")
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

if __name__ == "main":
    application.run()