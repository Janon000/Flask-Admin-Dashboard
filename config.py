import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'omegalul'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    """SCHEDULER_JOBS = [{'id': 'test_job',
                      'func': 'routes:test_job',
                      'trigger': 'interval',
                      'seconds': 3}]"""


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    EXPLAIN_TEMPLATE_LOADING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or "sqlite:///database.db"


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or "sqlite:///database.db"


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or "sqlite:///database.db"
