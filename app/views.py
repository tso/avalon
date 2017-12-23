from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from app.avalon import players_seen
from app.models import Game, Player, lobby_json


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class LobbyView(View):
    template_name = 'lobby.html'

    def get(self, request, game_id, player_id):
        game = Game.games.get(pk=game_id)
        player = Player.players.get(pk=player_id)

        if player.is_kicked:
            messages.add_message(request, messages.ERROR, "You've been kicked")
            return redirect('index')

        return render(request, self.template_name, {
            'game': game,
            'self': player,
            'json': lobby_json(game, player),
        })


class KickView(View):
    def get(self, request, game_id, player_id, player_token):
        game = Game.games.get(pk=game_id)
        player = Player.players.get(pk=player_id)
        kicked_player = Player.players.get(token=player_token)

        if game.is_started:
            messages.add_message(request, messages.ERROR, "Cannot kick a player once the game has started")
            return redirect('lobby', game_id=game_id, player_id=player_id)

        if not player.is_host:
            messages.add_message(request, messages.ERROR, "Only the host can kick players")
            return redirect('lobby', game_id=game_id, player_id=player_id)

        kicked_player.kick()
        return redirect('lobby', game_id=game_id, player_id=player_id)


class GameView(View):
    template_name = 'game.html'

    def post(self, request, game_id, player_id):
        game = Game.games.get(pk=game_id)
        player = Player.players.get(pk=player_id)

        if not player.is_host:
            messages.add_message(request, messages.ERROR, 'Only the host can start the game')
            return redirect('lobby', game_id=game_id, player_id=player_id)

        game.start()
        return redirect('game', game_id=game_id, player_id=player_id)

    def get(self, request, game_id, player_id):
        game = Game.games.get(pk=game_id)
        player = Player.players.get(pk=player_id)

        print(players_seen(game, player))

        return render(request, self.template_name, {
            'game': game,
            'self': player,
            'seen': players_seen(game, player),
        })


class CreateGameView(View):
    template_name = 'create_game.html'

    def post(self, request):
        name = request.POST.get('name')
        if not name:
            messages.add_message(request, messages.ERROR, 'Name cannot be blank')
            return redirect('create_game')

        game = Game.games.create_game(
            request.POST.get('has_mordred', 'off') == 'on',
            request.POST.get('has_oberon', 'off') == 'on',
        )
        player = Player.players.create_guest_player(
            game=game,
            name=name.title(),
            is_host=True,
        )

        return redirect('lobby', game_id=game.id, player_id=player.id)

    def get(self, request):
        return render(request, self.template_name)


class JoinGameView(View):
    template_name = 'join_game.html'

    def post(self, request):
        name = request.POST.get('name')
        if not name:
            messages.add_message(request, messages.ERROR, 'Name cannot be blank')
            return redirect('join_game')

        try:
            game = Game.games.get(
                joinable_id=request.POST.get('joinable_id').upper(),
                is_started=False
            )
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Could not find that game')
            return redirect('join_game')

        player = Player.players.create_guest_player(
            game=game,
            name=name.title(),
            is_host=False,
        )

        return redirect('lobby', game_id=game.id, player_id=player.id)

    def get(self, request):
        return render(request, self.template_name)
