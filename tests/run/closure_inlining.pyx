# cython: optimize.inline_defnode_calls=True
# mode: run
cimport cython

@cython.test_fail_if_path_exists('//SimpleCallNode')
@cython.test_assert_path_exists('//InlinedDefNodeCallNode')
def simple_noargs():
    """
    >>> simple_noargs()
    123
    """
    def inner():
        return 123
    return inner()


@cython.test_fail_if_path_exists('//SimpleCallNode')
@cython.test_assert_path_exists('//InlinedDefNodeCallNode')
def test_coerce(a, int b):
    """
    >>> test_coerce(2, 2)
    4
    """
    def inner(int a, b):
        return a * b
    return inner(a, b)


cdef class Foo(object):
    def __repr__(self):
        return '<Foo>'


@cython.test_fail_if_path_exists('//SimpleCallNode')
@cython.test_assert_path_exists('//InlinedDefNodeCallNode')
def test_func_signature(a):
    """
    >>> test_func_signature(Foo())
    <Foo>
    >>> test_func_signature(123)
    Traceback (most recent call last):
    TypeError: Cannot convert int to closure_inlining.Foo
    """

    def inner(Foo a):
        return a
    return inner(a)

@cython.test_fail_if_path_exists('//SimpleCallNode')
@cython.test_assert_path_exists('//InlinedDefNodeCallNode')
def test_func_signature2(a, b):
    """
    >>> test_func_signature2(Foo(), 123)
    (<Foo>, 123)
    >>> test_func_signature2(321, 123)
    Traceback (most recent call last):
    TypeError: Cannot convert int to closure_inlining.Foo
    """

    def inner(Foo a, b):
        return a, b
    return inner(a, b)

# Starred args and default values are not yet supported for inlining
@cython.test_assert_path_exists('//SimpleCallNode')
def test_defaults(a, b):
    """
    >>> test_defaults(1, 2)
    (1, 2, 123)
    """
    def inner(a, b=b, c=123):
        return a, b, c
    return inner(a)

@cython.test_assert_path_exists('//SimpleCallNode')
def test_kwonly_args(a, b):
    """
    >>> test_kwonly_args(1, 2)
    (1, 2, 123)
    """
    def inner(a, b=b, *, c=123):
        return a, b, c
    return inner(a)

@cython.test_assert_path_exists('//SimpleCallNode')
def test_kwonly_args_missing(a, b):
    """
    >>> test_kwonly_args_missing(1, 2)
    Traceback (most recent call last):
    TypeError: inner() needs keyword-only argument c
    """
    def inner(a, b=b, *, c):
        return a, b, c
    return inner(a)

@cython.test_assert_path_exists('//SimpleCallNode')
def test_starred(a):
    """
    >>> test_starred(123)
    (123, (), {})
    """
    def inner(a, *args, **kwargs):
        return a, args, kwargs
    return inner(a)


def test_global_calls_still_work():
    """
    >>> global_call_result
    123
    """
    return 123

global_call_result = test_global_calls_still_work()


@cython.test_fail_if_path_exists(
    '//InlinedDefNodeCallNode//SimpleCallNode')
@cython.test_assert_path_exists(
    '//InlinedDefNodeCallNode',
    '//InlinedDefNodeCallNode[@function_name.name = "call"]',
    '//InlinedDefNodeCallNode//InlinedDefNodeCallNode')
def test_sideeffect_call_order():
    """
    >>> test_sideeffect_call_order()
    [2, 4, 5]
    """
    L = []
    def sideeffect(x):
        L.append(x)
        return x
    def call(x1, x2, x3, x4, x5):
        pass
    call(1, sideeffect(2), 3, sideeffect(4), sideeffect(5))
    return L


def test_redef(redefine):
    """
    >>> test_redef(False)
    1
    >>> test_redef(True)
    2
    """
    def inner():
        return 1
    def inner2():
        return 2
    def redef():
        nonlocal inner
        inner = inner2
    if redefine:
        redef()
        assert inner == inner2
    else:
        assert inner != inner2
    return inner()


def test_with_statement():
    """
    >>> test_with_statement()
    enter
    running
    exit
    """
    def make_context_manager():
        class CM(object):
            def __enter__(self):
                print "enter"
            def __exit__(self, *args):
                print "exit"
        return CM()

    with make_context_manager():
        print "running"
