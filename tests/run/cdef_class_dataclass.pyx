# mode: run
# tag: dataclass

from cython cimport dataclass, field, InitVar, ClassVar
import cython
from libc.stdlib cimport malloc, free

include "cythonarrayutil.pxi"

cdef class NotADataclass:
    cdef cython.int a
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
    >>> inst2
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
    >>> InheritsFromDataclass(a=1.0, e=5)
    In __post_init__
    InheritsFromDataclass(a=1.0, b=NADC, c=0, d=[], e=5)
    """
    e: cython.int = 0

    def __post_init__(self):
        print "In __post_init__"

@dataclass
cdef class InheritsFromNotADataclass(NotADataclass):
    """
    >>> sorted(list(InheritsFromNotADataclass.__dataclass_fields__.keys()))
    ['c']
    >>> InheritsFromNotADataclass()
    InheritsFromNotADataclass(c=1)
    >>> InheritsFromNotADataclass(5)
    InheritsFromNotADataclass(c=5)
    """

    c: cython.int = 1

cdef struct S:
    int a

ctypedef S* S_ptr

cdef S_ptr malloc_a_struct():
    return <S_ptr>malloc(sizeof(S))

@dataclass
cdef class ContainsNonPyFields:
    """
    >>> ContainsNonPyFields() # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: __init__() takes ... 1 positional ...
    >>> ContainsNonPyFields(mystruct={'a': 1 })
    ContainsNonPyFields(mystruct={'a': 1}, memview=<MemoryView of 'array' object>)
    >>> ContainsNonPyFields(mystruct={'a': 1 }, memview=create_array((2,2), "c"))
    ContainsNonPyFields(mystruct={'a': 1}, memview=<MemoryView of 'array' object>)
    >>> ContainsNonPyFields(mystruct={'a': 1 }, mystruct_ptr=0)
    Traceback (most recent call last):
    TypeError: __init__() got an unexpected keyword argument 'mystruct_ptr'
    """
    mystruct: S = field(compare=False)
    mystruct_ptr: S_ptr = field(init=False, repr=False, default_factory=malloc_a_struct)
    memview: int[:, ::1] = field(default=create_array((3,1), "c"),  # mutable so not great but OK for a test
                                 compare=False)

    def __dealloc__(self):
        free(self.mystruct_ptr)

@dataclass
cdef class InitClassVars:
    """
    >>> sorted(list(InitClassVars.__dataclass_fields__.keys()))
    ['a']
    >>> InitClassVars.c
    2.0
    >>> InitClassVars.e
    []
    >>> inst1 = InitClassVars()
    In __post_init__
    >>> inst1  # init vars don't appear in string
    InitClassVars(a=0)
    >>> inst2 = InitClassVars(b=5, d=100)
    In __post_init__
    >>> inst1 == inst2  # comparison ignores the initvar
    True
    """
    a: cython.int = 0
    b: InitVar[double] = 1.0
    c: ClassVar[float] = 2.0
    cdef InitVar[cython.int] d
    d = 5
    cdef ClassVar[list] e
    e = []

    def __post_init__(self, b, d):
        assert self.b==0, self.b  # hasn't been assigned yet
        assert self.d==0, self.d
        self.b = b
        self.d = d
        print "In __post_init__"

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
        a: cython.int = field(default_factory = lambda: 5)

    @dataclass(init=True)
    class RegularClass2:
        """
        >>> from dataclasses import is_dataclass
        >>> is_dataclass(RegularClass2)
        True
        """
        a: cython.int = field(default_factory = lambda: 5)

dc1 = dataclass  # copy the cython attributes
fld1 = field
iv1 = InitVar
cv1 = ClassVar

cimport cython
dc2 = cython.dataclass
fld2 = cython.field
iv2 = cython.InitVar
cv2 = cython.ClassVar

__doc__ = """
# test that the Cython attributes are available as PyObjects
# any further use is impossible without the dataclasses module though
>>> all(isinstance(o, object) for o in [dc1, dc2, fld1, fld2, iv1, iv2, cv1, cv2])
True
"""

if sys.version_info >= (3, 7):
    __doc__ += """
    >>> from dataclasses import is_dataclass, dataclass, field, InitVar
    >>> from typing import ClassVar

    # cython attributes revert to being the standard library values
    >>> dc1 is dc2 and dc1 is dataclass
    True
    >>> fld1 is fld2 and fld1 is field
    True
    >>> iv1 is iv2 and iv1 is InitVar
    True
    >>> cv1 is cv2 and cv1 is ClassVar
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
