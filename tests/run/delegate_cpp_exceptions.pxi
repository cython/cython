from libcpp.exception cimport delegate_to_exception_handlers, runtime_error, logic_error

# Customize the module to simplify formatting for doctest
# because we re-use this include under a couple of different names.
class MyRuntimeError(Exception):
    __module__ = "x"

class MyLogicError(Exception):
    __module__ = "x"

class MyFallbackError(Exception):
    __module__ = "x"

cdef void maybe_handle_runtime_error(const runtime_error& e) except*:
    cdef bytes s = e.what()
    if len(s) > 20:
        raise MyRuntimeError("long message")
    # else unhandled

cdef void always_handle_runtime_error(const runtime_error& e) except*:
    raise MyRuntimeError(e.what().decode("ascii"))

cdef void handle_logic_error(const logic_error& e) except*:
    raise MyLogicError(e.what().decode("ascii"))

cdef void fallback_handler() except*:
    raise MyFallbackError("Don't know what happened but it was bad")

cdef void handler_with_fallback() except*:
    # deliberate mixture of & and no-& 
    delegate_to_exception_handlers(&maybe_handle_runtime_error, &always_handle_runtime_error, handle_logic_error, &fallback_handler)

cdef void handler_no_fallback() except*:
    # deliberate mixture of & and no-&
    delegate_to_exception_handlers(&maybe_handle_runtime_error, always_handle_runtime_error, handle_logic_error)


cdef extern from *:
    """
    void raise_some_cpp_error(int what) {
        if (what == 0) {
            throw std::runtime_error("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
        } else if (what == 1) {
            throw std::runtime_error("Bad");
        } else if (what == 2) {
            throw std::logic_error("Illogical");
        } else if (what == 3) {
            // Derived from logic error
            throw std::out_of_range("out of range");
        } else {
            throw std::bad_alloc();
        }
    }
    """
    void raise_some_cpp_error1 "raise_some_cpp_error"(int what) except +handler_with_fallback
    void raise_some_cpp_error2 "raise_some_cpp_error"(int what) except +handler_no_fallback


def test_with_fallback(int what):
    """
    >>> test_with_fallback(0)
    Traceback (most recent call last):
        ...
    x.MyRuntimeError: long message
    >>> test_with_fallback(1)
    Traceback (most recent call last):
        ...
    x.MyRuntimeError: Bad
    >>> test_with_fallback(2)
    Traceback (most recent call last):
        ...
    x.MyLogicError: Illogical
    >>> test_with_fallback(3)
    Traceback (most recent call last):
        ...
    x.MyLogicError: out of range
    >>> test_with_fallback(4)
    Traceback (most recent call last):
        ...
    x.MyFallbackError: Don't know what happened but it was bad
    """
    raise_some_cpp_error1(what)

def test_no_fallback(int what):
    """
    >>> test_no_fallback(0)
    Traceback (most recent call last):
        ...
    x.MyRuntimeError: long message
    >>> test_no_fallback(1)
    Traceback (most recent call last):
        ...
    x.MyRuntimeError: Bad
    >>> test_no_fallback(2)
    Traceback (most recent call last):
        ...
    x.MyLogicError: Illogical
    >>> test_no_fallback(3)
    Traceback (most recent call last):
        ...
    x.MyLogicError: out of range

    This is the difference compare to "test_with_fallback".
    In this case we revert to Cython's standard handling.
    >>> test_no_fallback(4)
    Traceback (most recent call last):
        ...
    MemoryError: std::bad_alloc
    """
    raise_some_cpp_error2(what)

def test_misuse_handler():
    """
    >>> test_misuse_handler()
    Traceback (most recent call last):
        ...
    SystemError: __pyx_delegrate_to_exception_handlers called without a C++ exception
    """
    handler_with_fallback()
