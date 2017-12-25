import json

def lobby_json(game, player=None):
    data = {
        'game': game.to_dict(),
        'players': list(map(lambda p: p.to_dict(), game.players())),
    }

    if player:
        data['self'] = player.to_dict(is_self=True)

    return json.dumps(data)
