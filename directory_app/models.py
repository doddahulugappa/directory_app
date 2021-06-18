from django.db import models
from django.utils.html import mark_safe
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
    subjects_taught = models.ManyToManyField(Subject,blank=True)


    def profile_pic(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.profile_picture.url))


    profile_pic.short_description = 'Image'
    profile_pic.allow_tags = True


    def __str__(self):
        return self.first_name




