# distutils: language = c++

from libcpp.exception cimport runtime_error, delegate_to_exception_handlers

class MyRuntimeError(Exception):
    pass

class UnknownError(Exception):
    pass

# Handlers for individual exceptions
cdef void handle_runtime_error(const runtime_error& e) except*:
    raise MyRuntimeError(e.what().decode("ascii"))

cdef void handle_anything() except*:
    raise UnknownError

# Overall exception handler mechanism
cdef void custom_exception_handler() except*:
    delegate_to_exception_handlers(handle_runtime_error, handle_anything)

cdef extern from *:
    """
    void may_raise() {
        /* implementation goes here */
    }
    """
    void may_raise() except +custom_exception_handler

def call_may_raise():
    may_raise()
