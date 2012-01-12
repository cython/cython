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
def test_starred(a):
    """
    >>> test_starred(123)
    (123, (), {})
    """
    def inner(a, *args, **kwargs):
        return a, args, kwargs
    return inner(a)
