#cython: embedsignature=True, annotation_typing=False

# signatures here are a little fragile - when they are
# generated during the build process gives slightly
# different (but equivalent) forms - therefore tests
# may need changing occasionally to reflect behaviour
# and this isn't necessarily a bug

import sys

include "skip_limited_api_helper.pxi"

def funcdoc(f):
    if not getattr(f, "__text_signature__", None):
        return f.__doc__
    doc = '%s%s' % (f.__name__, f.__text_signature__)
    if f.__doc__:
        if '\n' in f.__doc__:
            # preceding line endings get stripped
            doc = '%s\n\n%s' % (doc, f.__doc__)
        else:
            doc = '%s\n%s' % (doc, f.__doc__)
    return doc


# note the r, we use \n below
__doc__ = ur"""
    >>> print (Ext.__doc__)
    Ext(a, b, c=None)

    >>> print (Ext.attr0.__doc__)
    attr0: 'int'
    attr0 docstring
    >>> print (Ext.attr1.__doc__)
    attr1: object
    attr1 docstring
    >>> print (Ext.attr2.__doc__)
    attr2: list
    >>> print (Ext.attr3.__doc__)
    attr3: embedsignatures.Ext

    >>> print (Ext.prop0.__doc__)
    prop0 docstring
    >>> print (Ext.prop1.__doc__)
    None
    >>> print (Ext.attr4.__doc__)
    attr4 docstring
    >>> print (Ext.attr5.__doc__)
    attr5: 'int'
    attr5 docstring

    >>> print (Ext.a.__doc__)
    Ext.a(self)

    >>> print (Ext.b.__doc__)
    Ext.b(self, a, b, c)

    >>> print (Ext.c.__doc__)
    Ext.c(self, a, b, c=1)

    >>> print (Ext.d.__doc__)
    Ext.d(self, a, b, *, c=88)

    >>> print (Ext.e.__doc__)
    Ext.e(self, a, b, c=88, **kwds)

    >>> print (Ext.f.__doc__)
    Ext.f(self, a, b, *, c, d=42)

    >>> print (Ext.g.__doc__)
    Ext.g(self, a, b, *, c, d=42, e=17, f, **kwds)

    >>> print (Ext.h.__doc__)
    Ext.h(self, a, b, *args, c, d=42, e=17, f, **kwds)

    >>> print (Ext.k.__doc__)
    Ext.k(self, a, b, c=1, *args, d=42, e=17, f, **kwds)

    >>> print (Ext.l.__doc__)
    Ext.l(self, a, b, c=1, *args, d=42, e=17, f, **kwds)
    Existing string

    >>> print (Ext.m.__doc__)
    Ext.m(self, a='spam', b='foo', c=b'bar')

    >>> print (Ext.n.__doc__)
    Ext.n(self, a: int, b: float = 1.0, *args: tuple, **kwargs: dict) -> (None, True)

    >>> print (Ext.o.__doc__)
    Ext.o(self, a, b=1, /, c=5, *args, **kwargs)

    >>> print (Ext.__add__.__doc__)
    Ext.__add__(self, Ext other) -> Ext
    add docstring

    >>> print (Ext.get_int.__doc__)
    Ext.get_int(self) -> int

    >>> print (Ext.get_float.__doc__)
    Ext.get_float(self) -> float

    >>> print (Ext.get_str.__doc__)
    Ext.get_str(self) -> str
    Existing string

    >>> print (Ext.clone.__doc__)
    Ext.clone(self) -> Ext

    >>> print (funcdoc(foo))
    foo()

    >>> funcdoc(with_doc_1)
    'with_doc_1(a, b, c)\nExisting string'

    >>> funcdoc(with_doc_2)
    'with_doc_2(a, b, c)\nExisting string'

    >>> funcdoc(with_doc_3)
    'with_doc_3(a, b, c)\nExisting string'

    >>> funcdoc(with_doc_4)
    'with_doc_4(int a, str b, list c) -> str\nExisting string'

    >>> funcdoc(f_sd)
    "f_sd(str s='spam')"

    >>> funcdoc(cf_sd)
    "cf_sd(str s='spam') -> str"

    >>> funcdoc(types)
    'types(Ext a, int b, unsigned short c, float d, e)'

    >>> print(funcdoc(f_c))
    f_c(char c) -> char

    >>> print(funcdoc(f_uc))
    f_uc(unsigned char c) -> unsigned char

    >>> print(funcdoc(f_sc))
    f_sc(signed char c) -> signed char

    >>> print(funcdoc(f_s))
    f_s(short s) -> short

    >>> print(funcdoc(f_us))
    f_us(unsigned short s) -> unsigned short


    >>> print(funcdoc(f_i))
    f_i(int i) -> int

    >>> print(funcdoc(f_ui))
    f_ui(unsigned int i) -> unsigned int

    >>> print(funcdoc(f_bint))
    f_bint(bool i) -> bool


    >>> print(funcdoc(f_l))
    f_l(long l) -> long

    >>> print(funcdoc(f_ul))
    f_ul(unsigned long l) -> unsigned long


    >>> print(funcdoc(f_L))
    f_L(long long L) -> long long

    >>> print(funcdoc(f_uL))
    f_uL(unsigned long long L) -> unsigned long long


    >>> print(funcdoc(f_f))
    f_f(float f) -> float

    >>> print(funcdoc(f_d))
    f_d(double d) -> double

    >>> print(funcdoc(f_D))
    f_D(long double D) -> long double

    >>> print(funcdoc(f_my_i))
    f_my_i(MyInt i) -> MyInt

    >>> print(funcdoc(f_my_f))
    f_my_f(MyFloat f) -> MyFloat

    >>> print(funcdoc(f_defexpr1))
    f_defexpr1(int x=FLAG1, int y=FLAG2)

    >>> print(funcdoc(f_defexpr2))
    f_defexpr2(int x=FLAG1 | FLAG2, y=FLAG1 & FLAG2)

    >>> print(funcdoc(f_defexpr3))
    f_defexpr3(int x=Ext.CONST1, f=__builtins__.abs)

    >>> print(funcdoc(f_defexpr4))
    f_defexpr4(int x=(Ext.CONST1 + FLAG1) * Ext.CONST2)

    >>> print(funcdoc(f_defexpr5))
    f_defexpr5(int x=2 + 2)

    >>> print(funcdoc(f_charptr_null))
    f_charptr_null(char *s=NULL) -> char *
"""


