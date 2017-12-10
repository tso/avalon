import uuid
from django.db import models

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

class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    role = models.CharField(
        max_length=12,
        choices=ROLES,
    )

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    joinable_id = models.CharField(max_length=4)
    players = models.ManyToManyField(Player)
