# mode: run
# tag: directive, cpdef

cimport cython


# --- Default behavior: Python override still works ---

cdef class DefaultClass:
    cpdef int method(self):
        return 1

class _PySub(DefaultClass):
    def method(self):
        return 2

def test_default_override():
    """
    >>> test_default_override()
    2
    """
    return _PySub().method()


# --- python_subclassing=False: no OverrideCheckNode emitted ---

@cython.python_subclassing(False)
cdef class NoDispatchClass:
    """
    >>> NoDispatchClass().method()
    1
    """
    @cython.test_fail_if_path_exists("//OverrideCheckNode")
    cpdef int method(self):
        return 1


# --- python_subclassing=False: TypeError at pure Python subclass creation ---

@cython.python_subclassing(False)
cdef class NoSubclass:
    """
    >>> try:
    ...     class S(NoSubclass): pass
    ... except TypeError:
    ...     print("ok")
    ok
    """
    cpdef int method(self):
        return 1


# --- Cython cclass subclassing still works when base has python_subclassing=False ---

@cython.python_subclassing(False)
cdef class BaseC:
    cpdef int method(self):
        return 1

cdef class CythonChild(BaseC):
    """
    >>> CythonChild().method()
    2
    """
    cpdef int method(self):
        return 2


# --- python_subclassing=False on subclass doesn't affect base ---

cdef class BaseWithDispatch:
    cpdef int method(self):
        return 10

@cython.python_subclassing(False)
cdef class DerivedNoDispatch(BaseWithDispatch):
    """
    >>> DerivedNoDispatch().method()
    20
    """
    @cython.test_fail_if_path_exists("//OverrideCheckNode")
    cpdef int method(self):
        return 20
