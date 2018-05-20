# mode: run
# tag: pickle

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

    def __cinit__(self):
        self.x = self.y = -1

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "%s(x=%s, y=%s)" % (self.__class__.__name__, self.x, self.y)

    def __reduce__(self):
        return makeObj, (type(self), {'x': self.x, 'y': self.y})

def makeObj(obj_type, kwds):
    return obj_type(**kwds)


cdef class C(B):
    """
    >>> import pickle
    >>> pickle.loads(pickle.dumps(C(x=37, y=389)))
    C(x=37, y=389)
    """
    pass


@cython.auto_pickle(True)  # Not needed, just to test the directive.
cdef class DefaultReduce(object):
    """
    >>> a = DefaultReduce(11, 'abc'); a
    DefaultReduce(i=11, s='abc')
    >>> import pickle
    >>> pickle.loads(pickle.dumps(a))
    DefaultReduce(i=11, s='abc')
    >>> pickle.loads(pickle.dumps(DefaultReduce(i=11, s=None)))
    DefaultReduce(i=11, s=None)
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


cdef class result(DefaultReduceSubclass):
    """
    >>> a = result(i=11, s='abc', x=1.5); a
    result(i=11, s='abc', x=1.5)
    >>> import pickle
    >>> pickle.loads(pickle.dumps(a))
    result(i=11, s='abc', x=1.5)
    """

    def __repr__(self):
        return "result(i=%s, s=%r, x=%s)" % (self.i, self.s, self.x)


class DefaultReducePySubclass(DefaultReduce):
    """
    >>> a = DefaultReducePySubclass(i=11, s='abc', x=1.5); a
    DefaultReducePySubclass(i=11, s='abc', x=1.5)
    >>> import pickle
    >>> pickle.loads(pickle.dumps(a))
    DefaultReducePySubclass(i=11, s='abc', x=1.5)

    >>> a.self_reference = a
    >>> a2 = pickle.loads(pickle.dumps(a))
    >>> a2.self_reference is a2
    True
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


cdef class NoMembers(object):
    """
    >>> import pickle
    >>> pickle.loads(pickle.dumps(NoMembers()))
    NoMembers()
    """
    def __repr__(self):
        return "NoMembers()"


cdef class NoPyMembers(object):
    """
    >>> import pickle
    >>> pickle.loads(pickle.dumps(NoPyMembers(2, 1.75)))
    NoPyMembers(ii=[2, 4, 8], x=1.75)
    """
    cdef int[3] ii
    cdef double x

    def __init__(self, i, x):
        self.ii[0] = i
        self.ii[1] = i * i
        self.ii[2] = i * i * i
        self.x = x

    def __repr__(self):
        return "%s(ii=%s, x=%s)" % (type(self).__name__, self.ii, self.x)

class NoPyMembersPySubclass(NoPyMembers):
    """
    >>> import pickle
    >>> pickle.loads(pickle.dumps(NoPyMembersPySubclass(2, 1.75, 'xyz')))
    NoPyMembersPySubclass(ii=[2, 4, 8], x=1.75, s='xyz')
    """
    def __init__(self, i, x, s):
        super(NoPyMembersPySubclass, self).__init__(i, x)
        self.s = s
    def __repr__(self):
        return (super(NoPyMembersPySubclass, self).__repr__()
                [:-1] + ', s=%r)' % self.s)


cdef struct MyStruct:
    int i
    double x

cdef class StructMemberDefault(object):
    """
    >>> import pickle
    >>> s = StructMemberDefault(1, 1.5); s
    StructMemberDefault(i=1, x=1.5)
    >>> pickle.dumps(s)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...my_struct...
    """

    cdef MyStruct my_struct

    def __init__(self, i, x):
        self.my_struct.i = i
        self.my_struct.x = x

    def __repr__(self):
        return "%s(i=%s, x=%s)" % (
            type(self).__name__, self.my_struct.i, self.my_struct.x)

@cython.auto_pickle(True)  # Forced due to the (inherited) struct attribute.
cdef class StructMemberForcedPickle(StructMemberDefault):
    """
    >>> import pickle
    >>> s = StructMemberForcedPickle(1, 1.5); s
    StructMemberForcedPickle(i=1, x=1.5)
    >>> pickle.loads(pickle.dumps(s))
    StructMemberForcedPickle(i=1, x=1.5)
    """


cdef _unset = object()

# Test cyclic references.
cdef class Wrapper(object):
  """
  >>> import pickle
  >>> w = Wrapper(); w
  Wrapper(...)
  >>> w2 = pickle.loads(pickle.dumps(w)); w2
  Wrapper(...)
  >>> w2.ref is w2
  True

  >>> pickle.loads(pickle.dumps(Wrapper(DefaultReduce(1, 'xyz'))))
  Wrapper(DefaultReduce(i=1, s='xyz'))
  >>> L = [None]
  >>> L[0] = L
  >>> w = Wrapper(L)
  >>> pickle.loads(pickle.dumps(Wrapper(L)))
  Wrapper([[...]])

  >>> L[0] = w   # Don't print this one out...
  >>> w2 = pickle.loads(pickle.dumps(w))
  >>> w2.ref[0] is w2
  True
  """
  cdef public object ref
  def __init__(self, ref=_unset):
      if ref is _unset:
          self.ref = self
      else:
          self.ref = ref
  def __repr__(self):
      if self.ref is self:
          return "Wrapper(...)"
      else:
          return "Wrapper(%r)" % self.ref
