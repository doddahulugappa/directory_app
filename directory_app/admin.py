from django.contrib import admin

from .models import Teacher, Subject
from import_export.admin import ImportExportModelAdmin

from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import escape, format_html


class TeacherForm(forms.ModelForm):
    model = Teacher

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('subjects_taught').count() > 5:
            raise ValidationError('You can only choose upto 5 subjects!')





class TeacherAdmin(ImportExportModelAdmin):
    readonly_fields = ('profile_picture_tag',)
    form = TeacherForm
    list_display = ('first_name', 'last_name', 'email_address','subject_list','profile_picture_tag')
    list_display_links = ('first_name', 'last_name','email_address')


    list_filter = ('first_name','last_name','subjects_taught')

    filter_horizontal = ['subjects_taught']

    def profile_picture_tag(self,obj):
        if obj.profile_picture:
            return mark_safe('<img src="%s" style="width: 75px; height:75px;" />' % obj.profile_picture.url)
        else:
            return 'No Image Found'

    profile_picture_tag.allow_tags = True
    profile_picture_tag.short_description = 'ProfilePic'

    def subject_list(self,obj):
        """
        comma based values in list display
        """
        subject_list = ", ".join([self.create_link(x) for x in obj.subjects_taught.all()])
        return mark_safe(subject_list)

    def create_link(self,obj):
        link = reverse("admin:directory_app_subject_change",args=[obj.id])
        return format_html('<a href="{}">{}</a>',link,obj.subject_name)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        filter subject from manytomany field
        """
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
admin.site.site_url = "/"


