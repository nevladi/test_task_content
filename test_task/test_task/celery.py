import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_task.settings')

app = Celery('test_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
