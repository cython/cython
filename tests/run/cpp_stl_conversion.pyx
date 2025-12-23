# mode: run
# tag: cpp, werror, cpp11

from collections import defaultdict

from libcpp.map cimport map
from libcpp.unordered_map cimport unordered_map
from libcpp.set cimport set as cpp_set
from libcpp.unordered_set cimport unordered_set
from libcpp.string cimport string
from libcpp.pair cimport pair
from libcpp.vector cimport vector
from libcpp.list cimport list as cpp_list

py_set = set
py_xrange = xrange
py_unicode = unicode

include "skip_limited_api_helper.pxi"

cdef string add_strings(string a, string b) except *:
    return a + b

# TODO: print bytes values instead of decoding them.
def decode(bytes b):
    return b.decode("ascii")


def test_string(o):
    """
    >>> decode(test_string("abc".encode('ascii')))
    'abc'
    >>> decode(test_string("abc\\x00def".encode('ascii')))
    'abc\\x00def'
    """
    cdef string s = o
    return s

def test_encode_to_string(o):
    """
    >>> decode(test_encode_to_string('abc'))
    'abc'
    >>> decode(test_encode_to_string('abc\\x00def'))
    'abc\\x00def'
    """
    cdef string s = o.encode('ascii')
    return s

def test_encode_to_string_cast(o):
    """
    >>> decode(test_encode_to_string_cast('abc'))
    'abc'
    >>> decode(test_encode_to_string_cast('abc\\x00def'))
    'abc\\x00def'
    """
    s = <string>o.encode('ascii')
    return s

def test_unicode_encode_to_string(unicode o):
    """
    >>> decode(test_unicode_encode_to_string(py_unicode('abc')))
    'abc'
    >>> decode(test_unicode_encode_to_string(py_unicode('abc\\x00def')))
    'abc\\x00def'
    """
    cdef string s = o.encode('ascii')
    return s

def test_string_call(a, b):
    """
    >>> decode(test_string_call("abc".encode('ascii'), "xyz".encode('ascii')))
    'abcxyz'
    """
    return add_strings(a, b)

def test_c_string_convert(char *c_string):
    """
    >>> decode(test_c_string_convert("abc".encode('ascii')))
    'abc'
    """
    cdef string s
    with nogil:
        s = c_string
    return s

def test_bint_vector(o):
    """
    https://github.com/cython/cython/issues/5516
    Creating the "bint" specialization used to mess up the
    "int" specialization.

    >>> test_bint_vector([False, True])
    [False, True]
    >>> test_bint_vector(py_xrange(0,5))
    [False, True, True, True, True]
    >>> test_bint_vector(["", "hello"])
    [False, True]
    """

    cdef vector[bint] v = o
    return v

def test_int_vector(o):
    """
    >>> test_int_vector([1, 2, 3])
    [1, 2, 3]
    >>> test_int_vector((1, 10, 100))
    [1, 10, 100]
    >>> test_int_vector(py_xrange(1,10,2))
    [1, 3, 5, 7, 9]
    >>> test_int_vector([10**20])       #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...
    """
    cdef vector[int] v = o
    return v

cdef vector[int] takes_vector(vector[int] x):
    assert x[2] == 3
    return x

def test_list_literal_to_vector():
    """
    >>> test_list_literal_to_vector()
    [1, 2, 3]
    """
    return takes_vector([1, 2, 3])

def test_tuple_literal_to_vector():
    """
    >>> test_tuple_literal_to_vector()
    [1, 2, 3]
    """
    return takes_vector((1, 2, 3))

def test_generator_to_vector():
    """
    >>> test_generator_to_vector()
    [1, 2, 3]
    """
    g = (x for x in [1, 2, 3])
    return takes_vector(g)

class LengthlessIterable(object):
    def __getitem__(self, pos):
        if pos == 3:
            raise StopIteration
        return pos+1

class LengthlessIterableRaises(LengthlessIterable):
    def __length_hint__(self):
        raise Exception('__length_hint__ called')

def test_iterable_to_vector():
    """
    >>> test_iterable_to_vector()
    [1, 2, 3]
    """
    i = LengthlessIterable()
    return takes_vector(i)

@skip_if_limited_api("__length_hint__ isn't called in Limited API")
def test_iterable_raises_to_vector():
    """
    >>> test_iterable_raises_to_vector()
    Traceback (most recent call last):
    ...
    Exception: __length_hint__ called
    """
    i = LengthlessIterableRaises()
    return takes_vector(i)

