# mode: run
# tag: nogil, withgil

"""
Test the 'with gil:' statement.
"""

cimport cython
from cpython.ref cimport PyObject

import sys


def redirect_stderr(func, *args, **kwargs):
    """
    Helper function that redirects stderr to stdout for doctest.
    """
    stderr, sys.stderr = sys.stderr, sys.stdout
    func(*args, **kwargs)
    sys.stderr = stderr

cdef void puts(char *string) with gil:
    """
    We need this for doctest, used from nogil sections.
    """
    print string.decode('ascii')

class ExceptionWithMsg(Exception):
    """
    In python2.4 Exception is formatted as <exceptions.Exception
    instance at 0x1b8f948> when swallowed.
    """

    def __repr__(self):
        return "ExceptionWithMsg(%r)" % self.args


# Start with some normal Python functions

def test_simple():
    """
    >>> test_simple()
    ['spam', 'ham']
    """
    with nogil:
        with gil:
            print ['spam', 'ham']

def test_nested_gil_blocks():
    """
    >>> test_nested_gil_blocks()
    entered outer nogil section
    entered outer gil section
    entered inner nogil section
    entered inner gil section
    leaving inner gil section
    leaving inner nogil section
    leaving outer gil section
    leaving outer nogil section
    """

    with nogil:
        puts("entered outer nogil section")

        with gil:
            print 'entered outer gil section'

            with nogil:
                puts("entered inner nogil section")
                with gil:
                    print 'entered inner gil section'
                    print 'leaving inner gil section'
                puts("leaving inner nogil section")

            print "leaving outer gil section"
        puts("leaving outer nogil section")

def test_propagate_exception():
    """
    >>> test_propagate_exception()
    Traceback (most recent call last):
        ...
    Exception: This exception propagates!
    """
    # Note, doctest doesn't support both output and exceptions
    with nogil:
        with gil:
            raise Exception("This exception propagates!")

def test_catch_exception():
    """
    >>> test_catch_exception()
    This is executed
    Exception value
    This is also executed
    """
    try:
        with nogil:
            with gil:
                print "This is executed"
                raise Exception("Exception value")
                print "This is not executed"
            puts("This is also not executed")
    except Exception, e:
        print e
    print "This is also executed"

def test_try_finally_and_outer_except():
    """
    >>> test_try_finally_and_outer_except()
    First finally clause
    Second finally clause
    Caught: Some Exception
    End of function
    """
    try:

        with nogil:
            with gil:
                try:
                    with nogil:
                        with gil:
                            try:
                                raise Exception("Some Exception")
                            finally:
                                puts("First finally clause")
                finally:
                    puts("Second finally clause")
            puts("This is not executed")

    except Exception, e:
        print "Caught:", e

    print "End of function"

def test_restore_exception():
    """
    >>> test_restore_exception()
    Traceback (most recent call last):
        ...
    Exception: Override the raised exception
    """
    with nogil:
        with gil:
            try:
                with nogil:
                    with gil:
                        raise Exception("Override this please")
            finally:
                raise Exception("Override the raised exception")

### DISABLED: this cannot work with flow control analysis
##
## def test_declared_variables():
##     """
##     >>> test_declared_variables()
##     None
##     None
##     ['s', 'p', 'a', 'm']
##     ['s', 'p', 'a', 'm']
##     """
##     cdef object somevar
##
##     print somevar
##
##     with nogil:
##         with gil:
##             print somevar
##             somevar = list("spam")
##             print somevar
##
##     print somevar

### DISABLED: this cannot work with flow control analysis
##
## def test_undeclared_variables():
##     """
##     >>> test_undeclared_variables()
##     None
##     None
##     ['s', 'p', 'a', 'm']
##     ['s', 'p', 'a', 'm']
##     """
##     print somevar
##     with nogil:
##         with gil:
##             print somevar
##             somevar = list("spam")
##             print somevar
##
##     print somevar

def test_loops_and_boxing():
    """
    >>> test_loops_and_boxing()
    spamham
    h
    a
    m
    done looping
    """
    cdef char c, *string = "spamham"

    with nogil:
        with gil:
            print string.decode('ascii')
            for c in string[4:]:
                print "%c" % c
            else:
                print "done looping"

cdef class SomeExtClass(object):
    cdef int some_attribute

@cython.infer_types(True)
def test_infer_types():
    """
    >>> test_infer_types()
    10
    """
    with nogil:
        with gil:
            obj = SomeExtClass()
            obj.some_attribute = 10

    print obj.some_attribute

def test_closure():
    """
    >>> test_closure()
    Traceback (most recent call last):
        ...
    Exception: {'twinkle': 'little star'}
    """
    a = dict(twinkle='little star')

    def inner_function():
        with nogil:
            with gil:
                raise Exception(a)

    with nogil:
        with gil:
            inner_function()

    raise Exception("This should not be raised!")

cpdef test_cpdef():
    """
    >>> test_cpdef()
    Seems to work!
    Or does it?
    """
    with nogil:
        with gil:
            print "Seems to work!"
        puts("Or does it?")


# Now test some cdef functions with different return types

cdef void void_nogil_ignore_exception() noexcept nogil:
    with gil:
        raise ExceptionWithMsg("This is swallowed")

    puts("unreachable")
    with gil:
        print "unreachable"

