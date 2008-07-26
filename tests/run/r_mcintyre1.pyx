__doc__ = u"""
    >>> b = Bicycle()
    >>> b.fall_off()
    Falling off extremely hard
    >>> b.fall_off("somewhat")
    Falling off somewhat hard
"""

class Bicycle:

    def fall_off(self, how_hard = u"extremely"):
        print u"Falling off", how_hard, u"hard"
