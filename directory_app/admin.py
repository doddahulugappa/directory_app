from django.contrib import admin

from .models import Teacher, Subject
from import_export.admin import ImportExportModelAdmin

from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe


class TeacherForm(forms.ModelForm):
    model = Teacher

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('subjects_taught').count() > 5:
            raise ValidationError('You can only choose upto 5 subjects!')





class TeacherAdmin(ImportExportModelAdmin):
    form = TeacherForm
    # raw_id_fields = ['subjects_taught']
    list_display = ('first_name', 'last_name', 'email_address','profile_picture','subject_list')


    list_filter = ('first_name','last_name','subjects_taught')

    filter_horizontal = ['subjects_taught']

    def subject_list(self,obj):
        subject_list = ", ".join([x.subject_name for x in obj.subjects_taught.all()])
        return mark_safe(subject_list)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "subjects_taught":
            kwargs["queryset"] = Subject.objects.all()
        return super(TeacherAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class SubjectAdmin(ImportExportModelAdmin):
    list_display = ['subject_name']


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher, TeacherAdmin)



admin.site.site_header = 'Directory App Administration'
admin.site.site_title = 'Teacher\'s Site Administration'
admin.site.index_title = 'Teacher\'s Site Admin'


