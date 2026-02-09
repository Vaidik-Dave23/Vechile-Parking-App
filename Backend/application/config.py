class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND = "redis://redis:6379/0"

class LocalDevlopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///parkingdb.sqlite3'
    JWT_SECRET_KEY = "this-is-a-secret-key"
    CELERY = {
        'broker_url': 'redis://redis:6379/0',
        'result_backend': 'redis://redis:6379/0',
        'task_serializer': 'json',
        'result_serializer': 'json',
        'broker_connection_retry_on_startup': True
    }