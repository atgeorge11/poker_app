"""Defines url patterns for the game app"""

from django.urls import path
from . import views

app_name = "game"
urlpatterns = [
    path('create/', views.create, name="create"),
    path('join/', views.join, name="join"),
    path('gameroom/<str:game_name>/', views.gameroom, name="gameroom")
]