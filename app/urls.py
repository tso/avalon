from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('create_game', views.create_game_view, name='create_game'),
    path('join_game', views.join_game_view, name='join_game'),
    path('lobby/<uuid:game_id>/<uuid:player_id>', views.lobby_view, name='lobby'),
    path('game/<uuid:game_id>/<uuid:player_id>', views.game_view, name='game'),
    path('kick/<uuid:game_id>/<uuid:player_id>/<uuid:kicked_player_id>', views.kick_view, name='kick'),
]