def test_string_vector(s):
    """
    >>> list(map(decode, test_string_vector('ab cd ef gh'.encode('ascii'))))
    ['ab', 'cd', 'ef', 'gh']
    """
    cdef vector[string] cpp_strings = s.split()
    return cpp_strings

cdef list convert_string_vector(vector[string] vect):
    return vect

def test_string_vector_temp_funcarg(s):
    """
    >>> list(map(decode, test_string_vector_temp_funcarg('ab cd ef gh'.encode('ascii'))))
    ['ab', 'cd', 'ef', 'gh']
    """
    return convert_string_vector(s.split())

def test_double_vector(o):
    """
    >>> test_double_vector([1, 2, 3])
    [1.0, 2.0, 3.0]
    >>> test_double_vector([10**20])
    [1e+20]
    """
    cdef vector[double] v = o
    return v

def test_repeated_double_vector(a, b, int n):
    """
    >>> test_repeated_double_vector(1, 1.5, 3)
    [1.0, 1.5, 1.0, 1.5, 1.0, 1.5]
    """
    cdef vector[double] v = [a, b] * n
    return v

ctypedef int my_int

def test_typedef_vector(o):
    """
    >>> test_typedef_vector([1, 2, 3])
    [1, 2, 3]
    >>> test_typedef_vector([1, 2, 3**100])       #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...

    "TypeError: an integer is required" on CPython
    >>> test_typedef_vector([1, 2, None])       #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...int...
    """
    cdef vector[my_int] v = o
    return v

def test_pair(o):
    """
    >>> test_pair((1, 2))
    (1, 2.0)
    """
    cdef pair[long, double] p = o
    return p

def test_list(o):
    """
    >>> test_list([1, 2, 3])
    [1, 2, 3]
    """
    cdef cpp_list[int] l = o
    return l

def test_set(o):
    """
    >>> sorted(test_set([1, 2, 3]))
    [1, 2, 3]
    >>> sorted(test_set([1, 2, 3, 3]))
    [1, 2, 3]
    >>> type(test_set([])) is py_set
    True
    """
    cdef cpp_set[long] s = o
    return s

def test_unordered_set(o):
   """
   >>> sorted(test_unordered_set([1, 2, 3]))
   [1, 2, 3]
   >>> sorted(test_unordered_set([1, 2, 3, 3]))
   [1, 2, 3]
   >>> type(test_unordered_set([])) is py_set
   True
   """
   cdef unordered_set[long] s = o
   return s

def test_map(o):
    """
    >>> d = {1: 1.0, 2: 0.5, 3: 0.25}
    >>> test_map(d)
    {1: 1.0, 2: 0.5, 3: 0.25}
    >>> dd = defaultdict(float)
    >>> dd.update(d)
    >>> test_map(dd)  # try with a non-dict
    {1: 1.0, 2: 0.5, 3: 0.25}
    """
    cdef map[int, double] m = o
    return m

def test_unordered_map(o):
    """
    >>> d = {1: 1.0, 2: 0.5, 3: 0.25}
    >>> m = test_map(d)
    >>> sorted(m)
    [1, 2, 3]
    >>> (m[1], m[2], m[3])
    (1.0, 0.5, 0.25)

    >>> dd = defaultdict(float)
    >>> dd.update(d)
    >>> m = test_map(dd)
    >>> sorted(m)
    [1, 2, 3]
    >>> (m[1], m[2], m[3])
    (1.0, 0.5, 0.25)
    """
    cdef unordered_map[int, double] m = o
    return m

def test_nested(o):
    """
    >>> test_nested({})
    {}
    >>> d = test_nested({(1.0, 2.0): [1, 2, 3], (1.0, 0.5): [1, 10, 100]})
    >>> type(d) is dict or type(d)
    True
    >>> sorted(d)
    [(1.0, 0.5), (1.0, 2.0)]
    >>> d[(1.0, 0.5)]
    [1, 10, 100]
    >>> d[(1.0, 2.0)]
    [1, 2, 3]
    """
    cdef map[pair[double, double], vector[int]] m = o
    return m

cpdef enum Color:
    RED = 0
    GREEN
    BLUE

def test_enum_map(o):
    """
    >>> test_enum_map({Color.RED: Color.GREEN})
    {<Color.RED: 0>: <Color.GREEN: 1>}
    """
    cdef map[Color, Color] m = o
    return m

cdef map[unsigned int, unsigned int] takes_map(map[unsigned int, unsigned int] m):
    return m

def test_dict_literal_to_map():
    """
    >>> test_dict_literal_to_map()
    {1: 1}
    """
    return takes_map({1: 1})  # https://github.com/cython/cython/pull/4228
                              # DictNode could not be converted directly
