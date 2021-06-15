from django.contrib import admin

from .models import Teacher, Subject
from import_export.admin import ImportExportModelAdmin


class TeacherAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address','profile_picture',)


    list_filter = ('first_name','last_name',)

    filter_horizontal = ['subjects_taught']


class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('subject_name',)


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher, TeacherAdmin)



admin.site.site_header = 'Directory App Administration'
# admin.site.index = 'Directory App Administration'


