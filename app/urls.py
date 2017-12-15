from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_game', views.create_game, name='create_game'),
    path('join_game', views.join_game, name='join_game'),
    path('lobby/<uuid:game_id>/<uuid:player_id>', views.lobby, name='lobby'),
]
