# mode: run

from __future__ import print_function

cimport cython
import pickle
import sys

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

@cython.binding(False)
def no_binding(a, select_nocapture):
    """
    >>> f1 = no_binding("no binding!", select_nocapture=True)
    >>> f1_reloaded = pickle.loads(pickle.dumps(f1))
    >>> f1_reloaded()
    'no_binding.inner'

    >>> f2 = no_binding("no binding!", select_nocapture=False)
    >>> f2_reloaded = pickle.loads(pickle.dumps(f2))
    >>> f2_reloaded()
    'no binding!'
    """
    if select_nocapture:
        def inner():
            return "no_binding.inner"
    else:
        # This is almost certainly forced into "binding=True"
        # but it's worth testing anyway
        def inner():
            return a
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

def defaults_supported():
    """
    Where the defaults are a genuine constant we can pickle them
    and read the introspected defaults
    >>> f, g = defaults_supported()
    >>> f_reloaded = pickle.loads(pickle.dumps(f))
    >>> g_reloaded = pickle.loads(pickle.dumps(g))
    >>> f_reloaded.__defaults__ == f.__defaults__
    True
    >>> f_reloaded.__defaults__
    (5, 'str')
    >>> f_reloaded.__kwdefaults__ is None
    True

    >>> g_reloaded.__defaults__ is None
    True
    >>> g.__kwdefaults__ == g_reloaded.__kwdefaults__
    True
    >>> sorted(list(g_reloaded.__kwdefaults__.items()))
    [('a', 10), ('b', 'other str')]
    """

    def f(a=5, b="str"):
        return a, b
    def g(*, a=10, b="other str"):
        return a, b
    return f, g

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

def test_lambda(float a, use_closure):
    """
    >>> f1 = test_lambda(1.5, use_closure=True)
    >>> f1(1)
    2.5
    >>> f1_reloaded = pickle.loads(pickle.dumps(f1))
    >>> f1_reloaded(1)
    2.5

    >>> f2 = test_lambda(1.5, use_closure=False)
    >>> f2(1)
    1
    >>> f2_reloaded = pickle.loads(pickle.dumps(f2))
    >>> f2_reloaded(1)
    1
    """

    if use_closure:
        return lambda x: a+x
    else:
        return lambda x: x

def example_generator():
    """
    >>> reloaded_example_gen = pickle.loads(pickle.dumps(example_generator))
    >>> list(reloaded_example_gen())
    [0, 1]

    TODO: running generators cannot yet be pickled (needs changes to __pyx_CoroutineObject)
    #>>> gen = example_generator()
    #>>> next(gen)
    #0
    #>>> reloaded_gen = pickle.loads(pickle.dumps(gen))
    #>>> next(reloaded_gen)
    #1
    #>>> next(gen)
    #1
    """
    yield 0
    yield 1

def lambda_for_genexpr(N):
    """
    This is being tested because: the .0 dummy name used in handling the
    generator expression scope gets put in the closure. It needs to be omitted from
    the pickle (since the name isn't a valid identifier so generates bad Cython code).
    We need to confirm that omitting it from the pickle doesn't cause problems on
    deallocation. N is deliberately not typed to ensure it's a ref-counted object
    >>> originals = [ f for f in lambda_for_genexpr(5) ]
    >>> reloadeds = [ pickle.loads(pickle.dumps(original)) for original in originals ]
    >>> for original, reloaded in zip(originals, reloadeds):
    ...    assert original() == reloaded()
    """
    return ( (lambda : x) for x in range(N) )


def global_fused(cython.floating x):
    """
    # check that we haven't managed to block this by mistake
    >>> reloaded = pickle.loads(pickle.dumps(global_fused))
    >>> reloaded(1.)
    1.0
    """
    return x

class ClassFused:
    """
    The unbound function works through the normal boring global name lookup
    >>> unbound_f_reloaded = pickle.loads(pickle.dumps(ClassFused.f))
    >>> unbound_f_reloaded(ClassFused(), 2.)
    2.0
    """
    def f(self, cython.floating x):
        return x

# TODO - fused classes in closures look to be broken for other reasons
#def returns_fused():
#    """
#    >>> pickle.dumps(returns_fused())
#    >>> pickle.dumps(returns_fused()['double'])
#    """
#    def inner(cython.floating x):
#        return x
#    return inner

__doc__ = """

Abuse direct access to the unpickling function just to test error handling
>>> __pyx_unpickle_cyfunction(b"Not a valid name!", None, None, None)  # doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
_pickle.UnpicklingError: ...
"""
