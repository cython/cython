# mode: run
# tag: cyfunction, fused
# cython: binding=True

import platform
import sys


cdef extern from *:
    """
    static int __Pyx_InitAfterSharedUtility(void);
    """
    int __Pyx_InitAfterSharedUtility() except -1


def regular(value):
    return value


ctypedef fused numeric:
    int
    double


def fused(numeric value):
    return value


def repeat_init(int count):
    cyfunction_type = type(regular)
    fused_function_type = type(fused)
    before = sys.getrefcount(cyfunction_type), sys.getrefcount(fused_function_type)
    for _ in range(count):
        __Pyx_InitAfterSharedUtility()
    return (sys.getrefcount(cyfunction_type) - before[0],
            sys.getrefcount(fused_function_type) - before[1])


# Downstream code may call the helper before the generated module initializer does.
# Skip for PyPy and GraalPy, where reference counting is unreliable.
if platform.python_implementation() not in ("PyPy", "GraalVM"):
    __doc__ = """
    >>> repeat_init(10)
    (0, 0)
    >>> regular(123)
    123
    >>> fused(123)
    123
    >>> fused(1.5)
    1.5
    """
