from celery_worker import app

app.worker_main(['-A', 'celery_worker', 'worker', '--loglevel=INFO', '-E', '-B'])
