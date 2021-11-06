from django.db import models
class Subject(models.Model):
    subject_name = models.CharField(max_length=50, blank=False,null=False,unique=True)
    def __str__(self):
        return self.subject_name


class Teacher(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    profile_picture = models.ImageField(blank=True, default="default.png")
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12,null = True)
    room_number = models.CharField(max_length=12,null = True)
    subjects_taught = models.ManyToManyField(Subject,blank=True)

    def __str__(self):
        return self.first_name






