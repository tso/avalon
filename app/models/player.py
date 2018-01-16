import uuid

from channels import Group
from django.db import models
from enumfields import EnumField

from app.avalon import Role
from .game import Game
from .user import User
from .util import lobby_json


class PlayerManager(models.Manager):
    def _create_player(self, user, game, name, is_host):
        if not game:
            raise ValueError('The game must be set')

        is_guest = user is None
        player = self.model(
            user=user,
            name=name,
            game=game,
            is_guest=is_guest,
            is_host=is_host
        )
        player.save(using=self._db)
        game.message_players()
        return player

    def create_player(self, user, game, is_host):
        return self._create_player(user, game, None, is_host)

    def create_guest_player(self, game, name, is_host):
        return self._create_player(None, game, name, is_host)


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    role = EnumField(Role, max_length=12, null=True)
    is_guest = models.BooleanField()
    is_host = models.BooleanField()
    is_kicked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    players = PlayerManager()

    def set_role(self, role):
        self.role = role
        self.save()

    def kick(self):
        self.is_kicked = True
        self.save()
        self.message_player()

    def message_player(self):
        Group(str(self.game.id) + str(self.id)).send({
            'text': lobby_json(self.game, self),
        })

    def to_dict(self, is_self=False):
        data = {
            'token': str(self.token),
            'name': self.name,
            'is_host': self.is_host,
            'is_kicked': self.is_kicked,
        }

        if is_self:
            data['id'] = str(self.id)

        return data
