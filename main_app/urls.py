"""
directory_app URL Configuration

"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.test,name='test'),
    path('/add-subject/', views.run_program_on_schedule,name='run_program'),
]