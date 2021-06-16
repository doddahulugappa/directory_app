from django.contrib import admin

from .models import Teacher, Subject
from import_export.admin import ImportExportModelAdmin

from django.core.exceptions import ValidationError
from django import forms


class TeacherForm(forms.ModelForm):
    model = Teacher

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('subjects_taught').count() > 5:
            raise ValidationError('You can only choose upto 5 subjects!')





class TeacherAdmin(ImportExportModelAdmin):
    form = TeacherForm
    list_display = ('first_name', 'last_name', 'email_address','profile_picture',)


    list_filter = ('first_name','last_name',)

    filter_horizontal = ['subjects_taught']


class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('subject_name',)


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher, TeacherAdmin)



admin.site.site_header = 'Directory App Administration'
admin.site.site_title = 'Teacher\'s Site Administration'
admin.site.index_title = 'Teacher\'s Site Admin'


