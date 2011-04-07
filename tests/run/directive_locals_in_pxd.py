import cython

def foo(egg):
    if not cython.compiled:
        egg = float(egg)
    return egg

def foo_defval(egg=1):
    if not cython.compiled:
        egg = float(egg)
    return egg**2

def cpfoo(egg=False):
    if not cython.compiled:
        egg = bool(egg)
        v = int(not egg)
    else:
        v = not egg
    return egg, v

def test_pxd_locals():
    """
    >>> v1, v2, v3 = test_pxd_locals()
    >>> isinstance(v1, float)
    True
    >>> isinstance(v2, float)
    True
    >>> v3
    (True, 0)
    """
    return foo(1), foo_defval(), cpfoo(1)
