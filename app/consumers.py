from channels import Group
from channels.auth import http_session_user
from channels.security.websockets import allowed_hosts_only


# Connected to websocket.connect
@allowed_hosts_only
@http_session_user
def ws_connect(message, game_id, player_id):
    # Accept connection
    message.reply_channel.send({"accept": True})
    Group(game_id).add(message.reply_channel)
    Group(game_id + player_id).add(message.reply_channel)

    # Probably check that this is like, real? if it's not
    # then message.reply_channel.send({"close": True})


# Connected to websocket.disconnect
def ws_disconnect(message, game_id, player_id):
    Group(game_id).discard(message.reply_channel)
    Group(game_id + player_id).discard(message.reply_channel)
