cimport cython

@cython.c_api_binop_methods(False)
@cython.cclass
class Base(object):
    """
    >>> Base() + 2
    'Base.__add__(Base(), 2)'
    >>> 2 + Base()
    'Base.__radd__(Base(), 2)'
    """
    def __add__(self, other):
        return "Base.__add__(%s, %s)" % (self, other)

    def __radd__(self, other):
        return "Base.__radd__(%s, %s)" % (self, other)

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
    """
    def __add__(self, other):
        return "OverloadLeft.__add__(%s, %s)" % (self, other)


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
    >>> OverloadCApi() + 2
    'OverloadCApi.__add__(OverloadCApi(), 2)'
    >>> 2 + OverloadCApi()
    'OverloadCApi.__add__(2, OverloadCApi())'

    >>> OverloadCApi() + Base()
    'OverloadCApi.__add__(OverloadCApi(), Base())'
    >>> Base() + OverloadCApi()
    'OverloadCApi.__add__(Base(), OverloadCApi())'
    """
    def __add__(self, other):
        return "OverloadCApi.__add__(%s, %s)" % (self, other)

