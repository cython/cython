__doc__ = """
    >>> s = Spam()
    >>> print s.__class__.__name__
    Spam

    >>> s = SpamT()
    >>> print type(s).__name__
    SpamT
"""

class Spam: pass

class SpamT(object): pass
