import cython
import sys

if sys.version_info[0] < 3:
    __doc__ = """
    >>> import cPickle
    >>> a = A(5); a
    A(5)
    >>> cPickle.loads(cPickle.dumps(a))
    A(5)

    >>> b = B(0, 1); b
    B(x=0, y=1)
    >>> cPickle.loads(cPickle.dumps(b))
    B(x=0, y=1)
    """

cdef class A:
    """
    >>> a = A(3); a
    A(3)
    >>> import pickle
    >>> pickle.loads(pickle.dumps(a))
    A(3)
    """

    cdef int value

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "A(%s)" % self.value

    def __reduce__(self):
        return A, (self.value,)

cdef class B:
    """
    >>> b = B(x=37, y=389); b
    B(x=37, y=389)
    >>> import pickle
    >>> pickle.loads(pickle.dumps(b))
    B(x=37, y=389)
    """

    cdef int x, y

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "B(x=%s, y=%s)" % (self.x, self.y)

    def __reduce__(self):
        return makeB, ({'x': self.x, 'y': self.y},)

def makeB(kwds):
    return B(**kwds)


@cython.auto_pickle(True)  # Not needed, just to test the directive.
cdef class DefaultReduce(object):
    """
    >>> a = DefaultReduce(11, 'abc'); a
    DefaultReduce(i=11, s='abc')
    >>> import pickle
    >>> pickle.loads(pickle.dumps(a))
    DefaultReduce(i=11, s='abc')
    """

    cdef readonly int i
    cdef readonly str s

    def __init__(self, i=0, s=None):
        self.i = i
        self.s = s

    def __repr__(self):
        return "DefaultReduce(i=%s, s=%r)" % (self.i, self.s)


cdef class DefaultReduceSubclass(DefaultReduce):
    """
    >>> a = DefaultReduceSubclass(i=11, s='abc', x=1.5); a
    DefaultReduceSubclass(i=11, s='abc', x=1.5)
    >>> import pickle
    >>> pickle.loads(pickle.dumps(a))
    DefaultReduceSubclass(i=11, s='abc', x=1.5)
    """

    cdef double x

    def __init__(self, **kwargs):
        self.x = kwargs.pop('x', 0)
        super(DefaultReduceSubclass, self).__init__(**kwargs)

    def __repr__(self):
        return "DefaultReduceSubclass(i=%s, s=%r, x=%s)" % (self.i, self.s, self.x)


class DefaultReducePySubclass(DefaultReduce):
    """
    >>> a = DefaultReducePySubclass(i=11, s='abc', x=1.5); a
    DefaultReducePySubclass(i=11, s='abc', x=1.5)
    >>> import pickle
    >>> pickle.loads(pickle.dumps(a))
    DefaultReducePySubclass(i=11, s='abc', x=1.5)
    """
    def __init__(self, **kwargs):
        self.x = kwargs.pop('x', 0)
        super(DefaultReducePySubclass, self).__init__(**kwargs)

    def __repr__(self):
        return "DefaultReducePySubclass(i=%s, s=%r, x=%s)" % (self.i, self.s, self.x)


cdef class NoReduceDueToIntPtr(object):
    """
    >>> import pickle
    >>> pickle.dumps(NoReduceDueToIntPtr())
    Traceback (most recent call last):
    ...
    TypeError: self.int_ptr cannot be converted to a Python object for pickling
    """
    cdef int* int_ptr

cdef class NoReduceDueToNontrivialCInit(object):
    """
    >>> import pickle
    >>> pickle.dumps(NoReduceDueToNontrivialCInit(None))
    Traceback (most recent call last):
    ...
    TypeError: no default __reduce__ due to non-trivial __cinit__
    """
    def __cinit__(self, arg):
        pass
