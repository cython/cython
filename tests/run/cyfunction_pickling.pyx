# mode: run

import pickle
cimport cython

@cython.binding(True)
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

@cython.binding(False)
def outer2(a, select):
    """
    >>> f = outer2(10, True)
    >>> f(5)
    15
    >>> pickled = pickle.dumps(f)
    >>> reloaded_f = pickle.loads(pickled)
    >>> reloaded_f(5)
    15
    >>> g = outer2(10, False)
    >>> g(5)
    5
    >>> pickled = pickle.dumps(g)
    >>> reloaded_g = pickle.loads(pickled)
    >>> reloaded_g(5)
    5
    """
    if select:  # check that the same name doesn't confuse it
        def inner2(b):
            return a+b
    else:
        def inner2(b):
            return a-b
    return inner2