@skip_if_limited_api("known bugs")
def test_nonlimited_api():
    """
    >>> print (Ext.__call__.__doc__)
    Ext.__call__(self, a: int, b: float = 1.0, *args: tuple, **kwargs: dict) -> (None, True)
    call docstring
    """

cdef class Ext:

    cdef public int  attr0
    """attr0 docstring"""
    cdef public      attr1
    """attr1 docstring"""
    cdef public list attr2
    cdef public Ext attr3

    """NOT attr3 docstring"""
    cdef        int  attr4
    cdef public int \
        attr5
    """attr5 docstring"""

    CONST1, CONST2 = 1, 2

    property prop0:
        """prop0 docstring"""
        def __get__(self):
            return self.attr0

    property prop1:
        def __get__(self):
            return self.attr1

    property attr4:
        """attr4 docstring"""
        def __get__(self):
            return self.attr4

    def __init__(self, a, b, c=None):
        pass

    def a(self):
        pass

    def b(self, a, b, c):
        pass

    def c(self, a, b, c=1):
        pass

    def d(self, a, b, *, c = 88):
        pass

    def e(self, a, b, c = 88, **kwds):
        pass

    def f(self, a, b, *, c, d = 42):
        pass

    def g(self, a, b, *, c, d = 42, e = 17, f, **kwds):
        pass

    def h(self, a, b, *args, c, d = 42, e = 17, f, **kwds):
        pass

    def k(self, a, b, c=1, *args, d = 42, e = 17, f, **kwds):
        pass

    def l(self, a, b, c=1, *args, d = 42, e = 17, f, **kwds):
        """Existing string"""
        pass

    def m(self, a=u'spam', b='foo', c=b'bar'):
        pass

    def n(self, a: int, b: float = 1.0, *args: tuple, **kwargs: dict) -> (None, True):
        pass

    def o(self, a, b=1, /, c=5, *args, **kwargs):
        pass

    def __call__(self, a: int, b: float = 1.0, *args: tuple, **kwargs: dict) -> (None, True):
        """
        call docstring
        """
        pass

    def __add__(self, Ext other) -> Ext:
        """
        add docstring
        """
        return self

    cpdef int get_int(self):
        return 0

    cpdef float get_float(self):
        return 0.0

    cpdef str get_str(self):
        """Existing string"""
        return "string"

    cpdef Ext clone(self):
        return Ext(1,2)

