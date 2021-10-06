from graphene_django import DjangoObjectType
import graphene
from .models import UserModel, Teacher, Subject


class User(DjangoObjectType):
    class Meta:
        model = UserModel

class Mentor(DjangoObjectType):
    class Meta:
        model = Teacher

class Topic(DjangoObjectType):
    class Meta:
        model = Subject

class Query(graphene.ObjectType):
    users = graphene.List(User)
    mentors = graphene.List(Mentor)
    subjects = graphene.List(Topic)

    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()

    @graphene.resolve_only_args
    def resolve_mentors(self):
        return Teacher.objects.all()

    # @graphene.resolve_only_args
    #alternate way of resolving query with(root,info) without decorater
    def resolve_subjects(root, info):
        return Subject.objects.all()






schema = graphene.Schema(query=Query)