# mode: run
# tag: cpp, cpp11

from libcpp.exception cimport (
    exception_ptr,
    exception_ptr_error_handler,
    make_exception_ptr,
    rethrow_exception,
    wrapped_exception_ptr_from_exception,
)

cdef extern from *:
    """
    void raise_runtime_error() {
        throw std::runtime_error("hello");
    }
    """
    void raise_runtime_error() except +exception_ptr_error_handler

cdef extern from "<stdexcept>" namespace "std" nogil:
    cdef cppclass runtime_error:
        runtime_error(const char* s)

def test_custom_error_handler():
    """
    >>> test_custom_error_handler()
    """
    cdef exception_ptr eptr
    try:
        raise_runtime_error()
    except Exception as e:
        eptr = wrapped_exception_ptr_from_exception(e)
        assert eptr
        try:
            rethrow_exception(eptr)
        except RuntimeError as re:  # normal Cython error conversion
            assert re.args[0] == "hello"
        else:
            assert False
    else:
        assert False

def test_make_directly():
    """
    >>> test_make_directly()
    """
    eptr = make_exception_ptr(runtime_error("I'm an error"))
    try:
        rethrow_exception(eptr)
    except RuntimeError as re:
        assert re.args[0] == "I'm an error"
    else:
        assert False
