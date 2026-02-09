CELERY_CONFIG = {
    'broker_url': 'redis://redis:6379/0',
    'result_backend': 'redis://redis:6379/0',
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'broker_connection_retry_on_startup': True
}