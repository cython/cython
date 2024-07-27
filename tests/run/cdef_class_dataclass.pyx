# mode: run
# tag: dataclass

from cython cimport dataclasses
from cython.dataclasses cimport dataclass, field
try:
    import typing
    from typing import ClassVar
    from dataclasses import InitVar
    import dataclasses as py_dataclasses
except ImportError:
    pass
import cython
from libc.stdlib cimport malloc, free

include "../testsupport/cythonarrayutil.pxi"

cdef class NotADataclass:
    cdef cython.int a
    b: float

    def __repr__(self):
        return "NADC"

    def __str__(self):
        return "string of NotADataclass"  # should not be called - repr is called instead!

    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return 1

@dataclass(unsafe_hash=True)
cdef class BasicDataclass:
    """
    >>> sorted(list(BasicDataclass.__dataclass_fields__.keys()))
    ['a', 'b', 'c', 'd']

    # Check the field type attribute - this is currently a string since
    # it's taken from the annotation, but if we drop PEP563 in future
    # then it may change
    >>> BasicDataclass.__dataclass_fields__["a"].type
    'float'
    >>> BasicDataclass.__dataclass_fields__["b"].type
    'NotADataclass'
    >>> BasicDataclass.__dataclass_fields__["c"].type
    'object'
    >>> BasicDataclass.__dataclass_fields__["d"].type
    'list'

    >>> inst1 = BasicDataclass() # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: __init__() takes at least 1 ...
    >>> inst1 = BasicDataclass(2.0)

    # The error at-least demonstrates that the hash function has been created
    >>> hash(inst1) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...unhashable...
    >>> inst2 = BasicDataclass(2.0)
    >>> inst1 == inst2
    True
    >>> inst2 = BasicDataclass(2.0, NotADataclass(), [])
    >>> inst1 == inst2
    False
    >>> inst2 = BasicDataclass(2.0, NotADataclass(), [], [1,2,3])
    >>> inst2
    BasicDataclass(a=2.0, b=NADC, c=[], d=[1, 2, 3])
    >>> inst2.c = "Some string"
    >>> inst2
    BasicDataclass(a=2.0, b=NADC, c='Some string', d=[1, 2, 3])
    """
    a: float
    b: NotADataclass = field(default_factory=NotADataclass)
    c: object = field(default=0)
    d: list = dataclasses.field(default_factory=list)

@dataclasses.dataclass
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

@cython.dataclasses.dataclass
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
    >>> ContainsNonPyFields()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: __init__() takes ... 1 positional ...
    >>> ContainsNonPyFields(mystruct={'a': 1 })  # doctest: +ELLIPSIS
    ContainsNonPyFields(mystruct={'a': 1}, memview=<MemoryView of 'array' at ...>)
    >>> ContainsNonPyFields(mystruct={'a': 1 }, memview=create_array((2,2), "c"))  # doctest: +ELLIPSIS
    ContainsNonPyFields(mystruct={'a': 1}, memview=<MemoryView of 'array' at ...>)
    >>> ContainsNonPyFields(mystruct={'a': 1 }, mystruct_ptr=0)
    Traceback (most recent call last):
    TypeError: __init__() got an unexpected keyword argument 'mystruct_ptr'
    """
    mystruct: S = cython.dataclasses.field(compare=False)
    mystruct_ptr: S_ptr = field(init=False, repr=False, default_factory=malloc_a_struct)
    memview: cython.int[:, ::1] = field(default=create_array((3,1), "c"),  # mutable so not great but OK for a test
                                        compare=False)

    def __dealloc__(self):
        free(self.mystruct_ptr)

@dataclass
cdef class InitClassVars:
    """
    Private (i.e. defined with "cdef") members deliberately don't appear
    TODO - ideally c1 and c2 should also be listed here
    >>> sorted(list(InitClassVars.__dataclass_fields__.keys()))
    ['a', 'b1', 'b2']
    >>> InitClassVars.c1
    2.0
    >>> InitClassVars.e1
    []
    >>> inst1 = InitClassVars()
    In __post_init__
    >>> inst1  # init vars don't appear in string
    InitClassVars(a=0)
    >>> inst2 = InitClassVars(b1=5, d2=100)
    In __post_init__
    >>> inst1 == inst2  # comparison ignores the initvar
    True
    """
    a: cython.int = 0
    b1: InitVar[cython.double] = 1.0
    b2: py_dataclasses.InitVar[cython.double] = 1.0
    c1: ClassVar[float] = 2.0
    c2: typing.ClassVar[float] = 2.0
    cdef InitVar[cython.int] d1
    cdef py_dataclasses.InitVar[cython.int] d2
    d1 = 5
    d2 = 5
    cdef ClassVar[list] e1
    cdef typing.ClassVar[list] e2
    e1 = []
    e2 = []

    def __post_init__(self, b1, b2, d1, d2):
         # Check that the initvars haven't been assigned yet
        assert self.b1==0, self.b1
        assert self.b2==0, self.b2
        assert self.d1==0, self.d1
        assert self.d2==0, self.d2
        self.b1 = b1
        self.b2 = b2
        self.d1 = d1
        self.d2 = d2
        print "In __post_init__"

@dataclass
cdef class TestVisibility:
    """
    >>> inst = TestVisibility()
    >>> "a" in TestVisibility.__dataclass_fields__
    False
    >>> hasattr(inst, "a")
    False
    >>> "b" in TestVisibility.__dataclass_fields__
    True
    >>> hasattr(inst, "b")
    True
    >>> "c" in TestVisibility.__dataclass_fields__
    True
    >>> TestVisibility.__dataclass_fields__["c"].type
    'double'
    >>> hasattr(inst, "c")
    True
    >>> "d" in TestVisibility.__dataclass_fields__
    True
    >>> TestVisibility.__dataclass_fields__["d"].type
    'object'
    >>> hasattr(inst, "d")
    True
    """
    cdef double a
    a = 1.0
    b: cython.double = 2.0
    cdef public double c
    c = 3.0
    cdef public object d
    d = object()

@dataclass(frozen=True)
cdef class TestFrozen:
    """
    >>> inst = TestFrozen(a=5)
    >>> inst.a
    5.0
    >>> inst.a = 2.  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: attribute 'a' of '...TestFrozen' objects is not writable
    """
    a: cython.double = 2.0

def get_dataclass_initvar():
    return py_dataclasses.InitVar


@dataclass(kw_only=True)
cdef class TestKwOnly:
    """
    >>> inst = TestKwOnly(a=3, b=2)
    >>> inst.a
    3.0
    >>> inst.b
    2
    >>> inst = TestKwOnly(b=2)
    >>> inst.a
    2.0
    >>> inst.b
    2
    >>> fail = TestKwOnly(3, 2)
    Traceback (most recent call last):
    TypeError: __init__() takes exactly 0 positional arguments (2 given)
    >>> fail = TestKwOnly(a=3)
    Traceback (most recent call last):
    TypeError: __init__() needs keyword-only argument b
    >>> fail = TestKwOnly()
    Traceback (most recent call last):
    TypeError: __init__() needs keyword-only argument b
    """

    a: cython.double = 2.0
    b: cython.long


__doc__ = """
>>> from dataclasses import Field, is_dataclass, fields, InitVar

# It uses the types from the standard library where available
>>> all(isinstance(v, Field) for v in BasicDataclass.__dataclass_fields__.values())
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
>>> [ f.name for f in fields(BasicDataclass)]
['a', 'b', 'c', 'd']
>>> [ f.name for f in fields(InitClassVars)]
['a']
>>> get_dataclass_initvar() == InitVar
True
"""
