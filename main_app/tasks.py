from celery import shared_task
from directory_app.models import Subject

@shared_task(bind=True)
def test_func(self):
    print("hello Excuting the tasks ")
    for i in range(10):
        print(i)
    return "Done"

@shared_task(bind=True)
def insert_record(self):
    obj = Subject(subject_name = "DBMS")
    obj.save()

    return "Insertion Done"
