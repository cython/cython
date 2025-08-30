# mode: run
# tag: cpp, cpp11

# Do not add to this test - it's to ensure that all the right utility code
# is generated for exception_ptr_error_handler *if we don't do any other C++ error handling*.

from libcpp.exception cimport exception_ptr_error_handler

cdef extern from *:
    """
    void thrower() {
        throw std::runtime_error("bad");
    }
    """
    void thrower() except +exception_ptr_error_handler

def test():
    """
    >>> test()  # doctest: +ELLIPSIS
    RuntimeError(<capsule object "std::exception_ptr wrapper" at ...)
    """
    try:
        thrower()
    except Exception as e:
        return e