cdef void void_nogil_nested_gil() noexcept nogil:
    with gil:
        with nogil:
            with gil:
                print 'Inner gil section'
            puts("nogil section")
        raise ExceptionWithMsg("Swallow this")
    puts("Don't print this")

def test_nogil_void_funcs_with_gil():
    """
    >>> redirect_stderr(test_nogil_void_funcs_with_gil)  # doctest: +ELLIPSIS
    with_gil.ExceptionWithMsg: This is swallowed
    Exception... ignored...
    Inner gil section
    nogil section
    ...
    Exception... ignored...
    """
    void_nogil_ignore_exception()
    void_nogil_nested_gil()

def test_nogil_void_funcs_with_nogil():
    """
    >>> redirect_stderr(test_nogil_void_funcs_with_nogil)  # doctest: +ELLIPSIS
    with_gil.ExceptionWithMsg: This is swallowed
    Exception... ignored...
    Inner gil section
    nogil section
    with_gil.ExceptionWithMsg: Swallow this
    Exception... ignored...
    """
    with nogil:
        void_nogil_ignore_exception()
        void_nogil_nested_gil()


cdef PyObject *nogil_propagate_exception() except NULL nogil:
    with nogil:
        with gil:
            raise Exception("This exception propagates!")
    return <PyObject *> 1

def test_nogil_propagate_exception():
    """
    >>> test_nogil_propagate_exception()
    Traceback (most recent call last):
        ...
    Exception: This exception propagates!
    """
    nogil_propagate_exception()


cdef with_gil_raise() with gil:
    raise Exception("This exception propagates!")

def test_release_gil_call_gil_func():
    """
    >>> test_release_gil_call_gil_func()
    Traceback (most recent call last):
        ...
    Exception: This exception propagates!
    """
    with nogil:
        with gil:
            with_gil_raise()


# Test try/finally in nogil blocks

def test_try_finally_in_nogil():
    """
    >>> test_try_finally_in_nogil()
    Traceback (most recent call last):
        ...
    Exception: Override exception!
    """
    with nogil:
        try:
            with gil:
                raise Exception("This will be overridden")
        finally:
            with gil:
                raise Exception("Override exception!")

            with gil:
                raise Exception("This code should not be executed!")

def test_nogil_try_finally_no_exception():
    """
    >>> test_nogil_try_finally_no_exception()
    first nogil try
    nogil try gil
    second nogil try
    nogil finally
    ------
    First with gil block
    Second with gil block
    finally block
    """
    with nogil:
        try:
            puts("first nogil try")
            with gil:
                print "nogil try gil"
            puts("second nogil try")
        finally:
            puts("nogil finally")

    print '------'

    with nogil:
        try:
            with gil:
                print "First with gil block"

            with gil:
                print "Second with gil block"
        finally:
            puts("finally block")

def test_nogil_try_finally_propagate_exception():
    """
    >>> test_nogil_try_finally_propagate_exception()
    Execute finally clause
    Propagate this!
    """
    try:
        with nogil:
            try:
                with gil:
                    raise Exception("Propagate this!")
                with gil:
                    raise Exception("Don't reach this section!")
            finally:
                puts("Execute finally clause")
    except Exception, e:
        print e

def test_nogil_try_finally_return_in_with_gil(x):
    """
    >>> test_nogil_try_finally_return_in_with_gil(10)
    print me
    10
    """
    with nogil:
        try:
            with gil:
                raise Exception("Swallow me!")
        finally:
            with gil:
                print "print me"
                return x

    print "I am not executed"

cdef void nogil_try_finally_return() nogil:
    try:
        with gil:
            raise Exception("I am swallowed in nogil code... right?")
    finally:
        with gil:
            print "print me first"

        return

    with gil:
        print "I am not executed"

def test_nogil_try_finally_return():
    """
    >>> test_nogil_try_finally_return()
    print me first
    """
    with nogil:
        nogil_try_finally_return()

cdef int error_func() except -1 with gil:
    raise Exception("propagate this")

def test_nogil_try_finally_error_label():
    """
    >>> test_nogil_try_finally_error_label()
    print me first
    propagate this
    """
    try:
        with nogil:
            try:
                error_func()
            finally:
                with gil: print "print me first"
    except Exception, e:
        print e.args[0]


def void_with_python_objects():
    """
    >>> void_with_python_objects()
    """
    with nogil:
        _void_with_python_objects()


cdef void _void_with_python_objects() nogil:
    c = 123
    with gil:
        obj1 = [123]
        obj2 = [456]


def void_with_py_arg_reassigned(x):
    """
    >>> void_with_py_arg_reassigned(123)
    """
    with nogil:
        _void_with_py_arg_reassigned(x)


cdef void _void_with_py_arg_reassigned(x) nogil:
    c = 123
    with gil:
        x = [456]


cdef void test_timing_callback() with gil:
  pass

def test_timing(long N):
  """
  >>> sorted([test_timing(10000) for _ in range(10)])  # doctest: +ELLIPSIS
  [...]
  """
  import time
  t = time.time()
  with nogil:
    for _ in range(N):
      test_timing_callback()
  return time.time() - t
