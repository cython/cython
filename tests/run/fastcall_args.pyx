# mode: run
# tag: METH_FASTCALL
#### tag: warnings # FIXME

from __future__ import print_function

cimport cython

# test mainly basic compilation - these are mostly copied from
# fastcall.pyx
@cython.binding(False)
@cython.fastcall_args(True)
def fastcall_function(**kw):
    """
    >>> fastcall_function(a=1, b=2)
    2
    """
    return len(kw)

@cython.binding(True)
@cython.fastcall_args(True)
def fastcall_cyfunction(**kw):
    """
    >>> fastcall_cyfunction(a=1, b=2)
    2
    """
    return len(kw)

@cython.binding(False)
@cython.fastcall_args(True)
def no_special_args_function(a, b):
    """
    >>> no_special_args_function(1, 2)
    """
    pass

@cython.binding(True)
@cython.fastcall_args(True)
def no_special_args_cyfunction(a, b):
    """
    >>> no_special_args_cyfunction(1, 2)
    """
    pass

cdef class Dummy:
    @cython.binding(False)
    @cython.fastcall_args(True)
    def fastcall_method1(self, x, *args, **kw):
        """
        >>> Dummy().fastcall_method1(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(False)
    @cython.fastcall_args(True, False)
    def fastcall_method2(self, x, *args, **kw):
        """
        >>> Dummy().fastcall_method2(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(False)
    @cython.fastcall_args(False, True)
    def fastcall_method3(self, x, *args, **kw):
        """
        >>> Dummy().fastcall_method3(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(False)
    @cython.fastcall_args(True)
    def probably_not_fastcall_method(self, *args, **kw):
        """
        Should generate a warning about ignored kw. If this method
        becomes fastcall-able in future and the warning goes away
        then this is not an issue - just remove the test.

        >>> Dummy().probably_not_fastcall_method(1, 2, 3, a=1, b=2)
        5
        """
        return len(args) + len(kw)

cdef class CyDummy:
    @cython.binding(True)
    @cython.fastcall_args(True)
    def fastcall_method1(self, x, *args, **kw):
        """
        >>> CyDummy().fastcall_method1(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(True)
    @cython.fastcall_args(True, False)
    def fastcall_method2(self, x, *args, **kw):
        """
        >>> CyDummy().fastcall_method2(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(True)
    @cython.fastcall_args(False, True)
    def fastcall_method3(self, x, *args, **kw):
        """
        >>> CyDummy().fastcall_method3(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(False)
    @cython.fastcall_args(True, False)
    def probably_not_fastcall_method(self, *args, **kw):
        """
        >>> CyDummy().probably_not_fastcall_method(1, 2, 3, a=1, b=2)
        5
        """
        return len(args) + len(kw)

class PyDummy:
    @cython.fastcall_args(True)
    def fastcall_method1(self, x, *args, **kw):
        """
        >>> PyDummy().fastcall_method1(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.fastcall_args(True, False)
    def fastcall_method2(self, x, *args, **kw):
        """
        >>> PyDummy().fastcall_method2(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.fastcall_args(False, True)
    def fastcall_method3(self, x, *args, **kw):
        """
        >>> PyDummy().fastcall_method3(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    # FIXME should be generating warning
    @cython.fastcall_args(True, False)
    def probably_not_fastcall_method(self, *args, **kw):
        """
        >>> PyDummy().probably_not_fastcall_method(1, 2, 3, a=1, b=2)
        5
        """
        return len(args) + len(kw)

def call_with_args(*args):
    return len(args)

# all of these operations should be supported without coercion
@cython.test_fail_if_path_exists("//CoerceToPyTypeNode")
@cython.fastcall_args(True, False)
def test_starargs_ops(*args):
    """
    >>> test_starargs_ops(1, 2, 3)
    1 2 3
    1 2 3
    1 2
    Caught IndexError
    1
    2
    3
    3
    3
    """
    cdef int res = 1
    a = args[0]
    b = args[1]
    c = args[2]
    print(a, b, c)
    a = args[-3]
    b = args[-2]
    c = args[-1]
    print(a, b, c)
    subslice = args[:2]
    print(subslice[0], subslice[1])
    try:
        args[4]
    except IndexError:
        print("Caught IndexError")

    for arg in args:
        print(arg)

    res = len(args)
    print("3" if res==3 else "not 3")  # do it this way to avoid coercion to Python
    print(call_with_args(*args))  # should go directly to a fastcall call and not prepare a tuple

@cython.test_fail_if_path_exists("//CoerceToPyTypeNode")
@cython.fastcall_args(True)
def conversion_to_bool_good(dummy, *args, **kwds):
    """
    Specifically test for this to check both true and false cases
    because it's easy to generate C code that compiles but doesn't test
    the right thing
    >>> conversion_to_bool_good(1, 2, a=2)
    args
    kwds
    >>> conversion_to_bool_good(1, 2)
    args
    >>> conversion_to_bool_good(1, a=2)
    kwds
    >>> conversion_to_bool_good(1)
    """
    if args:
        print("args")
    if kwds:
        print("kwds")

@cython.fastcall_args(True, False)
def test_starargs_ops_explicit_conversion(*args):
    """
    >>> test_starargs_ops_explicit_conversion(1, 2, 3)
    (1, 2, 3)
    """
    res1 = tuple(args)
    res2 = tuple(args)  # if the conversion were non-explicit then they would generate warnings
    print(res1)

def test_starargs_coercion(*args):
    """
    The double coercion should force it to be a regular tuple
    >>> test_starargs_coercion(1, 2, 3)
    (0, (1, 2, 3), 'tuple object')
    """

    return args.index(1), args, cython.typeof(args)

cdef ord_(x):
    return ord(x)  # keeps the CoerceToPyTypeNode out of the main function

def call_with_kwds(**kwds):
    return len(kwds)

@cython.test_fail_if_path_exists("//CoerceToPyTypeNode")
@cython.fastcall_args(False, True)
def test_starstarargs_ops(**kwds):
    """
    >>> test_starstarargs_ops(a=1, b=2, c=3)
    3
    ['a', 'b', 'c']
    [1, 2, 3]
    294
    6
    3
    """
    cdef int res
    res = len(kwds)
    print("3" if res==3 else "not 3")  # avoid coercion to python object
    print(sorted(kwds.keys()))
    print(sorted(kwds.values()))
    print(sum([ ord_(k) for k in kwds.keys() ]))
    print(sum([ v for v in kwds.values() ]))
    print(call_with_kwds(**kwds))  # should be able to convert directly to a fastcall call

@cython.fastcall_args(False, True)
def test_starstarargs_ops_changes(**kwds):
    """
    Changes to kwds need to be preserved after coercion
    >>> test_starstarargs_ops_changes(a=1, b=2, c=3)
    1
    Failed to find 'a'
    10
    """
    print(kwds.pop("a"))
    try:
        kwds["a"]
    except KeyError:
        print("Failed to find 'a'")
    kwds["d"] = 10
    print(kwds.pop("d"))

def call_with_both(*args, **kwds):
    return len(args), len(kwds)

cdef extern from *:
    """
    #if CYTHON_METH_FASTCALL
    #define FASTCALLTUPLE_PROBE(x, offset) (intptr_t)(x.args + offset)
    #else
    #define FASTCALLTUPLE_PROBE(x, offset) 0 // test is pretty meaningless
    #endif
    """
    long FASTCALLTUPLE_PROBE(...)
    int PyCFunction_GET_FLAGS(op)

def has_fastcall(meth):
    """
    Given a builtin_function_or_method or cyfunction ``meth``,
    return whether it uses ``METH_FASTCALL``.
    """
    # Hardcode METH_FASTCALL constant equal to 0x80 for simplicity
    return bool(PyCFunction_GET_FLAGS(meth) & 0x80)


def assert_fastcall(meth):
    """
    Assert that ``meth`` uses ``METH_FASTCALL`` if the Python
    implementation supports it.
    """
    # getattr uses METH_FASTCALL on CPython >= 3.7
    if has_fastcall(getattr) and not has_fastcall(meth):
        raise AssertionError(f"{meth} does not use METH_FASTCALL")

def call_with_args_and_probe(dummy, *args):
    """
    Dummy argument is necessary for Cython to make it fastcall
    The assert_fastcall is only to check that the arguments can genuinely be forwarded directly
    (otherwise the test this is used in is pointless)
    >>> assert_fastcall(call_with_args_and_probe)
    """
    return FASTCALLTUPLE_PROBE(args, 0)

from cpython.long cimport PyLong_FromLong

@cython.test_fail_if_path_exists("//CoerceToPyTypeNode")
def test_forwarding(a, *args, **kwds):
    """
    >>> test_forwarding(1, 'a', 'b', 'c', 'd', x=1, y=2)
    FastcallTuple FastcallDict
    4
    2
    4 2
    True
    """
    print(cython.typeof(args), cython.typeof(kwds))
    print(call_with_args(*args))
    print(call_with_kwds(**kwds))
    print(*call_with_both(*args, **kwds))
    # PyLong_FromLong is to avoid coercion node being created
    print(PyLong_FromLong(FASTCALLTUPLE_PROBE(args, 1)) # +1 account for dummy argument
           == call_with_args_and_probe(*args))

def test_forwarding2(a, *args, **kwds):
    """
    Tests that all three combinations of kwds work:
    - the kwnames version
    - the dict version created after coercion/modification
    - the empty version
    >>> test_forwarding2(1, 'a', 'b', 'c', 'd', x=1, y=2)
    FastcallTuple FastcallDict
    2 2
    1 1
    >>> test_forwarding2(1, 'a', 'b', 'c', 'd')
    FastcallTuple FastcallDict
    0 0
    """
    print(cython.typeof(args), cython.typeof(kwds))
    print(call_with_kwds(**kwds), call_with_both(*args, **kwds)[1])
    if (len(kwds)):
        kwds.popitem()  # modifies so converts to a dictionary version
        print(call_with_kwds(**kwds), call_with_both(*args, **kwds)[1])

def test_coercion_gives_tuple(a, *args):
    """
    >>> test_coercion_gives_tuple(1, 2, 3)
    tuple object
    """
    class C:
        pass
    args.index(2)
    print(cython.typeof(args))
    c = C()
    c.store_args = args  # 2 coercions to should be enough to force it to use regular args

def test_noncoercion_gives_fastcall(a, *args):
    """
    >>> test_noncoercion_gives_fastcall(1, 2, 3)
    FastcallTuple
    """
    print(cython.typeof(args))

def test_nonfastcall_doesnt_use_keywords(*args, **kwds):
    """
    If the first test fails that isn't a problem - we just need to find another function
    that Cython doesn't give the fastcall calling convention
    >>> has_fastcall(test_nonfastcall_doesnt_use_keywords)
    False
    >>> test_nonfastcall_doesnt_use_keywords(a=1, b=2)
    'dict object'
    """
    return cython.typeof(kwds)

_WARNINGS = """
73:4: Request for **kw to be a specialized fastcall argument is pointless since the function itself is not fastcallable and so this will only cause degrade performance.
"""

