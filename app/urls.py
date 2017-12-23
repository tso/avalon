from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create_game', views.CreateGameView.as_view(), name='create_game'),
    path('join_game', views.JoinGameView.as_view(), name='join_game'),
    path('lobby/<uuid:game_id>/<uuid:player_id>', views.LobbyView.as_view(), name='lobby'),
    path('game/<uuid:game_id>/<uuid:player_id>', views.GameView.as_view(), name='game'),
    path('kick/<uuid:game_id>/<uuid:player_id>/<uuid:player_token>', views.KickView.as_view(), name='kick'),
]
