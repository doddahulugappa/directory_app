from import_export import resources
from .models import Subject, Teacher

class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject


class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher