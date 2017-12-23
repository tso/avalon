from enumfields import Enum


class Role(Enum):
    MERLIN = 'merlin'
    PERCIVAL = 'percival'
    VANILLA_GOOD = 'vanilla_good'
    VANILLA_BAD = 'vanilla_bad'
    MORGANA = 'morgana'
    ASSASSIN = 'assassin'
    OBERON = 'oberon'

TOTAL_BAD = {
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 3,
    10: 4,
}

DEFAULTS = {
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
}


def players_seen(game, player):
    '''
    Players seen takes in a game and a player whose role has been
    decided and returns a list of players who they "saw" during
    nightphase.
    '''
    pass


def assign_roles(game):
    '''
    Assign roles takes in a game and using game.roles assigns each
    player randomly a role.
    '''
    pass
