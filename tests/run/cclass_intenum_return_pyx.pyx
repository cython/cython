# mode: run
# tag: pure3, enum

"""
Test for regression: @cclass IntEnum with return type annotation - attribute without type annotation.
"""

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
    # Note: _winner_team has NO type annotation here
    # This might cause the compiler to infer it as object

    def __init__(self):
        self._winner_team = Team.NONE

    def winner_team(self) -> Team:
        """
        >>> v = VersusLevel()
        >>> v.winner_team()
        <Team.NONE: 1>
        """
        return self._winner_team


def test_intenum_return():
    """
    Test that returning an IntEnum value from a method with return type annotation works.

    >>> test_intenum_return()
    <Team.NONE: 1>
    """
    v = VersusLevel()
    result = v.winner_team()
    assert result is Team.NONE, result
    print(repr(result))
