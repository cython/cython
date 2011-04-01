# mode: compile

__doc__ = u"""
    >>> s = Swallow()
    >>> s.spam(1)
    1 42 'grail' True
    >>> s.spam(1, 2)
    1 2 'grail' True
    >>> s.spam(1, z = 2)
    1 42 'grail' 2
    >>> s.spam(1, y = 2)
    1 42 2 True
    >>> s.spam(1, x = 2, y = 'test')
    1 2 'test' True
"""

swallow = True

class Swallow:

    def spam(w, int x = 42, y = "grail", z = swallow):
        print w, x, y, z
