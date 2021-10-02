from django.shortcuts import render, HttpResponse
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from .tasks import test_func

# Create your views here.

def test(request):
    test_func.delay()
    return HttpResponse("Done")

def run_program_on_schedule(request):
    schedule, created =  CrontabSchedule.objects.get_or_create(hour=10, minute=17)
    task = PeriodicTask.objects.create(crontab=schedule,name="add subject-2",task='main_app.tasks.insert_record')
    return HttpResponse("Program Ran")
