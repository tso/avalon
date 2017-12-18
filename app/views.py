from django.shortcuts import render, redirect
from app.models import Game, Player
import random
import operator


def index(request):
    return render(request, 'index.html')


def lobby(request, game_id, player_id):
    game = Game.objects.get(pk=game_id)
    player = Player.objects.get(pk=player_id)
    players = sorted(game.player_set.all(), key=operator.attrgetter('created_at'))
    players = [(p, p == player, p.is_host) for p in players]

    return render(request, 'lobby.html', {
        'game': game,
        'player': player,
        'players': players,
        'is_host': player.is_host,
    })


def create_game(request):
    if request.method == 'POST':
        game = Game.objects.create_game()
        player = Player.objects.create_guest_player(
            game=game, name=request.POST.get('name').title(), is_host=True)
        return redirect('lobby', game_id=game.id, player_id=player.id)

    return render(request, 'create_game.html')


def join_game(request):
    if request.method == 'POST':
        game = Game.objects.get(
            joinable_id=request.POST.get('game').upper(), started=False)
        player = Player.objects.create_guest_player(
            game=game, name=request.POST.get('name').title(), is_host=False
        )
        return redirect('lobby', game_id=game.id, player_id=player.id)

    return render(request, 'join_game.html')
