# ticket: 561
# tag: py2
# This file tests the behavior of special methods under Python 2
# after #561.  (Only methods whose behavior differs between Python 2 and 3
# are tested here; see special_methods_T561.pyx for the rest of the tests.)

__doc__ = u"""
    >>> vs0 = VerySpecial(0)
    VS __init__ 0
    >>> vs1 = VerySpecial(1)
    VS __init__ 1
    >>> # Python 3 does not use __cmp__.
    >>> vs0_cmp = vs0.__cmp__
    >>> vs0_cmp(vs1)
    VS __cmp__ 0 1
    0
    >>> # Python 3 does not use __div__ or __idiv__.
    >>> vs0_div = vs0.__div__
    >>> vs0_div(vs1)
    VS __div__ 0 1
    >>> vs0_idiv = vs0.__idiv__
    >>> vs0_idiv(vs1)
    VS __idiv__ 0 /= 1
    >>> vs0_rdiv = vs0.__rdiv__
    >>> vs0_rdiv(vs1)
    VS __div__ 1 0
    >>> # Python 3 does not use __oct__ or __hex__.
    >>> vs0_oct = vs0.__oct__
    >>> vs0_oct()
    VS __oct__ 0
    >>> vs0_hex = vs0.__hex__
    >>> vs0_hex()
    VS __hex__ 0
    >>> # Python 3 does not use __nonzero__; if you define a __nonzero__
    >>> # method, Cython for Python 3 would give you a __bool__ method
    >>> # instead.
    >>> vs0_nonzero = vs0.__nonzero__
    >>> vs0_nonzero()
    VS __nonzero__ 0
    False
    >>> # If you define __next__, you get both __next__ and next (this behavior
    >>> # is unchanged by T561, but only happens in Python 2)
    >>> vs0_next = vs0.__next__
    >>> vs0_next()
    VS next/__next__ 0
    >>> vs0_next2 = vs0.next
    >>> vs0_next2()
    VS next/__next__ 0
    >>> # Cython supports getslice only for Python 2.
    >>> vs0_getslice = vs0.__getslice__
    >>> vs0_getslice(13, 42)
    VS __getslice__ 0 13 42
    >>> # Cython supports setslice and delslice only for Python 2.
    >>> # If you define either setslice or delslice, you get wrapper objects
    >>> # for both methods.  (This behavior is unchanged by #561.)
    >>> ss_setslice = SetSlice().__setslice__
    >>> ss_setslice(13, 42, 'foo')
    SetSlice setslice 13 42 'foo'
    >>> ss_delslice = SetSlice().__delslice__
    >>> ss_delslice(13, 42)
    Traceback (most recent call last):
    ...
    NotImplementedError: 2-element slice deletion not supported by special_methods_T561_py2.SetSlice
    >>> ds_setslice = DelSlice().__setslice__
    >>> ds_setslice(13, 42, 'foo')
    Traceback (most recent call last):
    ...
    NotImplementedError: 2-element slice assignment not supported by special_methods_T561_py2.DelSlice
    >>> ds_delslice = DelSlice().__delslice__
    >>> ds_delslice(13, 42)
    DelSlice delslice 13 42
    >>> sds_setslice = SetDelSlice().__setslice__
    >>> sds_setslice(13, 42, 'foo')
    SetDelSlice setslice 13 42 'foo'
    >>> sds_delslice = SetDelSlice().__delslice__
    >>> sds_delslice(13, 42)
    SetDelSlice delslice 13 42
    >>> # Python 3 does not use __long__.
    >>> Ll = Long().__long__
    >>> Ll()
    Long __long__
"""

cdef class VerySpecial:
    cdef readonly int value

    def __init__(self, v):
        self.value = v
        print "VS __init__ %d" % self.value

    def __getslice__(self, a, b):
        print "VS __getslice__ %d %d %d" % (self.value, a, b)

    def __next__(self):
        print "VS next/__next__ %d" % self.value

    def __nonzero__(self):
        print "VS __nonzero__ %d" % self.value

    def __oct__(self):
        print "VS __oct__ %d" % self.value

    def __hex__(self):
        print "VS __hex__ %d" % self.value

    def __cmp__(self, other):
        print "VS __cmp__ %d %d" % (self.value, other.value)

    def __div__(self, other):
        print "VS __div__ %d %d" % (self.value, other.value)

    def __idiv__(self, other):
        print "VS __idiv__ %d /= %d" % (self.value, other.value)

cdef class SetSlice:
    def __setslice__(self, a, b, value):
        print "SetSlice setslice %d %d %r" % (a, b, value)

cdef class DelSlice:
    def __delslice__(self, a, b):
        print "DelSlice delslice %d %d" % (a, b)

cdef class SetDelSlice:
    def __setslice__(self, a, b, value):
        print "SetDelSlice setslice %d %d %r" % (a, b, value)

    def __delslice__(self, a, b):
        print "SetDelSlice delslice %d %d" % (a, b)

cdef class Long:
    def __long__(self):
        print "Long __long__"
