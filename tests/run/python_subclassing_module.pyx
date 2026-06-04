# cython: python_subclassing=False
# mode: run
# tag: directive, cpdef

cimport cython


# Module-level directive disables dispatch for all cclasses in this file

cdef class ModuleLevel:
    """
    >>> try:
    ...     class S(ModuleLevel): pass
    ... except TypeError:
    ...     print("ok")
    ok
    >>> ModuleLevel().method()
    1
    """
    @cython.test_fail_if_path_exists("//OverrideCheckNode")
    cpdef int method(self):
        return 1


# Per-class override back to True

@cython.python_subclassing(True)
cdef class OverrideToTrue:
    """
    >>> _sub = _SubOverride()
    >>> _sub.method()
    99
    """
    cpdef int method(self):
        return 1

class _SubOverride(OverrideToTrue):
    def method(self):
        return 99
