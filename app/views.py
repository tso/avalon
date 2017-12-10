import string
import random
from django.shortcuts import render, redirect


games = set()

def index(request):
    return render(request, 'index.html')


def create_game(request):
    # games.add(game_id)
    # request.session['game'] = game_id
    # request.session['name'] = request.POST.get('name')
    return render(request, 'create_game.html')


def join_game(request):
    return render(request, 'join_game.html')


def lobby(request, game_id):
    return render(request, 'lobby.html', { 'game': game_id })
