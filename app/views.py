import string
import random
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html')


def create_game(request):
    return render(request, 'create_game.html')


def join_game(request):
    return render(request, 'join_game.html')


def lobby(request, game, name):
    return render(request, 'lobby.html', {'game': game, 'name': name})
