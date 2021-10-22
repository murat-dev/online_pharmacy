import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_project.settings')

app = Celery('pharmacy_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery -A pharmacy_project worker -l info
# celery -A pharmacy_project flower