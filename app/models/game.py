import random
import string
import uuid
from app.consumers import message_game
from django.db import models
from .util import lobby_json


class GameManager(models.Manager):
    def create_game(self, has_mordred, has_oberon):
        joinable_id = ''.join(random.choices(string.ascii_uppercase, k=4))
        # For the set of all unstarted games joinable ID must be unique
        while self.filter(is_started=False, joinable_id=joinable_id):
            joinable_id = ''.join(random.choices(string.ascii_uppercase, k=4))

        game = self.model(joinable_id=joinable_id,
                          has_mordred=has_mordred, has_oberon=has_oberon)
        game.save(using=self._db)
        return game


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    joinable_id = models.CharField(max_length=4)
    is_started = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    has_mordred = models.BooleanField(default=False)
    has_oberon = models.BooleanField(default=False)

    games = GameManager()

    def start(self):
        self.is_started = True
        self.save()
        message_game(self, lobby_json(self))

    def players(self):
        return self.player_set.filter(is_kicked=False).all()

    def to_dict(self):
        return {
            'id': str(self.id),
            'joinable_id': self.joinable_id,
            'is_started': self.is_started,
            'has_mordred': self.has_mordred,
            'has_oberon': self.has_oberon,
        }

