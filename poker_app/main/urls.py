"""Defines URL patterns for main interface"""

from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    #Home page
    path('', views.index, name='index'),

    #Login page
    path('log_in/', views.log_in, name="log_in"),

    #Logout page
    path('log_out/', views.log_out, name="log_out"),

    #Registration page
    path('register/', views.register, name="register"),
]