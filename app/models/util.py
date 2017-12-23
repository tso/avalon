import json
import operator

def lobby_json(game, player=None):
    players = sorted(game.players(), key=operator.attrgetter('created_at'))
    data = {
        'game': game.to_dict(),
        'players': list(map(lambda p: p.to_dict(), players)),
    }

    if player:
        data['self'] = player.to_dict(is_self=True)

    return json.dumps(data)
