# cython: binding=True, language_level=3
# mode: run
# tag: cyfunction

import inspect

try:
    sig = inspect.Signature.from_callable
except AttributeError:
    sig = inspect.Signature.from_function


def signatures_match(f1, f2):
    if sig(f1) == sig(f2):
        return None  # nothing to show in doctest
    return sig(f1), sig(f2)


def b(a, b, c):
    """
    >>> def py_b(a, b, c): pass
    >>> signatures_match(b, py_b)
    """


def c(a, b, c=1):
    """
    >>> def py_c(a, b, c=1): pass
    >>> signatures_match(c, py_c)
    """


def d(a, b, *, c = 88):
    """
    >>> def py_d(a, b, *, c = 88): pass
    >>> signatures_match(d, py_d)
    """


def e(a, b, c = 88, **kwds):
    """
    >>> def py_e(a, b, c = 88, **kwds): pass
    >>> signatures_match(e, py_e)
    """


def f(a, b, *, c, d = 42):
    """
    >>> def py_f(a, b, *, c, d = 42): pass
    >>> signatures_match(f, py_f)
    """


def g(a, b, *, c, d = 42, e = 17, f, **kwds):
    """
    >>> def py_g(a, b, *, c, d = 42, e = 17, f, **kwds): pass
    >>> signatures_match(g, py_g)
    """


def h(a, b, *args, c, d = 42, e = 17, f, **kwds):
    """
    >>> def py_h(a, b, *args, c, d = 42, e = 17, f, **kwds): pass
    >>> signatures_match(h, py_h)
    """


def k(a, b, c=1, *args, d = 42, e = 17, f, **kwds):
    """
    >>> def py_k(a, b, c=1, *args, d = 42, e = 17, f, **kwds): pass
    >>> signatures_match(k, py_k)
    """


def l(*, a, b, c = 88):
    """
    >>> def py_l(*, a, b, c = 88): pass
    >>> signatures_match(l, py_l)
    """


def m(a, *, b, c = 88):
    """
    >>> def py_m(a, *, b, c = 88): pass
    >>> signatures_match(m, py_m)
    """
    a, b, c = b, c, a


def n(a, *, b, c = 88):
    """
    >>> def py_n(a, *, b, c = 88): pass
    >>> signatures_match(n, py_n)
    """


cpdef cp1(a, b):
    """
    >>> def py_cp1(a, b): pass
    >>> signatures_match(cp1, py_cp1)
    """


# Currently broken, see GH #1864
cpdef cp2(a, b=True):
    """
    >>> def py_cp2(a, b=True): pass

    #>>> signatures_match(cp2, py_cp2)
    """


# Currently broken, see GH #1864
cpdef cp3(a=1, b=True):
    """
    >>> def py_cp3(a=1, b=True): pass

    #>>> signatures_match(cp3, py_cp3)
    """
