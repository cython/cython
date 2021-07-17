cimport cython

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
    """
    implemented: cython.bint

    def __init__(self, *, implemented=True):
        self.implemented = implemented

    def __add__(self, other):
        if (<Base>self).implemented:
            return "Base.__add__(%s, %s)" % (self, other)
        else:
            return NotImplemented

    def __radd__(self, other):
        if (<Base>self).implemented:
            return "Base.__radd__(%s, %s)" % (self, other)
        else:
            return NotImplemented

    def __pow__(self, other, mod):
        if (<Base>self).implemented:
            return "Base.__pow__(%s, %s, %s)" % (self, other, mod)
        else:
            return NotImplemented

    def __rpow__(self, other, mod):
        if (<Base>self).implemented:
            return "Base.__rpow__(%s, %s, %s)" % (self, other, mod)
        else:
            return NotImplemented

    def __repr__(self):
        return "%s()" % (self.__class__.__name__)

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
        if (<OverloadLeft>self).derived_implemented:
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
        if (<OverloadRight>self).derived_implemented:
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
        if isinstance(self, OverloadCApi):
            derived_implemented = (<OverloadCApi>self).derived_implemented
        else:
            derived_implemented = (<OverloadCApi>other).derived_implemented
        if derived_implemented:
            return "OverloadCApi.__add__(%s, %s)" % (self, other)
        else:
            return NotImplemented

# TODO: Test a class that only defines the `__r...__()` methods.
