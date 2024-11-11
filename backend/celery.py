# ElephantRent/ElephantRent/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ElephantRent.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# в папке на одну директорию выше с файлом celery.py: celery -A backend.celery worker --loglevel=INFO
# в папке на одну директорию выше с файлом celery.py: celery -A backend.celery beat --loglevel=info
# в общем и целом создаем файл celery.py с основными настройками celery, создаем файл tasks.py куда загружем наши задачи. и запускаем worker и beat
# чтобы было расписание создаем файл celery_beat_schedule.py и в нем прописываем параметры рассписания, импортируем их в settings.py
