from channels import Group
from channels.auth import http_session_user
from channels.security.websockets import allowed_hosts_only
from django.core.exceptions import ObjectDoesNotExist

from app.models import Game, Player


@allowed_hosts_only
@http_session_user
def ws_connect(message, game_id, player_id):
    try:
        game = Game.games.get(pk=game_id)
        Player.players.get(pk=player_id)
    except ObjectDoesNotExist:
        message.reply_channel.send({"close": True})
        return

    message.reply_channel.send({"accept": True})
    Group(game_id).add(message.reply_channel)
    Group(game_id + player_id).add(message.reply_channel)

    game.message_players()


def ws_disconnect(message, game_id, player_id):
    Group(game_id).discard(message.reply_channel)
    Group(game_id + player_id).discard(message.reply_channel)
