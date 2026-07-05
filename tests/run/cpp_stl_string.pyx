# mode: run
# tag: cpp, no-cpp-locals, warnings

cimport cython

from libcpp.string cimport string, npos, to_string, stoi, stof
from cython.operator cimport dereference as deref, preincrement as preinc, predecrement as predec

b_asdf = b'asdf'
b_asdg = b'asdg'
b_s = b's'


cdef int compare_to_asdf_ref(string& s) except -999:
    return s.compare(b"asdf")

def test_coerced_literal_ref():
    """
    >>> test_coerced_literal_ref()
    0
    """
    return compare_to_asdf_ref("asdf")


cdef int compare_to_asdf_const_ref(const string& s) except -999:
    return s.compare(b"asdf")

def test_coerced_literal_const_ref():
    """
    >>> test_coerced_literal_const_ref()
    0
    """
    return compare_to_asdf_const_ref("asdf")


cdef int compare_to_asdf_const(const string s) except -999:
    return s.compare(b"asdf")

def test_coerced_literal_const():
    """
    >>> test_coerced_literal_const()
    0
    """
    return compare_to_asdf_const("asdf")


def test_conversion(py_obj):
    """
    >>> test_conversion(b_asdf) == b_asdf or test_conversion(b_asdf)
    True
    >>> test_conversion(123)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: expected ..., int found
    """
    cdef string s = py_obj
    return s

def test_constructors(ch):
    """
    >>> b_s_7 = b_s * 7
    >>> test_constructors(b_s) == (b'', b_s, b_s * 3) + (b_s_7, ) * 5
    True
    """
    cdef string clone1 = string(7, <char>ord(ch))
    cdef string substr1 = string(clone1, 3, 1)
    cdef string substr2 = string(clone1.c_str(), 3)
    cdef string clone2 = string(clone1.c_str())
    cdef string clone3 = string(clone1)
    cdef string clone4 = string(clone1.begin(), clone1.end())
    cdef string clone5 = string(clone1.rbegin(), clone1.rend())

    return string(), substr1, substr2, clone1, clone2, clone3, clone4, clone5

def test_iterators(string s):
    """
    >>> test_iterators(b'XXX hello, world! XXX')
    (True, True)
    """
    cdef size_t c1 = 0, c2 = 0

    cdef string.iterator it = s.begin()
    cdef string.reverse_iterator rit = s.rbegin()

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

def test_assign(string s_asdf, string s_asdg):
    """
    >>> test_assign(b_asdf, b_asdg) == (b'XXXXXXX', b_asdf, b_asdf[0:2], b_asdg, b_asdf, b_asdg)
    True
    """
    cdef string s1, s2, s3, s4, s5, s6

    s1.assign(7, <char>ord('X'))
    s2.assign(s_asdf)
    s3.assign(s_asdf, 0, 2)
    s4.assign(s_asdg.c_str(), 4)
    s5.assign(s_asdf.c_str())
    s6.assign(s_asdg.begin(), s_asdg.end())

    return (s1, s2, s3, s4, s5, s6)

def test_access(string s, i):
    """
    >>> test_access(b_asdf, 1) == (ord(b_asdf[1:2]), ) * 2
    True
    >>> test_access(b_asdf, 5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    IndexError: ...
    """
    return s.at(i), s[i]

def test_empty(string s1, string s2):
    """
    >>> test_empty(b'', b_asdf)
    (True, False)
    """
    return s1.empty(), s2.empty()

def test_size(string s):
    """
    >>> test_size(b_asdf)
    (4, 4)
    """
    return s.size(), s.length()

def test_capacity(string s):
    """
    >>> test_capacity(b_asdf)
    (True, True)
    """
    s.reserve(9)
    s.resize(5)
    s.resize(7, <char>ord('X'))
    return s.max_size() > 0, s.capacity() > 0

def test_cstr(string s):
    """
    >>> test_cstr(b_asdf) == b_asdf
    True
    """
    return s.c_str()

def test_clear(string s):
    """
    >>> test_clear(b_asdf) == b''
    True
    """
    s.clear()
    return s

def test_insert(string a, string b, int i):
    """
    >>> test_insert(b'AAAA', b'BBBB', 2) == (b'AAAA', True, b'AA' + b'B' * 4 * 4 + b'AA')
    True
    """
    cdef string s = a
    s.insert(i, b)
    s.insert(i, b, 0, b.size())
    s.insert(i, b.c_str())
    cdef string o = s.insert(i, b.c_str(), b.size())
    return (a, s == o, s)

