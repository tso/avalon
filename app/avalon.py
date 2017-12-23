from enumfields import Enum
from random import shuffle


class Role(Enum):
    # Good
    MERLIN = 'merlin'
    PERCIVAL = 'percival'
    VANILLA_GOOD = 'vanilla_good'
    # Bad
    VANILLA_BAD = 'vanilla_bad'
    MORGANA = 'morgana'
    ASSASSIN = 'assassin'
    MORDRED = 'mordred'
    OBERON = 'oberon'


VISIBLE_BAD = [Role.VANILLA_BAD, Role.MORGANA, Role.ASSASSIN, Role.OBERON]
NOT_OBERON = [Role.VANILLA_BAD, Role.MORGANA, Role.ASSASSIN, Role.MORDRED]

# A Role sees ROLE_MECHANICS[Role] in nightphase.
ROLE_MECHANICS = {
    Role.MERLIN: VISIBLE_BAD,
    Role.PERCIVAL: [Role.MERLIN, Role.MORGANA],
    Role.VANILLA_GOOD: [],
    Role.VANILLA_BAD: NOT_OBERON,
    Role.MORGANA: NOT_OBERON,
    Role.ASSASSIN: NOT_OBERON,
    Role.MORDRED: NOT_OBERON,
    Role.OBERON: [],
}

TOTAL_BAD = {
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 3,
    10: 4,
}

DEFAULTS = {
    5: [Role.MERLIN, Role.PERCIVAL, Role.VANILLA_GOOD, Role.MORGANA, Role.ASSASSIN],
    6: [Role.MERLIN, Role.PERCIVAL],
    7: [Role.MERLIN, Role.PERCIVAL],
    8: [Role.MERLIN, Role.PERCIVAL],
    9: [Role.MERLIN, Role.PERCIVAL],
    10: [Role.MERLIN, Role.PERCIVAL],
}


def players_seen(game, player):
    '''
    Players seen takes in a game and a player whose role has been
    decided and returns a list of players who they "saw" during
    nightphase.
    '''
    players = game.players()
    roles_seen = ROLE_MECHANICS[player.role]
    other_players_seen = []
    for p in players:
        if p.role in roles_seen and p != player:
            other_players_seen.append(p)
    return other_players_seen


def assign_roles(game):
    '''
    Assign roles takes in a game and using game.roles assigns each
    player randomly a role.
    '''
    players = game.players()
    roles = DEFAULTS[len(players)]
    shuffle(roles)
    for player, role in zip(players, roles):
        player.set_role(role)
