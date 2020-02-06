# mode: run
# tag: METH_FASTCALL
# tag: warnings

from __future__ import print_function

cimport cython

# test mainly basic compilation - these are mostly copied from
# fastcall.pyx
@cython.binding(False)
@cython.fastcall_args("both")
def fastcall_function(**kw):
    """
    >>> fastcall_function(a=1, b=2)
    2
    """
    return len(kw)

@cython.binding(True)
@cython.fastcall_args("both")
def fastcall_cyfunction(**kw):
    """
    >>> fastcall_cyfunction(a=1, b=2)
    2
    """
    return len(kw)

@cython.binding(False)
@cython.fastcall_args("both")
def no_special_args_function(a, b):
    """
    >>> no_special_args_function(1, 2)
    """
    pass

@cython.binding(True)
@cython.fastcall_args("both")
def no_special_args_cyfunction(a, b):
    """
    >>> no_special_args_cyfunction(1, 2)
    """
    pass

cdef class Dummy:
    @cython.binding(False)
    @cython.fastcall_args("both")
    def fastcall_method1(self, x, *args, **kw):
        """
        >>> Dummy().fastcall_method1(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(False)
    @cython.fastcall_args("*")
    def fastcall_method2(self, x, *args, **kw):
        """
        >>> Dummy().fastcall_method2(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(False)
    @cython.fastcall_args("**")
    def fastcall_method3(self, x, *args, **kw):
        """
        >>> Dummy().fastcall_method3(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(False)
    @cython.fastcall_args("both")
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
    @cython.fastcall_args("both")
    def fastcall_method1(self, x, *args, **kw):
        """
        >>> CyDummy().fastcall_method1(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(True)
    @cython.fastcall_args("*")
    def fastcall_method2(self, x, *args, **kw):
        """
        >>> CyDummy().fastcall_method2(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(True)
    @cython.fastcall_args("**")
    def fastcall_method3(self, x, *args, **kw):
        """
        >>> CyDummy().fastcall_method3(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.binding(False)
    @cython.fastcall_args("*")
    def probably_not_fastcall_method(self, *args, **kw):
        """
        >>> CyDummy().probably_not_fastcall_method(1, 2, 3, a=1, b=2)
        5
        """
        return len(args) + len(kw)

class PyDummy:
    @cython.fastcall_args("both")
    def fastcall_method1(self, x, *args, **kw):
        """
        >>> PyDummy().fastcall_method1(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.fastcall_args("*")
    def fastcall_method2(self, x, *args, **kw):
        """
        >>> PyDummy().fastcall_method2(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    @cython.fastcall_args("**")
    def fastcall_method3(self, x, *args, **kw):
        """
        >>> PyDummy().fastcall_method3(1, 2, 3, a=1, b=2)
        4
        """
        return len(args) + len(kw)

    # FIXME should be generating warning
    @cython.fastcall_args("*")
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
@cython.fastcall_args("*")
def test_starargs_ops(*args):
    """
    >>> test_starargs_ops(1, 2, 3)
    1 2 3
    1 2 3
    1 2
    Caught IndexError
    1 2 3
    Caught ValueError
    Caught ValueError
    1
    2
    3
    True
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
    a, b, c = args
    print(a, b, c)
    try:
        a, b, c, d = args
    except ValueError:
        print("Caught ValueError")
    try:
        a, b = args
    except ValueError:
        print("Caught ValueError")

    for arg in args:
        print(arg)

    res = (1 in args)
    print(True if res else False)  # do it this way to avoid coercion to Python
    res = len(args)
    print("3" if res==3 else "not 3")  # do it this way to avoid coercion to Python
    print(call_with_args(*args))  # should go directly to a fastcall call and not prepare a tuple

@cython.test_fail_if_path_exists("//CoerceToPyTypeNode")
@cython.fastcall_args("both")
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

@cython.fastcall_args("*")
def test_starargs_ops_explicit_conversion(*args):
    """
    >>> test_starargs_ops_explicit_conversion(1, 2, 3)
    (1, 2, 3)
    """
    res1 = tuple(args)
    res2 = tuple(args)  # if the conversion were non-explicit then they would generate warnings
    print(res1)

@cython.fastcall_args("*")
def test_starargs_coercion_warning(*args):
    """
    >>> test_starargs_coercion_warning(1, 2, 3)
    (0, (1, 2, 3))
    """

    return args.index(1), args

cdef ord_(x):
    return ord(x)  # keeps the CoerceToPyTypeNode out of the main function

def call_with_kwds(**kwds):
    return len(kwds)

@cython.test_fail_if_path_exists("//CoerceToPyTypeNode")
@cython.fastcall_args("**")
def test_starstarargs_ops(**kwds):
    """
    >>> test_starstarargs_ops(a=1, b=2, c=3)
    3
    ['a', 'b', 'c']
    [1, 2, 3]
    [('a', 1), ('b', 2), ('c', 3)]
    True
    1
    294
    590
    294
    6
    3
    """
    cdef int res
    res = len(kwds)
    print("3" if res==3 else "not 3")  # avoid coercion to python object
    print(sorted(kwds.keys()))
    print(sorted(kwds.values()))
    print(sorted(kwds.items()))
    res = "a" in kwds
    print(True if res else False)  # avoid coercion to python object
    print(kwds["a"])
    print(sum([ ord_(k) for k in kwds ]))  # this way order doesn't matter
    print(sum([ ord_(k)*v for k, v in kwds.items() ]))
    print(sum([ ord_(k) for k in kwds.keys() ]))
    print(sum([ v for v in kwds.values() ]))
    print(call_with_kwds(**kwds))  # should be able to convert directly to a fastcall call

@cython.fastcall_args("**")
def test_starstarargs_ops_explicit_conversion(**kwds):
    """
    >>> test_starstarargs_ops_explicit_conversion(a=1, b=2, c=3)
    ['a', 'b', 'c']
    [1, 2, 3]
    """
    res1 = dict(kwds)
    res2 = dict(kwds)  # 2nd non-explicit conversion will generate warnings
    print(sorted(res1.keys()))
    print(sorted(res2.values()))

@cython.fastcall_args("**")
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

# TODO - failed test for copy into closure

_WARNINGS = """
73:4: Ignoring request for **kw to be a specialized fastcall argument since the function itself is not fastcallable and so this would only cause slower performance.
253:26: Fastcall tuple argument has been coerced to a Python object at least twice in this function. It may be more efficient to use a regular tuple argument.
319:4: Fastcall dict argument has been coerced to a Python object at least twice in this function. It may be more efficient to use a regular dict argument.
"""
