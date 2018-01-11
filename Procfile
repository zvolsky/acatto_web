web: gunicorn config.wsgi:application
worker: celery worker --app=acatto_web.taskapp --loglevel=info
