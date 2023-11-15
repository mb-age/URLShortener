from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webhelpers.settings')

app = Celery('webhelpers')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-expired-links': {
        'task': 'urlshortener.tasks.delete_expired_links',
        'schedule': crontab(hour=0, minute=0),  # daily at midnight
    },
}
