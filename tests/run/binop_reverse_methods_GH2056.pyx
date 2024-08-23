cimport cython

import sys
IS_PYTHON2 = sys.version_info[0] == 2

__doc__ = ""


@cython.c_api_binop_methods(False)
@cython.cclass
class Base(object):
    """
    >>> Base() + 2
    'Base.__add__(Base(), 2)'
    >>> 2 + Base()
    'Base.__radd__(Base(), 2)'

    >>> Base(implemented=False) + 2  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    >>> 2 + Base(implemented=False)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...

    >>> Base() ** 2
    'Base.__pow__(Base(), 2, None)'
    >>> 2 ** Base()
    'Base.__rpow__(Base(), 2, None)'
    >>> pow(Base(), 2, 100)
    'Base.__pow__(Base(), 2, 100)'
    >>> Base() // 1
    True
    >>> set() // Base()
    True

    # version dependent tests for @ and / are external
    """
    implemented: cython.bint

    def __init__(self, *, implemented=True):
        self.implemented = implemented

    def __add__(self, other):
        assert cython.typeof(self) == "Base"
        if self.implemented:
            return "Base.__add__(%s, %s)" % (self, other)
        else:
            return NotImplemented

    def __radd__(self, other):
        assert cython.typeof(self) == "Base"
        if self.implemented:
            return "Base.__radd__(%s, %s)" % (self, other)
        else:
            return NotImplemented

    def __pow__(self, other, mod):
        assert cython.typeof(self) == "Base"
        if self.implemented:
            return "Base.__pow__(%s, %s, %s)" % (self, other, mod)
        else:
            return NotImplemented

    def __rpow__(self, other, mod):
        assert cython.typeof(self) == "Base"
        if self.implemented:
            return "Base.__rpow__(%s, %s, %s)" % (self, other, mod)
        else:
            return NotImplemented

    def __repr__(self):
        return "%s()" % (self.__class__.__name__)

    # The following methods were missed from the initial implementation
    # that typed 'self'. These tests are a quick test to confirm that
    # but not the full binop behaviour
    def __matmul__(self, other):
        return cython.typeof(self) == 'Base'

    def __rmatmul__(self, other):
        return cython.typeof(self) == 'Base'

    def __truediv__(self, other):
        return cython.typeof(self) == 'Base'

    def __rtruediv__(self, other):
        return cython.typeof(self) == 'Base'

    def __floordiv__(self, other):
        return cython.typeof(self) == 'Base'

    def __rfloordiv__(self, other):
        return cython.typeof(self) == 'Base'


__doc__ += """
>>> Base() @ 1
True
>>> set() @ Base()
True

>>> Base() / 1
True
>>> set() / Base()
True
"""


@cython.c_api_binop_methods(False)
@cython.cclass
class OverloadLeft(Base):
    """
    >>> OverloadLeft() + 2
    'OverloadLeft.__add__(OverloadLeft(), 2)'
    >>> 2 + OverloadLeft()
    'Base.__radd__(OverloadLeft(), 2)'

    >>> OverloadLeft() + Base()
    'OverloadLeft.__add__(OverloadLeft(), Base())'
    >>> Base() + OverloadLeft()
    'Base.__add__(Base(), OverloadLeft())'

    >>> OverloadLeft(implemented=False) + Base(implemented=False)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    >>> Base(implemented=False) + OverloadLeft(implemented=False)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    """
    derived_implemented: cython.bint

    def __init__(self, *, implemented=True):
        super().__init__(implemented=implemented)
        self.derived_implemented = implemented

    def __add__(self, other):
        assert cython.typeof(self) == "OverloadLeft"
        if self.derived_implemented:
            return "OverloadLeft.__add__(%s, %s)" % (self, other)
        else:
            return NotImplemented


