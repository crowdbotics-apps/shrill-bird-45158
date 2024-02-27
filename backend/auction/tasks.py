# tasks.py (within your Django app)
from celery import shared_task
from celery.schedules import crontab
from datetime import timedelta
from auction.management.commands.auction_management import Command

@shared_task
def automate_auction():
    command = Command()
    command.handle()

CELERY_BEAT_SCHEDULE = {
    'automate-auction': {
        'task': 'auction.tasks.automate_auction',
        'schedule': timedelta(seconds=1),  # Adjust as needed
    },
}
