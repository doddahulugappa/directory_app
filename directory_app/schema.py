from graphene_django import DjangoObjectType
import graphene
from .models import Teacher, Subject




class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher

class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject

class Query(graphene.ObjectType):
    teachers = graphene.List(TeacherType)
    subjects = graphene.List(SubjectType)


    @graphene.resolve_only_args
    def resolve_teachers(self):
        return Teacher.objects.all()

    # @graphene.resolve_only_args
    #alternate way of resolving query with(root,info) without decorater
    def resolve_subjects(root, info):
        return Subject.objects.all()






schema = graphene.Schema(query=Query)