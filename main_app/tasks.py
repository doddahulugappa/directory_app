from celery import shared_task
from directory_app.models import Subject

@shared_task(bind=True)
def test_func(self):
    print("hello Excuting the tasks ")
    for i in range(10):
        print(i)
    return "Done"

