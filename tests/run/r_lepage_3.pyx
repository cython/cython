__doc__ = u"""
>>> g = Grail()
>>> g("spam", 42, ["tomato", "sandwich"])
Grail called with: spam 42 ['tomato', 'sandwich']
"""

cdef class Grail:

    def __call__(self, x, y, z):
        print u"Grail called with:", x, y, z
