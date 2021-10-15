from django.db import models
from django.utils.html import mark_safe
class Subject(models.Model):
    subject_name = models.CharField(max_length=50, blank=False,null=False,default=None)
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

    # def profile_picture_tag(self):
    #     if self.profile_picture:
    #         return mark_safe('<img src="%s" style="width: 75px; height:75px;" />' % self.profile_picture.url)
    #     else:
    #         return 'No Image Found'
    #
    # profile_picture_tag.allow_tags = True
    # profile_picture_tag.short_description = 'ProfilePic'

    def __str__(self):
        return self.first_name






