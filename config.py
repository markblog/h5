import os
import logging
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from app.tasks.email_job import email_job
from app.tasks.report_job import reportJob
from app.tasks.file_job import fileJob

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '0x1092-3dfe834-324few23-342dlej'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    LOGGING_FORMAT = """[%(levelname)s] - %(asctime)s : %(message)s
%(module)s [%(pathname)s:%(lineno)d]
    """
    LOGGING_LOCATION = 'log/debug.log'
    LOGGING_LEVEL = logging.DEBUG
    PDF_TOOL_PATH = 'D:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    PDF_IMAGE_PATH = 'D:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe'
    REPORTS_PATH = 'reports'

    DATA_FOLDER = ''
    EXCLUDE_RULES = ['/api/v2/messages/count']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres:gxtagging@localhost/ai_test'

    JOBS = [
        {
            'id': 'email_task',
            'func': email_job,
            'trigger': 'interval',
            'seconds': 60 * 60 *24
        },
        {
            'id': 'report_task',
            'func': reportJob,
            'trigger': 'interval',
            'seconds': 10 * 60 * 60
        },
        {
            'id': 'file_task',
            'func': fileJob,
            'trigger': 'interval',
            'seconds': 10 * 60 * 60
        }
    ]

    SCHEDULER_API_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgresql://postgres:123456@localhost/ai_test'


class ProductionConfig(Config):
    LOGGING_LOCATION = 'log/errors.log'
    LOGGING_LEVEL = logging.ERROR
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:123456@localhost/ai'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


