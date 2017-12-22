import json, operator
from channels import Group
from app.models import Game, Player


# Connected to websocket.connect
def ws_connect(message, game_id, player_id):
    # Accept connection
    message.reply_channel.send({"accept": True})
    Group(game_id).add(message.reply_channel)

    game = Game.games.get(pk=game_id)
    player = Player.players.get(pk=player_id)
    players = sorted(game.players(), key=operator.attrgetter('created_at'))

    Group(game_id).send({
        'text': json.dumps({
            'self': player.to_dict(),
            'game': game.to_dict(),
            'players': list(map(lambda p: p.to_dict(), players)),
        })
    })

    # Probably check that this is like, real? if it's not
    # then message.reply_channel.send({"close": True})

# Connected to websocket.receive
def ws_message(message, game_id, player_id):
    Group(game_id).send({
        'text': json.dumps({
            'message': message['text'],
            'player_id': player_id,
        }),
    })

# Connected to websocket.disconnect
def ws_disconnect(message, game_id, player_id):
    Group(game_id).discard(message.reply_channel)
