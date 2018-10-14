# cython: language_level=3str, binding=True
# mode: run
# tag: python3, str_is_str

print(end='')  # test that language_level 3 applies immediately at the module start, for the first token.

__doc__ = """
>>> items = sorted(locals_function(1).items())
>>> for item in items:
...     print('%s = %r' % item)
a = 1
b = 2
x = 'abc'
"""

def locals_function(a, b=2):
    x = 'abc'
    return locals()


### true division

def truediv(x):
    """
    >>> truediv(4)
    2.0
    >>> truediv(3)
    1.5
    """
    return x / 2


def truediv_int(int x):
    """
    >>> truediv_int(4)
    2.0
    >>> truediv_int(3)
    1.5
    """
    return x / 2


### Py3 feature tests

def print_function(*args):
    """
    >>> print_function(1,2,3)
    1 2 3
    """
    print(*args) # this isn't valid Py2 syntax


str_string = "abcdefg"

def no_unicode_literals():
    """
    >>> print( no_unicode_literals() )
    True
    abcdefg

    Testing non-ASCII docstrings: Πυθαγόρας
    """
    print(isinstance(str_string, str) or type(str_string))
    return str_string


def str_type_is_str():
    """
    >>> str_type, s = str_type_is_str()
    >>> isinstance(s, type(str_string)) or (s, str_type)
    True
    >>> isinstance(s, str_type) or (s, str_type)
    True
    >>> isinstance(str_string, str_type) or str_type
    True
    """
    cdef str s = 'abc'
    return str, s


def annotation_syntax(a: "test new test", b : "other" = 2, *args: "ARGS", **kwargs: "KWARGS") -> "ret":
    """
    >>> annotation_syntax(1)
    3
    >>> annotation_syntax(1,3)
    4

    >>> len(annotation_syntax.__annotations__)
    5
    >>> annotation_syntax.__annotations__['a']
    'test new test'
    >>> annotation_syntax.__annotations__['b']
    'other'
    >>> annotation_syntax.__annotations__['args']
    'ARGS'
    >>> annotation_syntax.__annotations__['kwargs']
    'KWARGS'
    >>> annotation_syntax.__annotations__['return']
    'ret'
    """
    result : int = a + b

    return result
