"""
directory_app URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('add-teacher/', views.add_teacher, name="add_teacher"),
    path('del-teacher/<int:id>/', views.delete_teacher, name="delete_teacher"),
    path('edit-teacher/<int:id>/', views.edit_teacher, name="edit_teacher"),
    path('subjects/', views.subject_list, name="subject_list"),
    path('add-subject/', views.add_subject, name="add_subject"),
    path('del-subject/<int:id>/', views.delete_subject, name="delete_subject"),
    path('edit-subject/<int:id>/', views.edit_subject, name="edit_subject"),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('user', views.UserView.as_view()),
]
