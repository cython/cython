# mode: run
# tag: cyfunction, fused
# cython: binding=True

import platform
import sys


cdef extern from *:
    """
    static int __Pyx_InitAfterSharedUtility(void);
    static int __pyx_CyFunction_init(PyObject *module);
    static int __pyx_FusedFunction_init(PyObject *module);
    """
    int __Pyx_InitAfterSharedUtility() except -1
    int __pyx_CyFunction_init(object module) except -1
    int __pyx_FusedFunction_init(object module) except -1


def regular(value):
    return value


ctypedef fused numeric:
    int
    double


def fused(numeric value):
    return value


def repeat_init(int count, bint direct=False):
    module = sys.modules[__name__]
    cyfunction_type = type(regular)
    fused_function_type = type(fused)
    before = sys.getrefcount(cyfunction_type), sys.getrefcount(fused_function_type)
    for _ in range(count):
        if direct:
            __pyx_CyFunction_init(module)
            __pyx_FusedFunction_init(module)
        else:
            __Pyx_InitAfterSharedUtility()
    return (sys.getrefcount(cyfunction_type) - before[0],
            sys.getrefcount(fused_function_type) - before[1])


# Downstream code may call the helper before the generated module initializer does.
# Skip for PyPy and GraalPy, where reference counting is unreliable.
if platform.python_implementation() not in ("PyPy", "GraalVM"):
    __doc__ = """
    >>> repeat_init(10)
    (0, 0)
    >>> repeat_init(10, direct=True)
    (0, 0)
    >>> regular(123)
    123
    >>> fused(123)
    123
    >>> fused(1.5)
    1.5
    """
