# mode: run
# tag: dataclass

from __future__ import print_function

from cython cimport dataclass, field

cdef class NotADataclass:
    cdef int a
    b: float

    def __repr__(self):
        return "NADC"

    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return 1

@dataclass(unsafe_hash=True)
cdef class BasicDataclass:
    """
    >>> sorted(list(BasicDataclass.__dataclass_fields__.keys()))
    ['a', 'b', 'c', 'd']
    >>> BasicDataclass.__dataclass_fields__['a'].type == float
    True
    >>> BasicDataclass.__dataclass_fields__['b'].type == NotADataclass
    True
    >>> BasicDataclass.__dataclass_fields__['c'].type == object
    True
    >>> BasicDataclass.__dataclass_fields__['d'].type == list
    True
    >>> inst1 = BasicDataclass() # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: __init__() takes at least 1 ...
    >>> inst1 = BasicDataclass(2.0)

    # The error at-least demonstrates that the hash function has been created
    >>> hash(inst1)
    Traceback (most recent call last):
    TypeError: unhashable type: 'list'
    >>> inst2 = BasicDataclass(2.0)
    >>> inst1 == inst2
    True
    >>> inst2 = BasicDataclass(2.0, NotADataclass(), [])
    >>> inst1 == inst2
    False
    >>> inst2 = BasicDataclass(2.0, NotADataclass(), [], [1,2,3])
    >>> print(inst2)
    BasicDataclass(a=2.0, b=NADC, c=[], d=[1, 2, 3])
    """
    a: float
    b: NotADataclass = field(default_factory=NotADataclass)
    c: object = field(default=0)
    d: list = field(default_factory=list)

@dataclass
cdef class InheritsFromDataclass(BasicDataclass):
    """
    >>> sorted(list(InheritsFromDataclass.__dataclass_fields__.keys()))
    ['a', 'b', 'c', 'd', 'e']
    >>> print(InheritsFromDataclass(a=1.0, e=5))
    In __post_init__
    InheritsFromDataclass(a=1.0, b=NADC, c=0, d=[], e=5)
    """
    e: int = 0

    def __post_init__(self):
        print("In __post_init__")

@dataclass
cdef class InheritsFromNotADataclass(NotADataclass):
    """
    >>> sorted(list(InheritsFromNotADataclass.__dataclass_fields__.keys()))
    ['c']
    >>> print(InheritsFromNotADataclass())
    InheritsFromNotADataclass(c=1)
    >>> print(InheritsFromNotADataclass(5))
    InheritsFromNotADataclass(c=5)
    """

    c: int = 1

import sys
if (sys.version_info >= (3, 7)
        and False # TODO: This currently doesn't work because regular classes don't
            # create __annotations__
        ):
    # if possible the Cython decorators should fall back to the Python module
    # where available.
    @dataclass
    class RegularClass:
        """
        >>> from dataclasses import is_dataclass
        >>> is_dataclass(RegularClass)
        True
        >>> is_dataclass(RegularClass())
        True
        """
        a: int = field(default_factory = lambda: 5)

    @dataclass(init=True)
    class RegularClass2:
        """
        >>> from dataclasses import is_dataclass
        >>> is_dataclass(RegularClass2)
        True
        """
        a: int = field(default_factory = lambda: 5)

if sys.version_info >= (3, 7):
    dc = dataclass  # copy the cython attributes
    fld = field
    __doc__ = """
    >>> from dataclasses import is_dataclass, dataclass, field

    # cython attributes revert to being the standard library values
    >>> dc is dataclass
    True
    >>> fld is field
    True

    # check out Cython dataclasses are close enough to convince it
    >>> is_dataclass(BasicDataclass)
    True
    >>> is_dataclass(BasicDataclass(1.5))
    True
    >>> is_dataclass(InheritsFromDataclass)
    True
    >>> is_dataclass(NotADataclass)
    False
    >>> is_dataclass(InheritsFromNotADataclass)
    True
    """
