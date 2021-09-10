# mode: run

from __future__ import print_function

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

# TODO add tests for the supported bits of this
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

def class_in_func(a):
    """
    This test case is a little odd - the class itself isn't pickleable so it's
    of very little practical use, but worth testing the assumptions made
    >>> C = class_in_func("hello")
    >>> cinst = C()
    >>> C_f_reloaded = pickle.loads(pickle.dumps(C.f))
    >>> C_f_reloaded([])  # can be called with a different "self"
    []

    >>> pickle.dumps(cinst.f)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AttributeError: Can't pickle local object ...

    >>> C_f_closure_reloaded = pickle.loads(pickle.dumps(C.f_with_closure))
    >>> C_f_closure_reloaded([])
    [] hello

    >>> pickle.dumps(cinst.f_with_closure)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AttributeError: Can't pickle local object ...

    >>> C_sm_reloaded = pickle.loads(pickle.dumps(C.sm))
    >>> C_sm_reloaded()
    C.sm

    >>> C_sm_closure_reloaded = pickle.loads(pickle.dumps(C.sm_with_closure))
    >>> C_sm_closure_reloaded()
    C.sm_with_closure hello

    >>> pickle.dumps(C.uses_super)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AttributeError: ... Cannot currently pickle CyFunctions with class cells ...
    """
    class C(object):
        # C().f is not pickleable because a C instance isn't
        # C.f is pickleable but not hugely useful without the class
        def f(self):
            print(self)

        # f_with_closure is largely the same as f
        def f_with_closure(self):
            print(self, a)

        # sm is pickleable and maybe practically usable
        @staticmethod
        def sm():
            print("C.sm")
        @staticmethod
        def sm_with_closure():
            print("C.sm_with_closure", a)

        # uses_super is not pickleable because it requires a classobj
        # This is currently deliberately forbidden. Even if it were
        # supported it's likely to fail (because it requires C to be pickleable)
        def uses_super(self):
            return super().some_func()
    return C

__doc__ = """
Abuse direct access to the unpickling function just to test error handling
>>> __pyx_unpickle_cyfunction(u"Not a valid name!", None, None, None)  # doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
_pickle.UnpicklingError: ...
"""
