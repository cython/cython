# mode: run
# tag: exttype, tpnew

from __future__ import print_function

from cpython.object cimport PyTypeObject


cdef gobble(a, b):
    print(a, b)


def tp_new_ptr(exttype):
    assert isinstance(exttype, type)
    tp = <PyTypeObject*> exttype
    return <unsigned long long><void*>tp.tp_new


cdef class Empty:
    """
    >>> n = Empty()
    >>> isinstance(n, Empty)
    True
    >>> tp_new_ptr(Empty) != 0
    True
    """


cdef class EmptySubclass(Empty):
    """
    >>> n = EmptySubclass()
    >>> isinstance(n, EmptySubclass)
    True
    >>> tp_new_ptr(EmptySubclass) != 0
    True
    >>> tp_new_ptr(EmptySubclass) == tp_new_ptr(Empty)
    True
    """


cdef class CInit:
    """
    >>> c = CInit()
    >>> isinstance(c, CInit)
    True
    """
    def __cinit__(self):
        assert self is not None


cdef class Spam:
    """
    >>> s = Spam(12)
    >>> s.eat()
    12 42
    """
    cdef eggs
    cdef int ham

    def __cinit__(self, eggs):
        self.eggs = eggs
        self.ham = 42

    def __dealloc__(self):
        self.ham = 0

    def eat(self):
        gobble(self.eggs, self.ham)


def f(Spam spam):
    """
    >>> s = Spam(12)
    >>> f(s)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: '...Spam' object has no attribute 'foo'
    >>> s.eat()
    12 42
    >>> class Spam2(Spam):
    ...     foo = 1
    >>> s = Spam2(12)
    >>> s.eat()
    12 42
    >>> f(s)
    >>> s.eat()
    12 42
    """
    x = spam.eggs
    y = spam.ham
    z = spam.foo
    spam.eggs = x
    spam.ham = y
    spam.foo = z
