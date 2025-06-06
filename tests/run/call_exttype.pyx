# mode: run

from cython cimport typeof

cdef class ExtType:
    def __call__(self):
        return self


def call_exttype():
    """
    >>> call_exttype()
    """
    x = ExtType()
    assert typeof(x) == 'ExtType', typeof(x)
    assert x() is x

    a = ExtType()()
    assert typeof(a) == 'Python object', typeof(a)
    assert type(a) is ExtType
    assert a is not x
