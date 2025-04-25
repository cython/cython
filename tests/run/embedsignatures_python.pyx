# cython: embedsignature=True
# cython: embedsignature.format=python
# cython: annotation_typing=False
# cython: c_string_type=bytearray

cpdef object      f00(object a): return a
cpdef long double f01(unsigned int a): return <double>a
cpdef long double f02(unsigned int a: float): return <double>a

__doc__ = ur"""
>>> print(f00.__doc__)
f00(a)

>>> print(f01.__doc__)
f01(a: int) -> float

>>> print(f02.__doc__)
f02(a: float) -> float

"""

include "skip_limited_api_helper.pxi"

cdef class Foo:
    "Foo docstring"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        "init Foo"
        pass

    def m00(self, a): return a
    def m01(self, unsigned int a): return a
    def m02(self, unsigned int a: int): return a
    def m03(self: Self, unsigned int a: int) -> float: return a
    def m04(self, const char* a): return a
    def m05(self, const char a[]): return a
    def m06(self, const char* a: bytes) -> bytes: return a

    @classmethod
    def c00(cls, a): return a
    @classmethod
    def c01(type cls, unsigned int a): return a
    @classmethod
    def c02(cls: type[Foo], unsigned int a: int): return a
    @classmethod
    def c03(type cls: type[Foo], unsigned int a: int) -> float: return a

    @staticmethod
    def s00(a): return a
    @staticmethod
    def s01(unsigned int a): return a
    @staticmethod
    def s02(unsigned int a: int): return a
    @staticmethod
    def s03(unsigned int a: int) -> float: return a

    cdef public long int p0
    property p1:
        """p1 docstring"""
        def __get__(self):
            return 0
    property p2:
        """p2 docstring"""
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

"""


@skip_if_limited_api("known bugs")
def test_nonlimited_api():
    """
    >>> print(Foo.__init__.__doc__)
    __init__(self, *args: Any, **kwargs: Any) -> None
    init Foo

    >>> print(Foo.__call__.__doc__)
    __call__(self, a: int, b: float = 1.0, *args: tuple, **kwargs: dict) -> (None, True)
    call docstring
    """

__doc__ += ur"""
>>> print(Foo.m00.__doc__)
m00(self, a)

>>> print(Foo.m01.__doc__)
m01(self, a: int)

>>> print(Foo.m02.__doc__)
m02(self, a: int)

>>> print(Foo.m03.__doc__)
m03(self: Self, a: int) -> float

>>> print(Foo.m04.__doc__)
m04(self, a: bytearray)

>>> print(Foo.m05.__doc__)
m05(self, a: bytearray)

>>> print(Foo.m06.__doc__)
m06(self, a: bytes) -> bytes

"""

__doc__ += ur"""
>>> print(Foo.c00.__doc__)
c00(cls, a)

>>> print(Foo.c01.__doc__)
c01(cls, a: int)

>>> print(Foo.c02.__doc__)
c02(cls: type[Foo], a: int)

>>> print(Foo.c03.__doc__)
c03(cls: type[Foo], a: int) -> float

"""

__doc__ += ur"""
>>> print(Foo.s00.__doc__)
s00(a)

>>> print(Foo.s01.__doc__)
s01(a: int)

>>> print(Foo.s02.__doc__)
s02(a: int)

>>> print(Foo.s03.__doc__)
s03(a: int) -> float

"""

__doc__ += ur"""
>>> print(Foo.p0.__doc__)
p0: int

>>> print(Foo.p1.__doc__)
p1 docstring

>>> print(Foo.p2.__doc__)
p2: int
p2 docstring

>>> print(Foo.p3.__doc__)
p3: Foo

>>> print(Foo.__add__.__doc__)
__add__(self, other: Foo) -> Foo
add docstring

"""

ctypedef long     long      LongLong
ctypedef signed   long long LongLongSigned
ctypedef unsigned long long LongLongUnsigned

cdef class Bar:

    cpdef          char       m00(self,          char       a): return a
    cpdef signed   char       m01(self, signed   char       a): return a
    cpdef unsigned char       m02(self, unsigned char       a): return a

    cpdef          short      m10(self,          short      a): return a
    cpdef signed   short      m11(self, signed   short      a): return a
    cpdef unsigned short      m12(self, unsigned short      a): return a

    cpdef          int        m20(self,          int        a): return a
    cpdef signed   int        m21(self, signed   int        a): return a
    cpdef unsigned int        m22(self, unsigned int        a): return a

    cpdef          long       m30(self,          long       a): return a
    cpdef signed   long       m31(self, signed   long       a): return a
    cpdef unsigned long       m32(self, unsigned long       a): return a

    cpdef          long long  m40(self,          long long  a): return a
    cpdef signed   long long  m41(self, signed   long long  a): return a
    cpdef unsigned long long  m42(self, unsigned long long  a): return a

    cpdef LongLong            m43(self, LongLong            a): return a
    cpdef LongLongSigned      m44(self, LongLongSigned      a): return a
    cpdef LongLongUnsigned    m45(self, LongLongUnsigned    a): return a

    cpdef float               m50(self, float               a): return a
    cpdef double              m60(self, double              a): return a
    cpdef long double         m70(self, long double         a): return a

    cpdef float       complex m51(self, float       complex a): return a
    cpdef double      complex m61(self, double      complex a): return a
    cpdef long double complex m71(self, long double complex a): return a


__doc__ += ur"""
>>> print(Bar.m00.__doc__)
m00(self, a: int) -> int

>>> print(Bar.m01.__doc__)
m01(self, a: int) -> int

>>> print(Bar.m02.__doc__)
m02(self, a: int) -> int

"""

__doc__ += ur"""
>>> print(Bar.m10.__doc__)
m10(self, a: int) -> int

>>> print(Bar.m11.__doc__)
m11(self, a: int) -> int

>>> print(Bar.m12.__doc__)
m12(self, a: int) -> int

"""

__doc__ += ur"""
>>> print(Bar.m20.__doc__)
m20(self, a: int) -> int

>>> print(Bar.m21.__doc__)
m21(self, a: int) -> int

>>> print(Bar.m22.__doc__)
m22(self, a: int) -> int

"""

__doc__ += ur"""
>>> print(Bar.m30.__doc__)
m30(self, a: int) -> int

>>> print(Bar.m31.__doc__)
m31(self, a: int) -> int

>>> print(Bar.m32.__doc__)
m32(self, a: int) -> int

"""

__doc__ += ur"""
>>> print(Bar.m40.__doc__)
m40(self, a: int) -> int

>>> print(Bar.m41.__doc__)
m41(self, a: int) -> int

>>> print(Bar.m42.__doc__)
m42(self, a: int) -> int

"""

__doc__ += ur"""
>>> print(Bar.m43.__doc__)
m43(self, a: int) -> int

>>> print(Bar.m44.__doc__)
m44(self, a: int) -> int

>>> print(Bar.m45.__doc__)
m45(self, a: int) -> int

"""

__doc__ += ur"""
>>> print(Bar.m50.__doc__)
m50(self, a: float) -> float

>>> print(Bar.m60.__doc__)
m60(self, a: float) -> float

>>> print(Bar.m70.__doc__)
m70(self, a: float) -> float

"""

__doc__ += ur"""
>>> print(Bar.m51.__doc__)
m51(self, a: complex) -> complex

>>> print(Bar.m61.__doc__)
m61(self, a: complex) -> complex

>>> print(Bar.m71.__doc__)
m71(self, a: complex) -> complex

"""
