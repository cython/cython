# mode: run
# tag: closures, optional_args

# An optional (defaulted) argument of a cdef function that is captured by an
# inner function (closure) must be moved into the closure scope, just like a
# non-optional argument. Previously it was unpacked only into a C local while
# the body and the closure read the (uninitialised) scope field, which returned
# the wrong value or crashed (NULL dereference on the freelist allocation path).


cdef test(object register=None, object length=None):
    # `length` is captured by `_on_done`, so it lives in the closure scope.
    def _on_done():
        return length
    return length, _on_done()


cdef test_multi(object device_index, object register=2, object tdi_data=3):
    def inner():
        return (device_index, register, tdi_data)
    return inner()


def run_passed():
    """
    >>> run_passed()
    (196883, 196883)
    """
    return test(0, 196883)


def run_default():
    """
    >>> run_default()
    (None, None)
    """
    return test(0)


def run_multi_all():
    """
    >>> run_multi_all()
    (1, 20, 30)
    """
    return test_multi(1, 20, 30)


def run_multi_partial():
    """
    >>> run_multi_partial()
    (1, 20, 3)
    """
    return test_multi(1, 20)


def run_multi_defaults():
    """
    >>> run_multi_defaults()
    (1, 2, 3)
    """
    return test_multi(1)
