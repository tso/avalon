from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
import uuid

VANILLA_TOWN = 'VANILLA_TOWN'
MERLIN = 'MERLIN'
PERCIVAL = 'PERCIVAL'
MORGANA = 'MORGANA'
ASSASSIN = 'ASSASSIN'
VANILA_BAD = 'VANILLA_BAD'
OBERON = 'OBERON'

ROLES = (
    (VANILLA_TOWN, 'Vanilla Town'),
    (MERLIN, 'Merlin'),
    (PERCIVAL, 'Percival'),
    (MORGANA, 'Morgana'),
    (ASSASSIN, 'Assassin'),
    (VANILA_BAD, 'Vanilla Bad'),
    (OBERON, 'Oberon'),
)


class User(AbstractUser):
    pass


class GameManager(models.Manager):
    def create_game(self):
        game = self.model(joinable_id=''.join(
            random.choices(string.ascii_uppercase, k=4)))
        game.save(using=self._db)
        return game


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    joinable_id = models.CharField(max_length=4)
    started = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def start(self):
        self.started = True
        self.save()

    objects = GameManager()


class PlayerManager(models.Manager):
    def _create_player(self, user, game, name):
        if not game:
            raise ValueError('The game must be set')

        is_guest = user is None
        player = self.model(user=user, name=name, game=game, is_guest=is_guest)
        player.save(using=self._db)
        return player

    def create_player(self, user, game):
        return self._create_player(user, game, None)

    def create_guest_player(self, game, name):
        return self._create_player(None, game, name)


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLES)
    is_guest = models.BooleanField()

    objects = PlayerManager()

    def set_role(self, role):
        if role not in ROLES:
            raise ValueError('Role must be valid')
        self.role = role
        self.save()