def foo():
    pass

def types(Ext a, int b, unsigned short c, float d, e):
    pass

def with_doc_1(a, b, c):
    """Existing string"""
    pass

def with_doc_2(a, b, c):
    """
    Existing string
    """
    pass

cpdef with_doc_3(a, b, c):
    """Existing string"""
    pass

cpdef str with_doc_4(int a, str b, list c):
    """
    Existing string
    """
    return b

def f_sd(str s='spam'):
    return s

cpdef str cf_sd(str s='spam'):
    return s

cpdef char f_c(char c):
    return c

cpdef unsigned char f_uc(unsigned char c):
    return c

cpdef signed char f_sc(signed char c):
    return c


cpdef short f_s(short s):
    return s

cpdef unsigned short f_us(unsigned short s):
    return s


cpdef int f_i(int i):
    return i

cpdef unsigned int f_ui(unsigned int i):
    return i

cpdef bint f_bint(bint i):
    return i


cpdef long f_l(long l):
    return l

cpdef unsigned long f_ul(unsigned long l):
    return l


cpdef long long f_L(long long L):
    return L

cpdef unsigned long long f_uL(unsigned long long L):
    return L


cpdef float f_f(float f):
    return f

cpdef double f_d(double d):
    return d

cpdef long double f_D(long double D):
    return D

ctypedef int MyInt
cpdef MyInt f_my_i(MyInt i):
    return i

ctypedef float MyFloat
cpdef MyFloat f_my_f(MyFloat f):
    return f

cdef enum:
    FLAG1
    FLAG2

cpdef f_defexpr1(int x = FLAG1, int y = FLAG2):
    pass

cpdef f_defexpr2(int x = FLAG1 | FLAG2, y = FLAG1 & FLAG2):
    pass

cpdef f_defexpr3(int x = Ext.CONST1, f = __builtins__.abs):
    pass

cpdef f_defexpr4(int x = (Ext.CONST1 + FLAG1) * Ext.CONST2):
    pass

cpdef f_defexpr5(int x = 2+2):
    pass

cpdef (char*) f_charptr_null(char* s=NULL):
    return s or b'abc'


# no signatures for lambda functions
lambda_foo = lambda x: 10
lambda_bar = lambda x: 20


cdef class Foo:
    def __init__(self, *args, **kwargs): pass
    def m00(self, a: None) ->  None: pass
    def m01(self, a: ...) ->  Ellipsis: pass
    def m02(self, a: True, b: False) ->  bool: pass
    def m03(self, a: 42, b: +42, c: -42) ->  int : pass  # XXX +42 -> 42
    def m04(self, a: 3.14, b: +3.14, c: -3.14) -> float : pass
    def m05(self, a: 1 + 2j, b: +2j, c: -2j) -> complex : pass
    def m06(self, a: "abc", b: b"abc", c: u"abc") -> (str, bytes, unicode) : pass
    def m07(self, a: [1, 2, 3], b: []) -> list: pass
    def m08(self, a: (1, 2, 3), b: ()) -> tuple: pass
    def m09(self, a: {1, 2, 3}, b: {i for i in ()}) -> set: pass
    def m10(self, a: {1: 1, 2: 2, 3: 3}, b: {}) -> dict: pass
   #def m11(self, a: [str(i) for i in range(3)]): pass  # Issue 1782
    def m12(self, a: (str(i) for i in range(3))): pass
    def m13(self, a: (str(i) for i in range(3) if bool(i))): pass
    def m14(self, a: {str(i) for i in range(3)}): pass
    def m15(self, a: {str(i) for i in range(3) if bool(i)}): pass
    def m16(self, a: {str(i): id(i) for i in range(3)}): pass
    def m17(self, a: {str(i): id(i) for i in range(3) if bool(i)}): pass
    def m18(self, a: dict.update(x=42, **dict(), **{})): pass
    def m19(self, a: sys is None, b: sys is not None): pass
    def m20(self, a: sys in [], b: sys not in []): pass
    def m21(self, a: (sys or sys) and sys, b: not (sys or sys)): pass
    def m22(self, a: 42 if sys else None): pass
    def m23(self, a: +int(), b: -int(), c: ~int()): pass
    def m24(self, a: (1+int(2))*3+(4*int(5))**(1+0.0/1)): pass
    def m25(self, a: list(range(3))[:]): pass
    def m26(self, a: list(range(3))[1:]): pass
    def m27(self, a: list(range(3))[:1]): pass
    def m28(self, a: list(range(3))[::1]): pass
    def m29(self, a: list(range(3))[0:1:1]): pass
    def m30(self, a: list(range(3))[7, 3:2:1, ...]): pass
    def m31(self, double[::1] a): pass
    def m32(self, a: tuple[()]) -> tuple[tuple[()]]: pass

