cdef int raise_py_error() except *:
    raise TypeError("custom")

cdef extern from "cpp_exceptions_helper.h":
    cdef int raise_int_raw "raise_int"(bint fire) except +
    cdef int raise_int_value "raise_int"(bint fire) except +ValueError
    cdef int raise_int_custom "raise_int"(bint fire) except +raise_py_error
    
    cdef int raise_index_raw "raise_index"(bint fire) except +
    cdef int raise_index_value "raise_index"(bint fire) except +ValueError
    cdef int raise_index_custom "raise_index"(bint fire) except +raise_py_error

def test_int_raw(bint fire):
    """
    >>> test_int_raw(False)
    >>> test_int_raw(True)
    Traceback (most recent call last):
    ...
    RuntimeError: Unknown exception
    """
    raise_int_raw(fire)

def test_int_value(bint fire):
    """
    >>> test_int_value(False)
    >>> test_int_value(True)
    Traceback (most recent call last):
    ...
    ValueError
    """
    raise_int_value(fire)

def test_int_custom(bint fire):
    """
    >>> test_int_custom(False)
    >>> test_int_custom(True)
    Traceback (most recent call last):
    ...
    TypeError: custom
    """
    raise_int_custom(fire)

def test_index_raw(bint fire):
    """
    >>> test_index_raw(False)
    >>> test_index_raw(True)
    Traceback (most recent call last):
    ...
    IndexError: c++ error
    """
    raise_index_raw(fire)

def test_index_value(bint fire):
    """
    >>> test_index_value(False)
    >>> test_index_value(True)
    Traceback (most recent call last):
    ...
    ValueError: c++ error
    """
    raise_index_value(fire)

def test_index_custom(bint fire):
    """
    >>> test_index_custom(False)
    >>> test_index_custom(True)
    Traceback (most recent call last):
    ...
    TypeError: custom
    """
    raise_index_custom(fire)