def test_insert_iterator(string s):
    """
    >>> test_insert_iterator(b_asdf) == b_asdf[:2] + b_asdf
    True
    """
    cdef string o = string()
    cdef string.iterator it = o.insert(o.end(), s.at(0))
    o.insert(o.end(), 1, s.at(1))
    o.insert(o.end(), s.begin(), s.end())
    return o

def test_pop_back(string a):
    """
    >>> test_pop_back(b'abc') == b'ab' or test_pop_back(b'abc')
    True
    """
    a.pop_back()
    return a

def test_erase(string s):
    """
    >>> test_erase(b_asdf) == (b'', b_asdf[:2], b_asdf[2:], b_asdf[1:], b_asdf[2:])
    True
    """
    cdef string o1, o2, o3, o4, o5
    o1, o2, o3, o4, o5 = (s, ) * 5
    o1.erase()
    o2.erase(2)
    o3.erase(0, 2)
    o4.erase(o4.begin())
    o5.erase(o5.begin(), o5.begin() + 2)
    return o1, o2, o3, o4, o5

def test_push_back(string s, a):
    """
    >>> test_push_back(b_asdf, b_s) == b_asdf + b_s
    True
    """
    s.push_back(<char>ord(a))
    return s

def test_npos(string a, string b):
    """
    >>> test_npos(b'abc', b'x')
    True
    >>> test_npos(b'abc', b'a')
    False
    """
    return a.find(b) == npos

def test_append(string s1, string s2):
    """
    >>> b_1234 = b'1234'
    >>> test_append(b_asdf, b_1234) == (True, b_asdf + b_1234 * 3 + b_1234[0:1] * 4)
    True
    """
    s1.append(s2)
    s1.append(s2.begin(), s2.end())
    s1.append(s2.c_str())
    s1.append(s2.c_str(), 1)
    s1.append(2, s2[0])
    cdef string oo = s1.append(s2, 0, 1)
    return (s1 == oo, s1)

def test_compare(string s1, string s2):
    """
    >>> all(map(lambda x: x == 0, test_compare(b_asdf, b_asdf)))
    True

    >>> all(map(lambda x: x > 0, test_compare(b_asdf, b_asdg)))
    True
    """
    return (s2.compare(s1),
            s2.compare(0, s1.size(), s1),
            s2.compare(0, s1.size(), s1, 0, s1.size()),
            s2.compare(s1.c_str()),
            s2.compare(0, s1.size(), s1.c_str()),
            s2.compare(0, s1.size(), s1.c_str(), s1.size()))

def test_replace(string s1, string s2):
    """
    >>> test_replace(b_asdf, b_asdg) == (b_asdg, ) * 6
    True
    """
    cdef string o1, o2, o3, o4, o5, o6
    o1, o2, o3, o4, o5, o6 = (s1, ) * 6
    o1.replace(0, s2.size(), s2)
    o2.replace(0, s2.size(), s2, 0, s2.size())
    o3.replace(0, s2.size(), s2.c_str(), s2.size())
    o4.replace(0, s2.size(), s2.c_str())
    o5.replace(s2.size() - 1, 1, 1, deref(s2.rbegin()))
    o6.replace(o6.begin(), o6.end(), s2.begin(), s2.end())
    return o1, o2, o3, o4, o5, o6

def test_substr(string s):
    """
    >>> b_test_str = b'ABCDEFGH'
    >>> test_substr(b_test_str) == (b_test_str, b_test_str[1:], b_test_str[1:5])
    True
    """
    cdef string o1, o2, o3
    o1 = s.substr()
    o2 = s.substr(1)
    o3 = s.substr(1, 4)
    return o1, o2, o3

def test_copy(string s):
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

def test_swap(string s1, string s2):
    """
    >>> test_swap(b_asdf, b_asdg) == (b_asdg, b_asdf)
    True
    """
    s1.swap(s2)
    return s1, s2

def test_find(string s1, string s2):
    """
    >>> all(map(lambda x: x == 2, test_find(b_asdf, b_asdf[2:])))
    True
    """
    return (s1.find(s2),
            s1.find(s2, 1),
            s1.find(s2.c_str(), 0, s2.size()),
            s1.find(s2.c_str()),
            s1.find(s2.c_str(), 0),
            s1.find(s2.at(0), 0))

def test_rfind(string s1, string s2):
    """
    >>> all(map(lambda x: x == 2, test_rfind(b_asdf, b_asdf[2:])))
    True
    """
    return (s1.rfind(s2),
            s1.rfind(s2, s1.size() - 2),
            s1.rfind(s2.c_str(), s1.size() - 2, s2.size()),
            s1.rfind(s2.c_str()),
            s1.rfind(s2.c_str(), s1.size() - 2),
            s1.rfind(s2.at(0), s1.size() - 2))

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode(string a):
    """
    >>> print(test_decode(b_asdf))
    asdf
    """
    return a.decode('ascii')


