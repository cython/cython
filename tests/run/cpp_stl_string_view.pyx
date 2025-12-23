# ticket: 6651
# mode: run
# tag: cpp, cpp17

cimport cython

from libcpp.string cimport string
from libcpp.string_view cimport string_view, npos
from cython.operator cimport dereference as deref, preincrement as preinc, predecrement as predec

b_asdf = b'asdf'
b_asdg = b'asdg'
b_s = b's'


cdef int compare_to_asdf(string_view s) except -999:
    return s.compare(b"asdf")

def test_coerced_literal_ref():
    """
    >>> test_coerced_literal_ref()
    0
    """
    return compare_to_asdf("asdf")


cdef return_to_py():
    return string_view(b"asdf")

def test_return_to_py():
    """
    >>> test_return_to_py() == b_asdf
    True
    """
    return return_to_py()


def test_constructors(py_str):
    """
    >>> b_s_7 = b_s * 7
    >>> test_constructors(b_s_7) == (b'', b_s, b_s * 3) + (b_s_7, ) * 5
    True
    """
    cdef string s = py_str
    cdef string_view view1 = s
    cdef string_view substr1 = view1.substr(3, 1)
    cdef string_view substr2 = string_view(view1.data(), 3)
    cdef string_view view2 = string_view(view1.data())
    cdef string_view view3 = string_view(view1)
    cdef string_view view4 = string_view(view1.data(), view1.size())
    cdef string_view view5
    view5 = view2

    return (string_view(), substr1, substr2, view1, view2, view3, view4, view5)


def test_iterators(string_view s):
    """
    >>> test_iterators(b'XXX hello, world! XXX')
    (True, True)
    """
    cdef size_t c1 = 0, c2 = 0

    cdef string_view.iterator it = s.begin()
    cdef string_view.reverse_iterator rit = s.rbegin()

    preinc(it)
    preinc(rit)

    assert deref(it + 1) == deref(rit + 1)
    assert deref(it - 1) == deref(rit - 1)

    assert it - 1 < it and it < it + 1
    assert it - 1 <= it and it <= it + 1
    assert it + 1 > it and it > it - 1
    assert it + 1 >= it and it >= it - 1

    assert rit - 1 < rit and rit < rit + 1
    assert rit - 1 <= rit and rit <= rit + 1
    assert rit + 1 > rit and rit > rit - 1
    assert rit + 1 >= rit and rit >= rit - 1

    assert it == it and it != it + 1
    assert rit == rit and rit != rit + 1

    predec(it)
    predec(rit)

    while it != s.end():
        preinc(it)
        preinc(c1)

    while rit != s.rend():
        preinc(rit)
        preinc(c2)

    return c1 == s.size(), c1 == c2


def test_access(string_view s, i):
    """
    >>> test_access(b_asdf, 1) == (ord(b_asdf[1:2]), ) * 2
    True
    >>> test_access(b_asdf, 5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    IndexError: ...
    """
    return s.at(i), s[i]


def test_empty(string_view s1, string_view s2):
    """
    >>> test_empty(b'', b_asdf)
    (True, False)
    """
    return s1.empty(), s2.empty()


def test_size(string_view s):
    """
    >>> test_size(b_asdf)
    (4, 4)
    """
    return s.size(), s.length()


def test_npos(string_view a, string_view b):
    """
    >>> test_npos(b'abc', b'x')
    True
    >>> test_npos(b'abc', b'a')
    False
    """
    return a.find(b) == npos


def test_compare(string_view s1, string_view s2):
    """
    >>> all(map(lambda x: x == 0, test_compare(b_asdf, b_asdf)))
    True

    >>> all(map(lambda x: x > 0, test_compare(b_asdf, b_asdg)))
    True
    """
    return (s2.compare(s1),
            s2.compare(0, s1.size(), s1),
            s2.compare(0, s1.size(), s1, 0, s1.size()),
            s2.compare(s1.data()),
            s2.compare(0, s1.size(), s1.data()),
            s2.compare(0, s1.size(), s1.data(), s1.size()))


def test_substr(string_view s):
    """
    >>> b_test_str = b'ABCDEFGH'
    >>> test_substr(b_test_str) == (b_test_str, b_test_str[1:], b_test_str[1:5])
    True
    """
    cdef string_view o1, o2, o3
    o1 = s.substr()
    o2 = s.substr(1)
    o3 = s.substr(1, 4)
    return o1, o2, o3


def test_copy(string_view s):
    """
    >>> test_copy(b_asdf) == (b_asdf[:3], b_asdf[1:])
    True
    """
    cdef char[5] buffer1, buffer2
    cdef size_t length1 = s.copy(buffer1, 3)
    cdef size_t length2 = s.copy(buffer2, 4, 1)
    buffer1[length1] = c'\0'
    buffer2[length2] = c'\0'
    return buffer1, buffer2


def test_swap(string_view s1, string_view s2):
    """
    >>> test_swap(b_asdf, b_asdg) == (b_asdg, b_asdf)
    True
    """
    s1.swap(s2)
    return s1, s2


def test_find(string_view s1, string_view s2):
    """
    >>> all(map(lambda x: x == 2, test_find(b_asdf, b_asdf[2:])))
    True
    """
    return (s1.find(s2),
            s1.find(s2, 1),
            s1.find(s2.data(), 0, s2.size()),
            s1.find(s2.data()),
            s1.find(s2.data(), 0),
            s1.find(s2.at(0), 0))


def test_rfind(string_view s1, string_view s2):
    """
    >>> all(map(lambda x: x == 2, test_rfind(b_asdf, b_asdf[2:])))
    True
    """
    return (s1.rfind(s2),
            s1.rfind(s2, s1.size() - 2),
            s1.rfind(s2.data(), s1.size() - 2, s2.size()),
            s1.rfind(s2.data()),
            s1.rfind(s2.data(), s1.size() - 2),
            s1.rfind(s2.at(0), s1.size() - 2))


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode(string_view a):
    """
    >>> print(test_decode(b_asdf))
    asdf
    """
    return a.decode('ascii')


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced(string_view a):
    """
    >>> print(test_decode_sliced(b_asdf))
    sd
    """
    return a[1:3].decode('ascii')


def test_equals_operator(char *a, string_view b):
    """
    >>> test_equals_operator(b_asdf, b_asdf)
    (True, False)
    """
    cdef string_view s = string_view(a)
    return b == s, b != <char *>"asdf"


def test_less_than(string_view a, char *b):
    """
    >>> test_less_than(b_asdf[:-1], b_asdf)
    (True, True, True)

    >>> test_less_than(b_asdf[:-1], b_asdf[:-1])
    (False, False, True)
    """
    cdef string_view t = string_view(b)
    return (a < t, a < b, a <= b)


def test_greater_than(string_view a, char *b):
    """
    >>> test_greater_than(b_asdf[:-1], b_asdf)
    (False, False, False)

    >>> test_greater_than(b_asdf[:-1], b_asdf[:-1])
    (False, False, True)
    """
    cdef string_view t = string_view(b)
    return (a > t, a > b, a >= b)


def test_iteration(string_view s):
    """
    >>> test_iteration(b'xyz')
    [120, 121, 122]
    >>> test_iteration(b'')
    []
    """
    return [c for c in s]
