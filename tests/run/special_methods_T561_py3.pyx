# ticket: 561
# tag: py3
# This file tests the behavior of special methods under Python 3
# after #561.  (Only methods whose behavior differs between Python 2 and 3
# are tested here; see special_methods_T561.pyx for the rest of the tests.)

__doc__ = u"""
    >>> vs0 = VerySpecial(0)
    VS __init__ 0
    >>> # Python 3 does not use __cmp__, so any provided __cmp__ method is
    >>> # discarded under Python 3.
    >>> vs0_cmp = vs0.__cmp__
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561_py3.VerySpecial' object has no attribute '__cmp__'
    >>> # Python 3 does not use __div__ or __idiv__, so these methods are
    >>> # discarded under Python 3.
    >>> vs0_div = vs0.__div__
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561_py3.VerySpecial' object has no attribute '__div__'
    >>> vs0_rdiv = vs0.__rdiv__
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561_py3.VerySpecial' object has no attribute '__rdiv__'
    >>> vs0_idiv = vs0.__idiv__
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561_py3.VerySpecial' object has no attribute '__idiv__'
    >>> # Python 3 does not use __oct__ or __hex__, so these methods are
    >>> # discarded under Python 3.
    >>> vs0_oct = vs0.__oct__
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561_py3.VerySpecial' object has no attribute '__oct__'
    >>> vs0_hex = vs0.__hex__
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561_py3.VerySpecial' object has no attribute '__hex__'
    >>> # Python 3 does not use __long__; if you define __long__ but not
    >>> # __int__, the __long__ definition will be used for __int__.
    >>> Ll = Long().__long__
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561_py3.Long' object has no attribute '__long__'
    >>> Li = Long().__int__
    >>> Li()
    Long __long__
    >>> # As of Python 3, defining __nonzero__ gives you a __bool__ method
    >>> # instead.
    >>> vs0_bool = vs0.__bool__
    >>> vs0_bool()
    VS __nonzero__ 0
    False
"""

cdef class VerySpecial:
    cdef readonly int value

    def __init__(self, v):
        self.value = v
        print "VS __init__ %d" % self.value

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

cdef class Long:
    def __long__(self):
        print "Long __long__"
