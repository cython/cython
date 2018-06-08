# cython: binding=True
# mode: run
# tag: cyfunction

cdef class TestMethodOneArg:
    def meth(self, arg):
        pass

def call_meth(x):
    """
    >>> call_meth(TestMethodOneArg())
    Traceback (most recent call last):
    ...
    TypeError: meth() takes exactly one argument (0 given)
    """
    return x.meth()
