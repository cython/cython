cimport cython

from libc.stdint cimport uint64_t

class A:
    def pop(self, *args):
        print args
        return None

cdef class B:
    """
    >>> B().call_pop()
    'B'
    """
    cdef pop(self):
        return "B"
    def call_pop(self):
        return self.pop()


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode/AttributeNode')
def simple_pop(L):
    """
    >>> L = list(range(10))
    >>> simple_pop(L)
    9
    >>> simple_pop(L)
    8
    >>> L
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> while L:
    ...    _ = simple_pop(L)

    >>> L
    []
    >>> simple_pop(L)
    Traceback (most recent call last):
    IndexError: pop from empty list

    >>> simple_pop(A())
    ()
    """
    return L.pop()

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode/AttributeNode')
def simple_pop_typed(list L):
    """
    >>> L = list(range(10))
    >>> simple_pop_typed(L)
    9
    >>> simple_pop_typed(L)
    8
    >>> L
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> while L:
    ...    _ = simple_pop_typed(L)

    >>> L
    []
    >>> simple_pop_typed(L)
    Traceback (most recent call last):
    IndexError: pop from empty list
    """
    return L.pop()


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode/AttributeNode')
def index_pop(L, int i):
    """
    >>> L = list(range(10))
    >>> index_pop(L, 2)
    2
    >>> index_pop(L, -10)
    Traceback (most recent call last):
    IndexError: pop index out of range
    >>> index_pop(L, -2)
    8
    >>> L
    [0, 1, 3, 4, 5, 6, 7, 9]
    >>> index_pop(L, 100)
    Traceback (most recent call last):
    IndexError: pop index out of range
    >>> index_pop(L, -100)
    Traceback (most recent call last):
    IndexError: pop index out of range

    >>> while L:
    ...    _ = index_pop(L, 0)

    >>> L
    []

    >>> index_pop(L, 0)
    Traceback (most recent call last):
    IndexError: pop from empty list

    >>> index_pop(A(), 3)
    (3,)
    """
    return L.pop(i)

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode/AttributeNode')
def index_pop_typed(list L, int i):
    """
    >>> L = list(range(10))
    >>> index_pop_typed(L, 2)
    2
    >>> index_pop_typed(L, -2)
    8
    >>> L
    [0, 1, 3, 4, 5, 6, 7, 9]
    >>> index_pop_typed(L, 100)
    Traceback (most recent call last):
    IndexError: pop index out of range
    >>> index_pop_typed(L, -100)
    Traceback (most recent call last):
    IndexError: pop index out of range

    >>> index_pop_typed(None, 0)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'pop'

    >>> while L:
    ...    _ = index_pop_typed(L, 0)

    >>> L
    []

    >>> index_pop_typed(L, 0)
    Traceback (most recent call last):
    IndexError: pop from empty list
    """
    return L.pop(i)


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode/AttributeNode')
def index_pop_list_object_index(list L, i):
    """
    >>> L = list(range(10))
    >>> index_pop_list_object_index(L, 2)
    2
    >>> index_pop_list_object_index(L, -2)
    8
    >>> L
    [0, 1, 3, 4, 5, 6, 7, 9]
    >>> index_pop_list_object_index(L, 100)
    Traceback (most recent call last):
    IndexError: pop index out of range
    >>> index_pop_list_object_index(L, -100)
    Traceback (most recent call last):
    IndexError: pop index out of range

    >>> index_pop_list_object_index(None, 0)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'pop'
    >>> index_pop_list_object_index([1], None)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> index_pop_list_object_index([1], 'abc')   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...

    >>> while L:
    ...    _ = index_pop_list_object_index(L, 0)

    >>> L
    []

    >>> index_pop_list_object_index(L, 0)
    Traceback (most recent call last):
    IndexError: pop from empty list
    """
    return L.pop(i)


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode/AttributeNode')
def index_pop_literal(list L):
    """
    >>> L = list(range(10))
    >>> index_pop_literal(L)
    0
    >>> L
    [1, 2, 3, 4, 5, 6, 7, 8, 9]

    >>> while L:
    ...    _ = index_pop_literal(L)

    >>> L
    []

    >>> index_pop_literal(L)
    Traceback (most recent call last):
    IndexError: pop from empty list
    """
    return L.pop(0)


@cython.test_fail_if_path_exists('//PythonCapiCallNode')
def crazy_pop(L):
    """
    >>> crazy_pop(list(range(10)))    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...pop... argument...
    >>> crazy_pop(A())
    (1, 2, 3)
    """
    return L.pop(1, 2, 3)


def method_name():
    """
    >>> method_name()
    'pop'
    """
    return [].pop.__name__


def object_pop_large_int():
    """
    >>> object_pop_large_int()
    {}
    """
    cdef object foo = {}
    cdef uint64_t bar = 201213467776703617ULL

    foo[bar] = None
    assert (<object>bar) in foo
    foo.pop(bar)
    return foo
