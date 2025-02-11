# ticket: t494

cimport cython

class SomeNumber(object):

    def __init__(self, n):
        self._n = n

    def __repr__(self):
        return "SomeNumber(%s)" % self._n

@cython.binding(True)
def add_to_func(self, x):
    """
    >>> add_to_func(SomeNumber(2), 5)
    7
    >>> SomeNumber(3).add_to(10)
    13
    >>> SomeNumber.add_to(SomeNumber(22), 7)
    29
    """
    return self._n + x

@cython.binding(False)
def new_num(n):
    """
    >>> new_num(11)
    SomeNumber(11)
    >>> SomeNumber.new(11)
    SomeNumber(11)
    >>> SomeNumber(3).new(11)
    SomeNumber(11)
    """
    return SomeNumber(n)

SomeNumber.add_to = add_to_func
SomeNumber.new = new_num
