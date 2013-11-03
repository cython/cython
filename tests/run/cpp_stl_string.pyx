# tag: cpp

cimport cython

from libcpp.string cimport string

b_asdf = b'asdf'
b_asdg = b'asdg'
b_s = b's'

def test_indexing(char *py_str):
    """
    >>> test_indexing(b_asdf)
    ('s', 's')
    """
    cdef string s
    s = string(py_str)
    return chr(s[1]), chr(s.at(1))

def test_size(char *py_str):
    """
    >>> test_size(b_asdf)
    (4, 4)
    """
    cdef string s
    s = string(py_str)
    return s.size(), s.length()

def test_compare(char *a, char *b):
    """
    >>> test_compare(b_asdf, b_asdf)
    0

    >>> test_compare(b_asdf, b_asdg) < 0
    True
    """
    cdef string s = string(a)
    cdef string t = string(b)
    return s.compare(t)

def test_empty():
    """
    >>> test_empty()
    (True, False)
    """
    cdef string a = string(<char *>b"")
    cdef string b = string(<char *>b"aa")
    return a.empty(), b.empty()

def test_push_back(char *a):
    """
    >>> test_push_back(b_asdf) == b_asdf + b_s
    True
    """
    cdef string s = string(a)
    s.push_back(<char>ord('s'))
    return s.c_str()

def test_insert(char *a, char *b, int i):
    """
    >>> test_insert('AAAA'.encode('ASCII'), 'BBBB'.encode('ASCII'), 2) == 'AABBBBAA'.encode('ASCII')
    True
    """
    cdef string s = string(a)
    cdef string t = string(b)
    cdef string u = s.insert(i, t)
    return u.c_str()

def test_copy(char *a):
    """
    >>> test_copy(b_asdf) == b_asdf[1:]
    True
    """
    cdef string t = string(a)
    cdef char buffer[6]
    cdef size_t length = t.copy(buffer, 4, 1)
    buffer[length] = c'\0'
    return buffer

def test_find(char *a, char *b):
    """
    >>> test_find(b_asdf, 'df'.encode('ASCII'))
    2
    """
    cdef string s = string(a)
    cdef string t = string(b)
    cdef size_t i = s.find(t)
    return i

def test_clear():
    """
    >>> test_clear() == ''.encode('ASCII')
    True
    """
    cdef string s = string(<char *>"asdf")
    s.clear()
    return s.c_str()

def test_assign(char *a):
    """
    >>> test_assign(b_asdf) == 'ggg'.encode('ASCII')
    True
    """
    cdef string s = string(a)
    s.assign(<char *>"ggg")
    return s.c_str()


def test_substr(char *a):
    """
    >>> test_substr('ABCDEFGH'.encode('ASCII')) == ('BCDEFGH'.encode('ASCII'), 'BCDE'.encode('ASCII'), 'ABCDEFGH'.encode('ASCII'))
    True
    """
    cdef string s = string(a)
    cdef string x, y, z
    x = s.substr(1)
    y = s.substr(1, 4)
    z = s.substr()
    return x.c_str(), y.c_str(), z.c_str()

def test_append(char *a, char *b):
    """
    >>> test_append(b_asdf, '1234'.encode('ASCII')) == b_asdf + '1234'.encode('ASCII')
    True
    """
    cdef string s = string(a)
    cdef string t = string(b)
    cdef string j = s.append(t)
    return j.c_str()

def test_char_compare(py_str):
    """
    >>> test_char_compare(b_asdf)
    True
    """
    cdef char *a = py_str
    cdef string b = string(a)
    return b.compare(b) == 0

def test_cstr(char *a):
    """
    >>> test_cstr(b_asdf) == b_asdf
    True
    """
    cdef string b = string(a)
    return b.c_str()

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode(char* a):
    """
    >>> print(test_decode(b_asdf))
    asdf
    """
    cdef string b = string(a)
    return b.decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced(char* a):
    """
    >>> print(test_decode_sliced(b_asdf))
    sd
    """
    cdef string b = string(a)
    return b[1:3].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_negative(char* a):
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
    cdef string b = string(a)
    return b[-3:-1].decode('ascii'), b[-5:-3].decode('ascii'), b[-20:-4].decode('ascii'), b[-2:-20].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_end(char* a):
    """
    >>> a,b = test_decode_sliced_end(b_asdf)
    >>> print(a)
    asd
    >>> print(b)
    asdf
    """
    cdef string b = string(a)
    return b[:3].decode('ascii'), b[:42].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_end_negative(char* a):
    """
    >>> a,b,c = test_decode_sliced_end_negative(b_asdf)
    >>> print(a)
    asd
    >>> print(b)
    a
    >>> print(c)
    <BLANKLINE>
    """
    cdef string b = string(a)
    return b[:-1].decode('ascii'), b[:-3].decode('ascii'), b[:-4].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_start(char* a):
    """
    >>> print(test_decode_sliced_start(b_asdf))
    df
    """
    cdef string b = string(a)
    return b[2:].decode('ascii')

@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_decode_sliced_start_negative(char* a):
    """
    >>> a,b = test_decode_sliced_start_negative(b_asdf)
    >>> print(a)
    df
    >>> print(b)
    asdf
    """
    cdef string b = string(a)
    return b[-2:].decode('ascii'), b[-20:].decode('ascii')

def test_equals_operator(char *a, char *b):
    """
    >>> test_equals_operator(b_asdf, b_asdf)
    (True, False)
    """
    cdef string s = string(a)
    cdef string t = string(b)
    return t == s, t != <char *>"asdf"

def test_less_than(char *a, char *b):
    """
    >>> test_less_than(b_asdf[:-1], b_asdf)
    (True, True, True)

    >>> test_less_than(b_asdf[:-1], b_asdf[:-1])
    (False, False, True)
    """
    cdef string s = string(a)
    cdef string t = string(b)
    return (s < t, s < b, s <= b)

def test_greater_than(char *a, char *b):
    """
    >>> test_greater_than(b_asdf[:-1], b_asdf)
    (False, False, False)

    >>> test_greater_than(b_asdf[:-1], b_asdf[:-1])
    (False, False, True)
    """
    cdef string s = string(a)
    cdef string t = string(b)
    return (s > t, s > b, s >= b)
