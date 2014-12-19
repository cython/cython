#cython: embedsignature=True

import sys

if sys.version_info >= (3, 4):
    def funcdoc(f):
        if not f.__text_signature__:
            return f.__doc__
        doc = '%s%s' % (f.__name__, f.__text_signature__)
        if f.__doc__:
            if '\n' in f.__doc__:
                # preceding line endings get stripped
                doc = '%s\n\n%s' % (doc, f.__doc__)
            else:
                doc = '%s\n%s' % (doc, f.__doc__)
        return doc

else:
    def funcdoc(f):
        return f.__doc__


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
    Ext.m(self, a=u'spam')

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
    'with_doc_2(a, b, c)\n\n    Existing string\n    '

    >>> funcdoc(with_doc_3)
    'with_doc_3(a, b, c)\nExisting string'

    >>> funcdoc(with_doc_4)
    'with_doc_4(int a, str b, list c) -> str\n\n    Existing string\n    '

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

    >>> print(funcdoc(f_ss))
    f_ss(signed short s) -> signed short


    >>> print(funcdoc(f_i))
    f_i(int i) -> int

    >>> print(funcdoc(f_ui))
    f_ui(unsigned int i) -> unsigned int

    >>> print(funcdoc(f_si))
    f_si(signed int i) -> signed int

    >>> print(funcdoc(f_bint))
    f_bint(bool i) -> bool


    >>> print(funcdoc(f_l))
    f_l(long l) -> long

    >>> print(funcdoc(f_ul))
    f_ul(unsigned long l) -> unsigned long

    >>> print(funcdoc(f_sl))
    f_sl(signed long l) -> signed long


    >>> print(funcdoc(f_L))
    f_L(long long L) -> long long

    >>> print(funcdoc(f_uL))
    f_uL(unsigned long long L) -> unsigned long long

    >>> print(funcdoc(f_sL))
    f_sL(signed long long L) -> signed long long


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
    f_defexpr5(int x=4)
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

    def m(self, a=u'spam'):
        pass

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

cpdef signed short f_ss(signed short s):
    return s


cpdef int f_i(int i):
    return i

cpdef unsigned int f_ui(unsigned int i):
    return i

cpdef signed int f_si(signed int i):
    return i

cpdef bint f_bint(bint i):
    return i


cpdef long f_l(long l):
    return l

cpdef unsigned long f_ul(unsigned long l):
    return l

cpdef signed long f_sl(signed long l):
    return l


cpdef long long f_L(long long L):
    return L

cpdef unsigned long long f_uL(unsigned long long L):
    return L

cpdef signed long long f_sL(signed long long L):
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
