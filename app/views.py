from django.shortcuts import render, redirect
from app.models import Game, Player
import random


def index(request):
    return render(request, 'index.html')


def lobby(request, game_id, player_id):
    game = Game.objects.get(pk=game_id)
    player = Player.objects.get(pk=player_id)
    players = game.player_set.all()

    return render(request, 'lobby.html', {
        'game': game,
        'player': player,
        'players': players,
    })


def create_game(request):
    if request.method == 'POST':
        game = Game.objects.create_game()
        player = Player.objects.create_guest_player(
            game=game, name=request.POST.get('name'))
        return redirect('lobby', game_id=game.id, player_id=player.id)

    return render(request, 'create_game.html')


def join_game(request):
    if request.method == 'POST':
        game = Game.objects.get(
            joinable_id=request.POST.get('game'), started=False)
        player = Player.objects.create_guest_player(
            game=game, name=request.POST.get('name')
        )
        return redirect('lobby', game_id=game.id, player_id=player.id)

    return render(request, 'join_game.html')
