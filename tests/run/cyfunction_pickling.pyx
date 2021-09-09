# mode: run

import pickle

def outer1(a, select):
    """
    >>> f = outer1(10, True)
    >>> f(5)
    15
    >>> pickled = pickle.dumps(f)
    >>> reloaded_f = pickle.loads(pickled)
    >>> reloaded_f(5)
    15
    >>> g = outer1(10, False)
    >>> g(5)
    5
    >>> pickled = pickle.dumps(g)
    >>> reloaded_g = pickle.loads(pickled)
    >>> reloaded_g(5)
    5
    """
    if select:  # check that the same name doesn't confuse it
        def inner1(b):
            return a+b
    else:
        def inner1(b):
            return a-b
    return inner1

def no_capture():
    """
    >>> f = no_capture()
    >>> f()
    True
    >>> pickled = pickle.dumps(f)
    >>> reloaded_f = pickle.loads(pickled)
    >>> reloaded_f()
    True
    """
    def inner():
        return True
    return inner

def defaults_currently_unsupported(a):
    """
    # TODO remove this test once this has been made to work properly
    >>> f = defaults_currently_unsupported(10)
    >>> f()
    10
    >>> pickle.dumps(f)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AttributeError: ... Cannot currently pickle CyFunctions with non-constant default arguments
    """
    def inner(b=a):
        return b
    return inner
