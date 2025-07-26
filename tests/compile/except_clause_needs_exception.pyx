# mode: compile
# tag: cpp, cpp17, no-cpp-locals

# This test tests a small optimization for except clauses where they can
# potentially omit some exception handling code if sufficiently simple.
# The optimization is performed explicitly because it's completely
# unobservable. Therefore, it's hard to test behaviourally.
#
# Restrict to c++17 just because we use cpp_locals in the test.

cimport cython

cdef cppclass CppClass:
    int attr
    CppClass():
        pass

def return_empty():
    with cython.test_body_needs_exception_handling(False):
        return

def return_none():
    with cython.test_body_needs_exception_handling(False):
        return None

def return_int():
    with cython.test_body_needs_exception_handling(False):
        return 100

def return_str_literal():
    with cython.test_body_needs_exception_handling(False):
        return "I'm always in the module cache!"

def return_arg(arg):
    with cython.test_body_needs_exception_handling(False):
        return arg

def return_assigned():
    x = object()
    with cython.test_body_needs_exception_handling(False):
        return x

def result_maybe_unassigned(arg):
    if arg:
        x = object
    with cython.test_body_needs_exception_handling(True):
        return x

py_global = None
cdef int c_global = 0

def return_py_global():
    with cython.test_body_needs_exception_handling(True):
        return py_global

def return_c_global():
    with cython.test_body_needs_exception_handling(True):
        return c_global

def test_pass():
    with cython.test_body_needs_exception_handling(False):
        pass

cdef void noexcept_func() noexcept:
    pass

def call_noexcept_func():
    with cython.test_body_needs_exception_handling(True):
        noexcept_func()

def test_assignment(arg):
    global py_global, c_global

    cdef str typed_as_string = "hello"

    cdef list this_is_a_list = []

    some_value = 5
    with cython.test_body_needs_exception_handling(False):
        a = 2
        b = None
        c = some_value
        d = arg
        typed_as_string = "goodbye"  # string destructor is safe

    if arg:
        some_other_value = object()
    cdef float some_c_value = 0.0
    with cython.test_body_needs_exception_handling(True):
        e = some_other_value
    with cython.test_body_needs_exception_handling(False):
        # Re-assignment of Python or C objects isn't a problem.
        # We're treating it as undefined if the destructor gets called
        # during the exception handler.
        some_other_value = None  # may call destructor
        some_c_value = 1.0  # no destructor
    with cython.test_body_needs_exception_handling(True):
        this_is_a_list = arg  # type-check
    with cython.test_body_needs_exception_handling(True):
        py_global = True
    with cython.test_body_needs_exception_handling(False):
        c_global = 1

    cdef CppClass cpp_instance1
    cdef CppClass cpp_instance2

    with cython.test_body_needs_exception_handling(True):
        cpp_instance1 = cpp_instance2  # operator= can be non-trivial

def test_memoryview_assignment(obj):
    cdef int[:] obj_view = obj
    cdef int[:] uninitialized_view
    cdef int[:] a, b, c

    with cython.test_body_needs_exception_handling(True):
        a = obj  # this can fail
    
    with cython.test_body_needs_exception_handling(False):
        b = obj_view
        # `a` may call destructor on re-assignment but we're
        # treating that as implementation-defined.
        a = obj_view

cdef class CClass:
    cdef int x
    cdef object y
    cdef int[:] z

def test_attr_assignment(CClass arg):
    cdef int[:] mview = arg
    cdef int[:] unassigned_mview
    o = object()
    with cython.test_body_needs_exception_handling(False):
        arg.x = 5
        something = arg.x
        arg.y = o
        arg.z = mview
    with cython.test_body_needs_exception_handling(True):
        unassigned_mview = arg.z  # needs initialized check
    with cython.test_body_needs_exception_handling(True):
        arg.unknown_attr = 1
    with cython.test_body_needs_exception_handling(True):
        b = arg.unknown_attr

def test_maybe_unassigned_int(arg):
    cdef int a, b
    if arg:
        maybe_unassigned = 5
    with cython.test_body_needs_exception_handling(False):
        b = maybe_unassigned

@cython.cpp_locals(True)
def test_cpp_locals(arg):
    # Currently, cpp classes are need exception handling because
    # they may have a non-trivial assignment operator. So by
    # definition cpp_locals also need exception handling.
    if arg:
        maybe_unassigned = CppClass()
    with cython.test_body_needs_exception_handling(True):
        maybe_unassigned.attr = 1
    with cython.test_body_needs_exception_handling(True):
        a = arg.maybe_unassigned

def test_indexing(s):
    cdef list this_is_a_list = []
    cdef const char *s_ptr = s
    cdef int[5] arr
    with cython.test_body_needs_exception_handling(True):
        this_is_a_list[0]
    with cython.test_body_needs_exception_handling(False):
        s_ptr[0]
        arr[0]