@cython.c_api_binop_methods(False)
@cython.cclass
class OverloadRight(Base):
    """
    >>> OverloadRight() + 2
    'Base.__add__(OverloadRight(), 2)'
    >>> 2 + OverloadRight()
    'OverloadRight.__radd__(OverloadRight(), 2)'

    >>> OverloadRight() + Base()
    'Base.__add__(OverloadRight(), Base())'
    >>> Base() + OverloadRight()
    'OverloadRight.__radd__(OverloadRight(), Base())'

    >>> OverloadRight(implemented=False) + Base(implemented=False)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    >>> Base(implemented=False) + OverloadRight(implemented=False)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    """
    derived_implemented: cython.bint

    def __init__(self, *, implemented=True):
        super().__init__(implemented=implemented)
        self.derived_implemented = implemented

    def __radd__(self, other):
        assert cython.typeof(self) == "OverloadRight"
        if self.derived_implemented:
            return "OverloadRight.__radd__(%s, %s)" % (self, other)
        else:
            return NotImplemented


@cython.c_api_binop_methods(True)
@cython.cclass
class OverloadCApi(Base):
    """
    >>> OverloadCApi() + 2
    'OverloadCApi.__add__(OverloadCApi(), 2)'
    >>> 2 + OverloadCApi()
    'OverloadCApi.__add__(2, OverloadCApi())'

    >>> OverloadCApi() + Base()
    'OverloadCApi.__add__(OverloadCApi(), Base())'
    >>> Base() + OverloadCApi()
    'OverloadCApi.__add__(Base(), OverloadCApi())'

    >>> OverloadCApi(derived_implemented=False) + 2 #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    >>> 2 + OverloadCApi(derived_implemented=False) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    """
    derived_implemented: cython.bint

    def __init__(self, *, derived_implemented=True):
        super().__init__(implemented=True)
        self.derived_implemented = derived_implemented

    def __add__(self, other):
        assert cython.typeof(self) != "OverloadCApi"  # should be untyped
        if isinstance(self, OverloadCApi):
            derived_implemented = (<OverloadCApi>self).derived_implemented
        else:
            derived_implemented = (<OverloadCApi>other).derived_implemented
        if derived_implemented:
            return "OverloadCApi.__add__(%s, %s)" % (self, other)
        else:
            return NotImplemented


__doc__ += """
>>> d = PyVersionDependent()
>>> d @ 2
9
>>> 2 @ d
99
>>> i = d
>>> i @= 2
>>> i
999
"""


@cython.c_api_binop_methods(False)
@cython.cclass
class PyVersionDependent:
    """
    >>> d = PyVersionDependent()
    >>> d / 2
    5
    >>> 2 / d
    2
    >>> d // 2
    55
    >>> 2 // d
    22
    >>> i = d
    >>> i /= 2
    >>> i
    4
    >>> i = d
    >>> i //= 2
    >>> i
    44
    """
    def __div__(self, other):
        assert IS_PYTHON2
        return 5

    def __rdiv__(self, other):
        assert IS_PYTHON2
        return 2

    def __idiv__(self, other):
        assert IS_PYTHON2
        return 4

    def __truediv__(self, other):
        assert not IS_PYTHON2
        return 5

    def __rtruediv__(self, other):
        assert not IS_PYTHON2
        return 2

    def __itruediv__(self, other):
        assert not IS_PYTHON2
        return 4

    def __floordiv__(self, other):
        return 55

    def __rfloordiv__(self, other):
        return 22

    def __ifloordiv__(self, other):
        return 44

    def __matmul__(self, other):
        return 9

    def __rmatmul__(self, other):
        return 99

    def __imatmul__(self, other):
        return 999


@cython.cclass
class CallMethodsDirectly:
    """
    A slightly more useful version of this pattern is used by
    Pandas. In order to (a) not cause a recursion error and
    (b) correctly follow Python behaviour, the call to __add__
    should use the function as written and not our dispatch
    wrapper.

    >>> CallMethodsDirectly() + CallMethodsDirectly  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...

    We can also do this
    >>> CallMethodsDirectly().__radd__(None)  #doctest: +ELLIPSIS
    NotImplemented
    """

    def __add__(self, other):
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)


# TODO: Test a class that only defines the `__r...__()` methods.
