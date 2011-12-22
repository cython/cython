# mode: run
# ticket: 674

cdef class Foo:
    cdef str name

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<%s>' % self.name

def test_exttype_args(a, b, c):
    """
    >>> f1 = test_exttype_args([1, 2, 3], 123, Foo('Foo'))
    >>> f2 = test_exttype_args([0], 0, Foo('Bar'))
    >>> f1()
    ([1, 2, 3], 123, <Foo>)
    >>> f2()
    ([0], 0, <Bar>)
    """
    def inner(a=a, int b=b, Foo c=c):
        return a, b, c
    return inner
