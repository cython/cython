__doc__ = """
    >>> b = Bicycle()
    >>> b.fall_off()
    Falling off extremely hard
    >>> b.fall_off("somewhat")
    Falling off somewhat hard
"""

class Bicycle:

    def fall_off(self, how_hard = "extremely"):
        print "Falling off", how_hard, "hard"
