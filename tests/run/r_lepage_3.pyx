__doc__ = """
g = r_lepage_3.Grail()
g("spam", 42, ["tomato", "sandwich"])
"""

cdef class Grail:

    def __call__(self, x, y, z):
        print "Grail called with:", x, y, z
