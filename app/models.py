import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

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
    def create_joinable_id(self):
        pass


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    joinable_id = models.CharField(max_length=4)
    started = models.BooleanField(default=False)

    def start(self):
        self.started = True
        self.save()

    objects = GameManager()


class PlayerManager(models.Manager):
    def _create_player(self, user, game, role):
        if not game:
            raise ValueError('The game must be set')
        if role not in ROLES:
            raise ValueError(f'The role must be one of {ROLES}')

        is_guest = user is None
        player = self.model(user=user, game=game, role=role, is_guest=is_guest)
        player.save(using=self._db)
        return player

    def create_player(self, user, game, role):
        return self._create_player(user, game, role)

    def create_guest_player(self, game, role):
        return self._create_player(None, game, role)


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLES)
    is_guest = models.BooleanField()

    objects = PlayerManager()
