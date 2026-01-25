# mode: run

import sys
import platform

# For heaptypes the type of an instance is reference counted
# and creating and destroying an instance should leave the reference count
# unchanged.
# For static types the type of an instance isn't reference counted
# so the test also works (but is less important because it's not our problem).

cdef class C:
    pass

cdef class D(C):
    pass

class E(C):
    pass

cdef class L(list):
    pass

# Skip for PyPy and GraalPy - refcounting is likely unreliable.
if not platform.python_implementation in ("PyPy", "GraalVM"):
    __doc__= """
    >>> old_refcount_c = sys.getrefcount(C)
    >>> x = [C() for _ in range(100)]
    >>> del x
    >>> assert old_refcount_c == sys.getrefcount(C)

    >>> old_refcount_d = sys.getrefcount(D)
    >>> x = [D() for _ in range(100)]
    >>> del x
    >>> assert old_refcount_d == sys.getrefcount(D)
    >>> assert old_refcount_c == sys.getrefcount(C)  # probably should be unaffected, but make sure.

    >>> old_refcount_e = sys.getrefcount(E)
    >>> x = [E() for _ in range(100)]
    >>> del x
    >>> assert old_refcount_e == sys.getrefcount(E)
    >>> assert old_refcount_c == sys.getrefcount(C)  # probably should be unaffected, but make sure.

    >>> old_refcount_l = sys.getrefcount(L)
    >>> x = [L() for _ in range(100)]
    >>> del x
    >>> assert old_refcount_l == sys.getrefcount(L)
    """
