# mode: run
# tag: cpp, werror, cpp20

from libcpp cimport bool
from libcpp.string cimport string

b_A = b'A'
b_F = b'F'
b_abc = b"ABC"
b_def = b"DEF"

def test_string_starts_with_char(bytes py_str):
    """
    Test std::string.starts_with() with char type argument
    >>> test_string_starts_with_char(b'A')
    True
    >>> test_string_starts_with_char(b'F')
    False
    """
    cdef char c = py_str[0]
    cdef string s = b"ABCDEF"
    return s.starts_with(c)


def test_string_starts_with_cstr(bytes py_str):
    """
    Test std::string.starts_with() with c str type argument (char*)
    >>> test_string_starts_with_cstr(b"ABC")
    True
    >>> test_string_starts_with_cstr(b"DEF")
    False
    """
    cdef char* c = py_str
    cdef string s = b"ABCDEF"
    return s.starts_with(c)


def test_string_ends_with_char(bytes py_str):
    """
    Test std::string.ends_with() with char type argument
    >>> test_string_ends_with_char(b'F')
    True
    >>> test_string_ends_with_char(b'A')
    False
    """
    cdef char c = py_str[0]
    cdef string s = b"ABCDEF"
    return s.ends_with(c)


def test_string_ends_with_cstr(bytes py_str):
    """
    Test std::string.ends_with() with c str type argument (char*)
    >>> test_string_ends_with_cstr(b"DEF")
    True
    >>> test_string_ends_with_cstr(b"ABC")
    False
    """
    cdef char* c = py_str
    cdef string s = b"ABCDEF"
    return s.ends_with(c)