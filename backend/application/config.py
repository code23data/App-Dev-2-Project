import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://localhost:6380/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6380/2"


class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DB_DIR = os.path.join(basedir, "/db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///project_test_db.sqlite3"
    JWT_SECRET_KEY = "super-secret"  # Change this to your own secret key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    CELERY_BROKER_URL = "redis://localhost:6380/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6380/2"
    CELERY_TIMEZONE = "Asia/Kolkata"
    CELERY_ENABLE_UTC = True
    # CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = "redis://localhost:6380/3"
    CACHE_DEFAULT_TIMEOUT = 300

    DEBUG = True


class ProjectDevelopmentConfig(Config):
    SQLALCHEMY_DB_DIR = os.path.join(basedir, "/db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        SQLALCHEMY_DB_DIR, "project_example.sqlite3"
    )
    DEBUG = False
