# mode: run
# tag: traceback

# A cdef function that returns its exception value without raising is a user
# error, but it used to crash in __Pyx_AddTraceback() on Python 3.12+.

import traceback


cdef int returns_error_value(int x) except -1:
    return x

cdef int calls_returns_error_value(int x) except -1:
    returns_error_value(x)
    return 0


def call_with_error_value():
    """
    >>> call_with_error_value()
    Traceback (most recent call last):
    SystemError: error return without exception set
    """
    returns_error_value(-1)


def call_with_normal_value():
    """
    >>> call_with_normal_value()
    5
    """
    return returns_error_value(5)


def nested_traceback():
    """
    >>> nested_traceback()
    """
    try:
        calls_returns_error_value(-1)
    except SystemError:
        tb_string = traceback.format_exc()
    else:
        assert False, "no exception raised"
    for s in ('calls_returns_error_value', 'nested_traceback',
              'error return without exception set'):
        assert s in tb_string, (s, tb_string)
