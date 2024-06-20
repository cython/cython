# mode: run
# tag: cpp, werror

cdef int raise_py_error() except *:
    raise TypeError("custom")

cdef extern from "cpp_exceptions_helper.h":
    cdef int raise_int_raw "raise_int"(bint fire) except +
    cdef int raise_int_value "raise_int"(bint fire) except +ValueError
    cdef int raise_int_custom "raise_int"(bint fire) except +raise_py_error

    cdef int raise_index_raw "raise_index"(bint fire) except +
    cdef int raise_index_value "raise_index"(bint fire) except +ValueError
    cdef int raise_index_custom "raise_index"(bint fire) except +raise_py_error

    cdef void raise_domain_error() except +
    cdef void raise_ios_failure() except +
    cdef void raise_memory() except +
    cdef void raise_overflow() except +
    cdef void raise_range_error() except +
    cdef void raise_typeerror() except +
    cdef void raise_underflow() except +

    cdef raise_or_throw(bint py) except +
    cdef int raise_or_throw_int(bint py) except +*

    cdef cppclass Foo:
        int bar_raw "bar"(bint fire) except +
        int bar_value "bar"(bint fire) except +ValueError
        int bar_custom "bar"(bint fire) except +raise_py_error


def test_domain_error():
    """
    >>> test_domain_error()
    Traceback (most recent call last):
    ...
    ValueError: domain_error
    """
    raise_domain_error()

def test_ios_failure():
    """
    >>> try: test_ios_failure()
    ... except (IOError, OSError): pass
    """
    raise_ios_failure()

def test_memory():
    """
    >>> test_memory()
    Traceback (most recent call last):
    ...
    MemoryError
    """
    # Re-raise the exception without a description string because we can't
    # rely on the implementation-defined value of what() in the doctest.
    try:
        raise_memory()
    except MemoryError:
        raise MemoryError

def test_overflow():
    """
    >>> test_overflow()
    Traceback (most recent call last):
    ...
    OverflowError: overflow_error
    """
    raise_overflow()

def test_range_error():
    """
    >>> test_range_error()
    Traceback (most recent call last):
    ...
    ArithmeticError: range_error
    """
    raise_range_error()

def test_typeerror():
    """
    >>> test_typeerror()
    Traceback (most recent call last):
    ...
    TypeError
    """
    # Re-raise the exception without a description string because we can't
    # rely on the implementation-defined value of what() in the doctest.
    try:
        raise_typeerror()
    except TypeError:
        raise TypeError

def test_underflow():
    """
    >>> test_underflow()
    Traceback (most recent call last):
    ...
    ArithmeticError: underflow_error
    """
    raise_underflow()

def test_func_that_can_raise_or_throw(bint py):
    """
    >>> test_func_that_can_raise_or_throw(0)
    Traceback (most recent call last):
    ...
    RuntimeError: oopsie
    >>> test_func_that_can_raise_or_throw(1)
    Traceback (most recent call last):
    ...
    ValueError: oopsie
    """
    raise_or_throw(py)

def test_func_that_can_raise_or_throw_c_return(bint py):
    """
    >>> test_func_that_can_raise_or_throw_c_return(0)
    Traceback (most recent call last):
    ...
    RuntimeError: oopsie
    >>> test_func_that_can_raise_or_throw_c_return(1)
    Traceback (most recent call last):
    ...
    ValueError: oopsie
    """
    raise_or_throw_int(py)

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

def test_cppclass_method_raw(bint fire):
    """
    >>> test_cppclass_method_raw(False)
    >>> test_cppclass_method_raw(True)
    Traceback (most recent call last):
    ...
    RuntimeError: Unknown exception
    """
    foo = new Foo()
    try:
        foo.bar_raw(fire)
    finally:
        del foo

def test_cppclass_method_value(bint fire):
    """
    >>> test_cppclass_method_value(False)
    >>> test_cppclass_method_value(True)
    Traceback (most recent call last):
    ...
    ValueError
    """
    foo = new Foo()
    try:
        foo.bar_value(fire)
    finally:
        del foo

def test_cppclass_method_custom(bint fire):
    """
    >>> test_cppclass_method_custom(False)
    >>> test_cppclass_method_custom(True)
    Traceback (most recent call last):
    ...
    TypeError: custom
    """
    foo = new Foo()
    try:
        foo.bar_custom(fire)
    finally:
        del foo
