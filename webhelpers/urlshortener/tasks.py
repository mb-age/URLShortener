from datetime import datetime, timedelta

from celery import shared_task

from urlshortener.models import LinkPair
from webhelpers.settings import STORAGE_TIME


@shared_task
def delete_expired_links():
    # Define the expiration threshold (e.g., links older than 7 days)
    expiration_dt = datetime.now() - timedelta(days=STORAGE_TIME)
    LinkPair.objects.filter(created_at__lt=expiration_dt).delete()
