cimport cython

@cython.c_api_binop_methods(False)
@cython.cclass
class Base(object):
    """
    >>> Base(1) + 2
    'Base.__add__(Base(), 2)'
    >>> 2 + Base(1)
    'Base.__radd__(Base(), 2)'

    >>> Base(0) + 2  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    >>> 2 + Base(0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...

    >>> Base(1) ** 2
    'Base.__pow__(Base(), 2, None)'
    >>> 2 ** Base(1)
    'Base.__rpow__(Base(), 2, None)'
    >>> pow(Base(1), 2, 100)
    'Base.__pow__(Base(), 2, 100)'
    """
    implemented: cython.int

    def __init__(self, implemented):
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
    >>> OverloadLeft(1) + 2
    'OverloadLeft.__add__(OverloadLeft(), 2)'
    >>> 2 + OverloadLeft(1)
    'Base.__radd__(OverloadLeft(), 2)'

    >>> OverloadLeft(1) + Base(1)
    'OverloadLeft.__add__(OverloadLeft(), Base())'
    >>> Base(1) + OverloadLeft(1)
    'Base.__add__(Base(), OverloadLeft())'

    >>> OverloadLeft(0) + Base(0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    >>> Base(0) + OverloadLeft(0)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    """
    derived_implemented: cython.int

    def __init__(self, derived_implemented):
        super().__init__(1)
        self.derived_implemented = derived_implemented

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
    """
    def __radd__(self, other):
        return "OverloadRight.__radd__(%s, %s)" % (self, other)

@cython.c_api_binop_methods(True)
@cython.cclass
class OverloadCApi(Base):
    """
    >>> OverloadCApi(1) + 2
    'OverloadCApi.__add__(OverloadCApi(), 2)'
    >>> 2 + OverloadCApi(1)
    'OverloadCApi.__add__(2, OverloadCApi())'

    >>> OverloadCApi(1) + Base(1)
    'OverloadCApi.__add__(OverloadCApi(), Base())'
    >>> Base(1) + OverloadCApi(1)
    'OverloadCApi.__add__(Base(), OverloadCApi())'

    >>> OverloadCApi(0) + 2 #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    >>> 2 + OverloadCApi(0) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type...
    """
    derived_implemented: cython.int

    def __init__(self, derived_implemented):
        super().__init__(1)
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

