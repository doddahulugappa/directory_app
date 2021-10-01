from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','directory_app.settings')

app = Celery('directory_app')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Dubai')

app.config_from_object(settings,namespace='CELERY')

app.autodiscover_tasks()

#Celery Beat Settings
app.conf.beat_schedule = {
'test_run':{
    'task':'main_app.tasks.test_func',
    'schedule':crontab(hour=21,minute=56,day_of_month=1,month_of_year=10)
}

}


@app.task(bind=True)
def debug_task(self):
    print('Request: ',self.request)