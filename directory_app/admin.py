from django.contrib import admin

from .models import Teacher, Subject
from django.shortcuts import render


class TeacherAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'email_address','profile_picture')
    list_filter = ('first_name','last_name','subject__subject_name')
    # readonly_fields = [field.name for field in Teacher._meta.fields]

    # def changelist_view(self, request):
    #     context = {'title': 'My Custom AdminForm'}
    #
    #     return render(request, 'admin/change_form.html', context)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'teacher_id')
    # readonly_fields = [field.name for field in Subject._meta.fields]


admin.site.register(Teacher, TeacherAdmin)

admin.site.register(Subject, SubjectAdmin)

admin.site.site_header = 'Directory App Administration'


