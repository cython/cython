# cython: auto_cpdef=True

from enum import IntEnum

from cython import cclass


@cclass
class Team(IntEnum):
    """
    Enumeration representing the selected team.
    """

    RED = 0
    NONE = 1
    BLUE = 2


class VersusLevel:
    _winner_team: Team

    def __init__(self):
        self._winner_team = Team.NONE

    def winner_team(self) -> Team:
        return self._winner_team


def test_intenum_return():
    v = VersusLevel()
    result = v.winner_team()
    assert result is Team.NONE, result
    print(repr(result))
