#cython: language_level=2
# mode: run
# ticket: 653

cdef class MyDict(dict):
    def test_items(self):
        """
        >>> MyDict(a=1, b=2).test_items()
        [('a', 1), ('b', 2)]
        """
        l = [ (key, value) for key, value in self.items() ]
        l.sort()
        return l

    def test_iteritems(self):
        """
        >>> MyDict(a=1, b=2).test_iteritems()
        [('a', 1), ('b', 2)]
        """
        l = [ (key, value) for key, value in self.iteritems() ]
        l.sort()
        return l
