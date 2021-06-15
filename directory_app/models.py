from django.db import models
from django.core.exceptions import ValidationError

class Subject(models.Model):
    subject_name = models.CharField(max_length=50, blank=False,null=False,default=None)
    def __str__(self):
        return self.subject_name

class Teacher(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    profile_picture = models.ImageField(blank=True, null=True)
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12,null = True)
    room_number = models.CharField(max_length=12,null = True)
    subjects_taught = models.ManyToManyField(Subject)

    def __str__(self):
        return self.email_address

    def clean(self, *args, **kwargs):
        if self.subjects_taught.count() > 5:
            raise ValidationError("You can't assign more than 5 subjects")
        super(Teacher, self).clean(*args, **kwargs)

