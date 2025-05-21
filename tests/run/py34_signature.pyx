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


lb = lambda a, b, c: None

def b(a, b, c):
    """
    >>> def py_b(a, b, c): pass
    >>> signatures_match(b, py_b)

    >>> py_lb = lambda a, b, c: None
    >>> signatures_match(lb, py_lb)
    """


lc = lambda a, b, c=1: None

def c(a, b, c=1):
    """
    >>> def py_c(a, b, c=1): pass
    >>> signatures_match(c, py_c)

    >>> py_lc = lambda a, b, c=1: None
    >>> signatures_match(lc, py_lc)
    """


ld = lambda a, b, *, c = 88: None

def d(a, b, *, c = 88):
    """
    >>> def py_d(a, b, *, c = 88): pass
    >>> signatures_match(d, py_d)


    >>> py_ld = lambda a, b, *, c = 88: None
    >>> signatures_match(ld, py_ld)
    """


le = lambda a, b, c = 88, **kwds: None

def e(a, b, c = 88, **kwds):
    """
    >>> def py_e(a, b, c = 88, **kwds): pass
    >>> signatures_match(e, py_e)

    >>> py_le = lambda a, b, c = 88, **kwds: None
    >>> signatures_match(le, py_le)
    """


lf = lambda a, b, *, c, d = 42: None

def f(a, b, *, c, d = 42):
    """
    >>> def py_f(a, b, *, c, d = 42): pass
    >>> signatures_match(f, py_f)

    >>> py_lf = lambda a, b, *, c, d = 42: None
    >>> signatures_match(lf, py_lf)
    """


lg = lambda a, b, *, c, d = 42, e = 17, f, **kwds: None

def g(a, b, *, c, d = 42, e = 17, f, **kwds):
    """
    >>> def py_g(a, b, *, c, d = 42, e = 17, f, **kwds): pass
    >>> signatures_match(g, py_g)

    >>> py_lg = lambda a, b, *, c, d = 42, e = 17, f, **kwds: None
    >>> signatures_match(lg, py_lg)
    """


lh = lambda a, b, *args, c, d = 42, e = 17, f, **kwds: None

def h(a, b, *args, c, d = 42, e = 17, f, **kwds):
    """
    >>> def py_h(a, b, *args, c, d = 42, e = 17, f, **kwds): pass
    >>> signatures_match(h, py_h)

    >>> py_lh = lambda a, b, *args, c, d = 42, e = 17, f, **kwds: None
    >>> signatures_match(lh, py_lh)
    """


lk = lambda a, b, c=1, *args, d = 42, e = 17, f, **kwds: None

def k(a, b, c=1, *args, d = 42, e = 17, f, **kwds):
    """
    >>> def py_k(a, b, c=1, *args, d = 42, e = 17, f, **kwds): pass
    >>> signatures_match(k, py_k)

    >>> py_lk = lambda a, b, c=1, *args, d = 42, e = 17, f, **kwds: None
    >>> signatures_match(lk, py_lk)
    """


ll = lambda *, a, b, c = 88: None

def l(*, a, b, c = 88):
    """
    >>> def py_l(*, a, b, c = 88): pass
    >>> signatures_match(l, py_l)

    >>> py_ll = lambda *, a, b, c = 88: None
    >>> signatures_match(ll, py_ll)
    """


lm = lambda a, *, b, c = 88: None

def m(a, *, b, c = 88):
    """
    >>> def py_m(a, *, b, c = 88): pass
    >>> signatures_match(m, py_m)

    >>> py_lm = lambda a, *, b, c = 88: None
    >>> signatures_match(lm, py_lm)
    """
    a, b, c = b, c, a


ln = lambda a, *, b, c = 88: None

def n(a, *, b, c = 88):
    """
    >>> def py_n(a, *, b, c = 88): pass
    >>> signatures_match(n, py_n)

    >>> py_ln = lambda a, *, b, c = 88: None
    >>> signatures_match(ln, py_ln)
    """


cpdef cp1(a, b):
    """
    >>> def py_cp1(a, b): pass
    >>> signatures_match(cp1, py_cp1)
    """


cpdef cp2(a, b=True):
    """
    >>> def py_cp2(a, b=True): pass

    >>> signatures_match(cp2, py_cp2)
    """


cpdef cp3(a=1, b=True):
    """
    >>> def py_cp3(a=1, b=True): pass

    >>> signatures_match(cp3, py_cp3)
    """
