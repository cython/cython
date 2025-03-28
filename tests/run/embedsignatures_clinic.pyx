# cython: embedsignature=True
# cython: embedsignature.format=clinic
# cython: annotation_typing=False
# cython: binding=False
# cython: c_string_type=bytearray
# tag: py3only

def f00(a, object b=42):
    "f00 docstring"
    pass

def f01(unsigned int a: int, unsigned int b: int = 42, /, c=123):
    "f01 docstring"
    pass

def f02(unsigned int a: float, *, unsigned int b: float = 42) -> tuple[int]:
    "f02 docstring"
    pass

__doc__ = ur"""
>>> print(f00.__doc__)
f00 docstring
>>> print(f00.__text_signature__)
(a, b=42)

>>> print(f01.__doc__)
f01 docstring
>>> print(f01.__text_signature__)
(a, b=42, /, c=123)

>>> print(f02.__doc__)
f02 docstring
>>> print(f02.__text_signature__)
(a, *, b=42)

"""


cdef class Foo:
    "Foo docstring"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        "init Foo"
        pass

    def m00(self, a, b=42, *args, c=123):
        "m00 docstring"
        pass

    def m01(self, a, b=42, *, c=123, **kwargs):
        "m01 docstring"
        pass

    @classmethod
    def c00(cls, a):
        "c00 docstring"
        pass

    @staticmethod
    def s00(a):
        "s00 docstring"
        pass

    cdef public long int p0
    property p1:
        "p1 docstring"
        def __get__(self):
            return 0
    property p2:
        "p2 docstring"
        def __get__(self) -> int:
            return 0
    cdef public Foo p3

    def __call__(self, a: int, b: float = 1.0, *args: tuple, **kwargs: dict) -> (None, True):
        """
        call docstring
        """
        pass

    def __add__(self, Foo other) -> Foo:
        """
        add docstring
        """
        return self



__doc__ += ur"""
>>> print(Foo.__doc__)
Foo docstring
>>> print(Foo.__init__.__doc__)
init Foo
>>> print(Foo.__init__.__text_signature__)
($self, *args, **kwargs)

"""

__doc__ += ur"""
>>> print(Foo.m00.__doc__)
m00 docstring
>>> print(Foo.m00.__text_signature__)
($self, a, b=42, *args, c=123)

>>> print(Foo.m01.__doc__)
m01 docstring
>>> print(Foo.m01.__text_signature__)
($self, a, b=42, *, c=123, **kwargs)

"""

__doc__ += ur"""
>>> print(Foo.c00.__doc__)
c00 docstring
>>> print(Foo.c00.__text_signature__)
($type, a)

>>> print(Foo.s00.__doc__)
s00 docstring
>>> print(Foo.s00.__text_signature__)
(a)

"""


__doc__ += ur"""
>>> print(Foo.p0.__doc__)
None

>>> print(Foo.p1.__doc__)
p1 docstring

>>> print(Foo.p2.__doc__)
p2 docstring

>>> print(Foo.p3.__doc__)
None

>>> print(Foo.__call__.__doc__)
call docstring

>>> print(Foo.__call__.__text_signature__)
($self, a, b=1.0, *args, **kwargs)

>>> print(Foo.__add__.__doc__)
add docstring

>>> print(Foo.__add__.__text_signature__)
($self, other)

"""
