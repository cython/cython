#mode: run
#tag: pure3.0
#tag: warnings
#tag: property

# in a separate file largely to keep the warnings part manageable
# is a pure Python test to confirm that the behaviour is identical

import cython

@cython.cclass
@cython.test_assert_path_exists("//PropertyNode")
class C:
    """
    >>> inst = C()
    >>> inst.a
    0
    >>> inst.b = 5
    >>> inst.c
    5
    >>> del inst.c
    >>> inst.a
    -100
    >>> inst.c = 10
    >>> inst.b
    10
    >>> inst = C()
    >>> try:
    ...     del inst.a
    ... except (AttributeError, NotImplementedError): # exact error varies between Python and Cython
    ...     print("Failed")
    Failed
    >>> try:
    ...     del inst.b
    ... except (AttributeError, NotImplementedError): # exact error varies between Python and Cython
    ...     print("Failed")
    Failed
    >>> inst.a = 10  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    AttributeError: can't delete attribute   (but message varies slightly)
    """
    value = cython.declare(cython.int)

    def __init__(self):
        self.value = 0

    # On Python 3 + Cython:
    #  a can get
    #  b can get set
    #  c can get set delete
    # On (pure) Python 2 it's a bit of a mess and doesn't seem reproducible so don't test this!
    @property
    def a(self):
        return self.value
    @a.setter
    def b(self, value):
        self.value = value
    @b.deleter
    def c(self):
        self.value = -100

_WARNINGS = """
55:4: Mismatching property names, expected 'a', got 'b'
58:4: Mismatching property names, expected 'b', got 'c'
"""
