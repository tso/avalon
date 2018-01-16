from channels.routing import route

from app.consumers import ws_connect, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/lobby/(?P<game_id>[0-9a-f-]+)/(?P<player_id>[0-9a-f-]+)/$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/lobby/(?P<game_id>[0-9a-f-]+)/(?P<player_id>[0-9a-f-]+)/$"),
]
