from django.db import models
from django.core.exceptions import ValidationError
from .settings import MEDIA_URL


class Teacher(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    profile_picture = models.ImageField(upload_to=MEDIA_URL,blank=True, null=True)
    email_address = models.EmailField(max_length=100, blank=False,unique=True)
    phone_number = models.CharField(max_length=12,null = True)

    def __str__(self):
        return self.email_address


def restrict_number_of_subjects(value):
    if Subject.objects.filter(teacher_id=value).count() >= 5:
        raise ValidationError('Teacher can teach maximum (5) subjects')

class Subject(models.Model):
    subject_name = models.CharField(max_length=100, blank=False)
    teacher_id = models.ForeignKey(Teacher,on_delete=models.CASCADE, validators=(restrict_number_of_subjects,))