__doc__ += ur"""
>>> print(Foo.__doc__)
Foo(*args, **kwargs)
>>> assert Foo.__init__.__doc__ == type.__init__.__doc__

>>> print(Foo.m00.__doc__)
Foo.m00(self, a: None) -> None

>>> print(Foo.m01.__doc__)
Foo.m01(self, a: ...) -> Ellipsis

>>> print(Foo.m02.__doc__)
Foo.m02(self, a: True, b: False) -> bool

>>> print(Foo.m03.__doc__)
Foo.m03(self, a: 42, b: +42, c: -42) -> int

>>> print(Foo.m04.__doc__)
Foo.m04(self, a: 3.14, b: +3.14, c: -3.14) -> float

>>> print(Foo.m05.__doc__)
Foo.m05(self, a: 1 + 2j, b: +2j, c: -2j) -> complex

>>> print(Foo.m06.__doc__)
Foo.m06(self, a: 'abc', b: b'abc', c: 'abc') -> (str, bytes, unicode)

>>> print(Foo.m07.__doc__)
Foo.m07(self, a: [1, 2, 3], b: []) -> list

>>> print(Foo.m08.__doc__)
Foo.m08(self, a: (1, 2, 3), b: ()) -> tuple

>>> print(Foo.m09.__doc__)
Foo.m09(self, a: {1, 2, 3}, b: {i for i in ()}) -> set

>>> print(Foo.m10.__doc__)
Foo.m10(self, a: {1: 1, 2: 2, 3: 3}, b: {}) -> dict

# >>> print(Foo.m11.__doc__)
# Foo.m11(self, a: [str(i) for i in range(3)])

>>> print(Foo.m12.__doc__)
Foo.m12(self, a: (str(i) for i in range(3)))

>>> print(Foo.m13.__doc__)
Foo.m13(self, a: (str(i) for i in range(3) if bool(i)))

>>> print(Foo.m14.__doc__)
Foo.m14(self, a: {str(i) for i in range(3)})

>>> print(Foo.m15.__doc__)
Foo.m15(self, a: {str(i) for i in range(3) if bool(i)})

>>> print(Foo.m16.__doc__)
Foo.m16(self, a: {str(i): id(i) for i in range(3)})

>>> print(Foo.m17.__doc__)
Foo.m17(self, a: {str(i): id(i) for i in range(3) if bool(i)})

>>> print(Foo.m18.__doc__)
Foo.m18(self, a: dict.update(x=42, **dict()))

>>> print(Foo.m19.__doc__)
Foo.m19(self, a: sys is None, b: sys is not None)

>>> print(Foo.m20.__doc__)
Foo.m20(self, a: sys in [], b: sys not in [])

>>> print(Foo.m21.__doc__)
Foo.m21(self, a: (sys or sys) and sys, b: not (sys or sys))

>>> print(Foo.m22.__doc__)
Foo.m22(self, a: 42 if sys else None)

>>> print(Foo.m23.__doc__)
Foo.m23(self, a: +int(), b: -int(), c: ~int())

>>> print(Foo.m24.__doc__)
Foo.m24(self, a: (1 + int(2)) * 3 + (4 * int(5)) ** (1 + 0.0 / 1))

>>> print(Foo.m25.__doc__)
Foo.m25(self, a: list(range(3))[:])

>>> print(Foo.m26.__doc__)
Foo.m26(self, a: list(range(3))[1:])

>>> print(Foo.m27.__doc__)
Foo.m27(self, a: list(range(3))[:1])

>>> print(Foo.m28.__doc__)
Foo.m28(self, a: list(range(3))[::1])

>>> print(Foo.m29.__doc__)
Foo.m29(self, a: list(range(3))[0:1:1])

>>> print(Foo.m30.__doc__)
Foo.m30(self, a: list(range(3))[7, 3:2:1, ...])

>>> print(Foo.m31.__doc__)
Foo.m31(self, double[::1] a)

>>> print(Foo.m32.__doc__)
Foo.m32(self, a: tuple[()]) -> tuple[tuple[()]]

"""
