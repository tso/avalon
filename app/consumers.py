from channels import Group
from app.models import Game, Player
from app.views import lobby_json


# Connected to websocket.connect
def ws_connect(message, game_id, player_id):
    # Accept connection
    message.reply_channel.send({"accept": True})
    Group(game_id).add(message.reply_channel)
    Group(game_id + player_id).add(message.reply_channel)

    game = Game.games.get(pk=game_id)
    player = Player.players.get(pk=player_id)
    Group(game_id).send({
        'text': lobby_json(game, player, include_self=False)
    })

    # Probably check that this is like, real? if it's not
    # then message.reply_channel.send({"close": True})


# Connected to websocket.disconnect
def ws_disconnect(message, game_id, player_id):
    Group(game_id).discard(message.reply_channel)
    Group(game_id + player_id).discard(message.reply_channel)
