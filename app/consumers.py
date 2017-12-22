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
    players = [{'name': p.name, 'token': str(p.token), 'is_host': p.is_host} for p in players]

    Group(game_id).send({
        'text': json.dumps({
            'self': {
                'is_host': player.is_host,
                'token': str(player.token),
            },
            'game': {
                'joinable_id': game.joinable_id,
                'is_started': False,
                'roles': 'Oberon',
            },
            'players': players,
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
