import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm1.settings')

app = Celery('store')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# celery beat tasks
app.conf.beat_schedule = {
    'text-every-minute': {
        'task': 'store.tasks.make_goods_update',
        'schedule': crontab(minute='0', hour='*/1'),
    }
}
