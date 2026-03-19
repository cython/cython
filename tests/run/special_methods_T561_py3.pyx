# ticket: t561
# tag: py3, warnings
# This file tests the behavior of special methods under Python 3
# after #561.  (Only methods whose behavior differs between Python 2 and 3
# are tested here; see special_methods_T561.pyx for the rest of the tests.)

__doc__ = u"""
    >>> vs0 = VerySpecial(0)
    VS __init__ 0

    >>> # Python 3 does not use __cmp__, __div__, __idiv__, __oct__ or __hex__;
    >>> # These methods have no special behaviour and aren't tested beyond that
    >>> # they don't break compilation.

    >>> # Python 3 does not use __long__; if you define __long__ but not
    >>> # __int__, the __long__ definition will be used for __int__.
    >>> Ll = Long().__long__  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: 'special_methods_T561_py3.Long' object has no attribute '__long__'...
    >>> Li = Long().__int__
    >>> Li()
    Long __long__

    >>> # As of Python 3, defining __nonzero__ gives you a __bool__ method instead.
    >>> vs0_bool = vs0.__bool__
    >>> vs0_bool()
    VS __nonzero__ 0
    False
"""

cdef class VerySpecial:
    cdef readonly int value

    def __init__(self, v):
        self.value = v
        print(f"VS __init__ {self.value}")

    def __nonzero__(self):
        print(f"VS __nonzero__ {self.value}")

    def __oct__(self):
        print(f"VS __oct__ {self.value}")

    def __hex__(self):
        print(f"VS __hex__ {self.value}")

    def __cmp__(self, other):
        print(f"VS __cmp__ {self.value} {other.value}")

    def __div__(self, other):
        print(f"VS __div__ {self.value} / {other.value}")

    def __idiv__(self, other):
        print(f"VS __idiv__ {self.value} /= {other.value}")


cdef class Bool:
    """
    >>> b = Bool()
    >>> bool(b)
    VS __bool__
    False
    """
    def __bool__(self):
        print("VS __bool__")

    def __nonzero__(self):
        print("VS __nonzero__")
        return self.__bool__()


cdef class Long:
    def __long__(self):
        print("Long __long__")


_WARNINGS = """
38:4: __nonzero__ was removed in Python 3; use __bool__ instead
67:4: __nonzero__ was removed in Python 3; ignoring it and using __bool__ instead
73:4: __long__ was removed in Python 3; use __int__ instead
"""
