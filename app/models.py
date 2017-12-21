from django.db import models
from django.contrib.auth.models import AbstractUser
from enumfields import Enum, EnumField
import random
import string
import uuid

class Role(Enum):
    MERLIN = 'merlin'
    PERCIVAL = 'percival'
    VANILLA_GOOD = 'vanilla_good'
    VANILLA_BAD = 'vanilla_bad'
    MORGANA = 'morgana'
    ASSASSIN = 'assassin'
    OBERON = 'oberon'


class User(AbstractUser):
    pass


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

    def start(self):
        self.is_started = True
        self.save()

    def players(self):
        return self.player_set.filter(is_kicked=False).all()

    games = GameManager()


class PlayerManager(models.Manager):
    def _create_player(self, user, game, name, is_host):
        if not game:
            raise ValueError('The game must be set')

        is_guest = user is None
        player = self.model(user=user, name=name, game=game,
                            is_guest=is_guest, is_host=is_host)
        player.save(using=self._db)
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
