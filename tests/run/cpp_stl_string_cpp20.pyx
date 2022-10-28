# mode: run
# tag: cpp, werror, cpp20

from libcpp cimport bool
from libcpp cimport string

b_A = b'A'
b_F = b'F'
b_abc = b"ABC"
b_def = b"DEF"

def test_string_starts_with_char(py_obj1):
    """
    Test std::string.starts_with() with char type argument
    >>> test_string_starts_with_char(b_A)
    True
    >>> test_string_starts_with_char(b_F)
    False
    """
    cdef char c = py_obj1
    cdef string s = b"ABCDEF"
    return s.starts_with(c)


def test_string_starts_with_cstr(py_obj1):
    """
    Test std::string.starts_with() with c str type argument (char*)
    >>> test_string_starts_cstr(b_abc)
    True
    >>> test_string_starts_cstr(b_def)
    False
    """
    cdef char* c = py_obj1
    cdef string s = b"ABCDEF"
    return s.starts_with(c)


def test_string_ends_with_char(py_obj1):
    """
    Test std::string.ends_with() with char type argument
    >>> test_string_ends_with_char(b_F)
    True
    >>> test_string_ends_with_char(b_A)
    False
    """
    cdef char c = py_obj1
    cdef string s = b"ABCDEF"
    return s.ends_with(c)


def test_string_ends_with_cstr(py_obj1):
    """
    Test std::string.ends_with() with c str type argument (char*)
    >>> test_string_ends_with_cstr(b_def)
    True
    >>> test_string_ends_with_cstr(b_abc)
    False
    """
    cdef char* c = py_obj1
    cdef string s = b"ABCDEF"
    return s.ends_with(c)