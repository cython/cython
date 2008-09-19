#cython: embedsignature=True

# note the r, we use \n below
__doc__ = ur"""
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

    >>> print (Ext.get_int.__doc__)
    Ext.get_int(self) -> int

    >>> print (Ext.get_float.__doc__)
    Ext.get_float(self) -> float

    >>> print (Ext.clone.__doc__)
    Ext.clone(self) -> Ext

    >>> print (foo.__doc__)
    foo()

    >>> with_doc_1.__doc__
    'with_doc_1(a, b, c)\nExisting string'

    >>> with_doc_2.__doc__
    'with_doc_2(a, b, c)\n\n    Existing string\n    '

    >>> types.__doc__
    'types(Ext a, int b, int c, float d, e)'

"""

cdef class Ext:

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

    cpdef int get_int(self):
        return 0

    cpdef float get_float(self):
        return 0.0

    cpdef Ext clone(self):
        return Ext()

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
