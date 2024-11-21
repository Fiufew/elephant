# ElephantRent/your_app_name/celery_beat_schedule.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-rental-expiration-notification': {
        'task': 'backend.tasks.check_rental_expiration',
        'schedule': crontab(minute='*/1'),  # Каждые 2 минут
    },
}
