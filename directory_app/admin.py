from django.contrib import admin

from .models import Teacher, Subject
from import_export.admin import ImportExportModelAdmin

from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import escape


class TeacherForm(forms.ModelForm):
    model = Teacher

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('subjects_taught').count() > 5:
            raise ValidationError('You can only choose upto 5 subjects!')





class TeacherAdmin(ImportExportModelAdmin):
    save_on_top = True
    save_as = True
    form = TeacherForm
    list_display = ('first_name', 'last_name', 'email_address','subject_list','profile_picture')
    list_display_links = ('first_name', 'last_name','email_address')
    # readonly_fields = ('profile_picture',)


    list_filter = ('first_name','last_name','subjects_taught')

    filter_horizontal = ['subjects_taught']
    # filter_vertical = ['subjects_taught']

    def subject_list(self,obj):
        subject_list = ", ".join([x.subject_name for x in obj.subjects_taught.all()])
        return mark_safe(subject_list)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "subjects_taught":
            kwargs["queryset"] = Subject.objects.all()
        return super(TeacherAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)



    # change_form_template = 'admin/change_form.html'

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     return super(TeacherAdmin, self).change_view(
    #         request, object_id, form_url, extra_context=extra_context,
    #     )

class SubjectAdmin(ImportExportModelAdmin):
    list_display = ['subject_name']


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher, TeacherAdmin)



admin.site.site_header = 'Directory App Administration'
admin.site.site_title = 'Teacher\'s Site Administration'
admin.site.index_title = 'Teacher\'s Site Admin'


