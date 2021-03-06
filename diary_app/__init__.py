import os
from flask import Flask
from flask.ext.cors import CORS
from diary_app.database import db

# Initialize App
application = Flask(__name__)
CORS(application)
application.config.from_object(
    'diary_app.config.' + os.getenv('EPILEPSY_CONFIG'))

# Initialize Logging
'''
from diary_app.utils import logger
application.logger.addHandler(logger.get_rotating_file_handler(APP_LOG_FILE))
items_log = logger.get_logger(JOB_ITEMS_LOG_FILE, log_level=LOG_LEVEL)
tasks_log = logger.get_logger(TASKS_LOG_FILE,  log_level=LOG_LEVEL)
jobs_log = logger.get_logger(JOBS_LOG_FILE, log_level=LOG_LEVEL)
'''

# Import APIs
import diary_app.users.api
import diary_app.events.api
import diary_app.charts.api


@application.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()