@cython.test_assert_path_exists("//ReturnStatNode//PythonCapiCallNode")
def test_cstr_decode(string a):
    """
    >>> print(test_cstr_decode(b_asdf))
    asdf
    """
    return a.c_str().decode('utf-8')


@cython.test_assert_path_exists("//ReturnStatNode//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//ReturnStatNode//AttributeNode")
def test_cstr_ptr_decode(string a):
    """
    >>> print(test_cstr_ptr_decode(b_asdf))
    asdf
    """
    s = a.c_str()
    return s.decode('utf-8')


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced(string a):
    """
    >>> print(test_decode_sliced(b_asdf))
    sd
    """
    return a[1:3].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_negative(string a):
    """
    >>> a,b,c,d = test_decode_sliced_negative(b_asdf)
    >>> print(a)
    sd
    >>> print(b)
    a
    >>> print(c)
    <BLANKLINE>
    >>> print(d)
    <BLANKLINE>
    """
    return a[-3:-1].decode('ascii'), a[-5:-3].decode('ascii'), a[-20:-4].decode('ascii'), a[-2:-20].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_end(string a):
    """
    >>> a,b = test_decode_sliced_end(b_asdf)
    >>> print(a)
    asd
    >>> print(b)
    asdf
    """
    return a[:3].decode('ascii'), a[:42].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_end_negative(string a):
    """
    >>> a,b,c = test_decode_sliced_end_negative(b_asdf)
    >>> print(a)
    asd
    >>> print(b)
    a
    >>> print(c)
    <BLANKLINE>
    """
    return a[:-1].decode('ascii'), a[:-3].decode('ascii'), a[:-4].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_start(string a):
    """
    >>> print(test_decode_sliced_start(b_asdf))
    df
    """
    return a[2:].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_start_negative(string a):
    """
    >>> a,b = test_decode_sliced_start_negative(b_asdf)
    >>> print(a)
    df
    >>> print(b)
    asdf
    """
    return a[-2:].decode('ascii'), a[-20:].decode('ascii')

def test_equals_operator(char *a, string b):
    """
    >>> test_equals_operator(b_asdf, b_asdf)
    (True, False)
    """
    cdef string s = string(a)
    return b == s, b != <char *>"asdf"

def test_less_than(string a, char *b):
    """
    >>> test_less_than(b_asdf[:-1], b_asdf)
    (True, True, True)

    >>> test_less_than(b_asdf[:-1], b_asdf[:-1])
    (False, False, True)
    """
    cdef string t = string(b)
    return (a < t, a < b, a <= b)

def test_greater_than(string a, char *b):
    """
    >>> test_greater_than(b_asdf[:-1], b_asdf)
    (False, False, False)

    >>> test_greater_than(b_asdf[:-1], b_asdf[:-1])
    (False, False, True)
    """
    cdef string t = string(b)
    return (a > t, a > b, a >= b)


def test_iteration(string s):
    """
    >>> test_iteration(b'xyz')
    [120, 121, 122]
    >>> test_iteration(b'')
    []
    """
    return [c for c in s]


def test_to_string(x):
    """
    >>> print(test_to_string(5))
    si=5 sl=5 ss=5 sss=5
    >>> print(test_to_string(-5))
    si=-5 sl=-5 ss=5 sss=-5
    """
    si = to_string(<int>x).decode('ascii')
    sl = to_string(<long>x).decode('ascii')
    ss = to_string(<size_t>abs(x)).decode('ascii')
    sss = to_string(<ssize_t>x).decode('ascii')
    return f"si={si} sl={sl} ss={ss} sss={sss}"


def test_stoi(string a):
    """
    >>> test_stoi(b'5')
    5
    """
    return stoi(a)


def test_stof(string a):
    """
    >>> test_stof(b'5.5')
    5.5
    """
    return stof(a)


def test_float_parsing(string a):
    """
    >>> test_float_parsing(b'0.5')
    0.5
    >>> try: test_float_parsing(b'xxx')
    ... except ValueError: pass
    ... else: print("NOT RAISED!")
    >>> try: test_float_parsing(b'')
    ... except ValueError: pass
    ... else: print("NOT RAISED!")
    """
    return float(a)


_WARNINGS = """
22:31: Cannot pass Python object as C++ data structure reference (string &), will pass by copy.
"""
