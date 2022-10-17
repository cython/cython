# mode: run
# tag: pure3, pure2

import cython

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
@cython.locals(x=bytearray)
def basic_bytearray_iter(x):
    """
    >>> basic_bytearray_iter(bytearray(b"hello"))
    h
    e
    l
    l
    o
    """
    for a in x:
        print(chr(a))

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
@cython.locals(x=bytearray)
def reversed_bytearray_iter(x):
    """
    >>> reversed_bytearray_iter(bytearray(b"hello"))
    o
    l
    l
    e
    h
    """
    for a in reversed(x):
        print(chr(a))

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
@cython.locals(x=bytearray)
def modifying_bytearray_iter1(x):
    """
    >>> modifying_bytearray_iter1(bytearray(b"abcdef"))
    a
    b
    c
    3
    """
    count = 0
    for a in x:
        print(chr(a))
        del x[-1]
        count += 1
    print(count)

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
@cython.locals(x=bytearray)
def modifying_bytearray_iter2(x):
    """
    >>> modifying_bytearray_iter2(bytearray(b"abcdef"))
    a
    c
    e
    3
    """
    count = 0
    for a in x:
        print(chr(a))
        del x[0]
        count += 1
    print(count)

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
@cython.locals(x=bytearray)
def modifying_reversed_bytearray_iter(x):
    """
    NOTE - I'm not 100% sure how well-defined this behaviour is in Python.
    However, for the moment Python and Cython seem to do the same thing.
    Testing that it doesn't crash is probably more important than the exact output!
    >>> modifying_reversed_bytearray_iter(bytearray(b"abcdef"))
    f
    f
    f
    f
    f
    f
    """
    for a in reversed(x):
        print(chr(a))
        del x[0]

# ticket: 3473

def test_bytearray_iteration(src):
    """
    >>> src = b'123'
    >>> test_bytearray_iteration(src)
    49
    50
    51
    """

    data = bytearray(src)
    for elem in data:
        print(elem)
