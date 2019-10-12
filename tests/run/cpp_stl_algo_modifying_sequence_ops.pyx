# mode: run
# tag: cpp, werror, cpp11

from cython.operator cimport postincrement
from libcpp cimport bool
from libcpp.algorithm cimport copy, copy_if, copy_n, copy_backward, move, move_backward, fill, fill_n, transform
from libcpp.algorithm cimport generate, generate_n, remove, remove_if, remove_copy, remove_copy_if
from libcpp.iterator cimport back_inserter
from libcpp.string cimport string
from libcpp.vector cimport vector


def copy_int(vector[int] values):
    """
    Test copy.

    >>> copy_int(range(5))
    [0, 1, 2, 3, 4]
    """
    cdef vector[int] out
    copy(values.begin(), values.end(), back_inserter(out))
    return out


cdef bool is_odd(int i):
    return i % 2


def copy_int_if_odd(vector[int] values):
    """
    Test copy_if.

    >>> copy_int_if_odd(range(5))
    [1, 3]
    """
    cdef vector[int] out
    copy_if(values.begin(), values.end(), back_inserter(out), is_odd)
    return out


def copy_int_n(vector[int] values, int count):
    """
    Test copy_n.

    >>> copy_int_n(range(5), 2)
    [0, 1]
    """
    cdef vector[int] out
    copy_n(values.begin(), count, back_inserter(out))
    return out


def copy_int_backward(vector[int] values):
    """
    Test copy_backward.

    >>> copy_int_backward(range(5))
    [0, 0, 0, 0, 1, 2, 3, 4]
    """
    out = vector[int](values.size() + 3)
    copy_backward(values.begin(), values.end(), out.end())
    return out


def move_int(vector[int] values):
    """
    Test move.

    >>> move_int(range(5))
    [0, 1, 2, 3, 4]
    """
    cdef vector[int] out
    move(values.begin(), values.end(), back_inserter(out))
    return out


def move_int_backward(vector[int] values):
    """
    Test move_backward.

    >>> move_int_backward(range(5))
    [0, 0, 0, 0, 1, 2, 3, 4]
    """
    out = vector[int](values.size() + 3)
    move_backward(values.begin(), values.end(), out.end())
    return out


def fill_int(vector[int] array, int value):
    """
    Test fill.

    >>> fill_int(range(5), -1)
    [-1, -1, -1, -1, -1]
    """
    fill(array.begin(), array.end(), value)
    return array


def fill_int_n(vector[int] array, int count, int value):
    """
    Test fill_n.

    >>> fill_int_n(range(5), 3, -1)
    [-1, -1, -1, 3, 4]
    """
    fill_n(array.begin(), count, value)
    return array


cdef int to_ord(unsigned char c):
    return c


def string_to_ord(string s):
    """
    Test transform (unary version).

    >> string_to_ord(b"HELLO")
    [72, 69, 76, 76, 79]
    """
    cdef vector[int] ordinals
    transform(s.begin(), s.end(), back_inserter(ordinals), to_ord)
    return ordinals


cdef int add_ints(int lhs, int rhs):
    return lhs + rhs


def add_int_vectors(vector[int] lhs, vector[int] rhs):
    """
    Test transform (binary version).

    >>> add_int_vectors([1, 2, 3], [4, 5, 6])
    [5, 7, 9]
    """
    transform(lhs.begin(), lhs.end(), rhs.begin(), lhs.begin(), add_ints)
    return lhs


cdef int i = 0
cdef int generator():
    return postincrement(i)


def generate_ints(int count):
    """
    Test generate.

    >> generate_ints(5)
    [0, 1, 2, 3, 4]
    """
    out = vector[int](count)
    generate(out.begin(), out.end(), generator)
    return out


cdef int j = 0
cdef int generator2():
    return postincrement(j)


def generate_n_ints(int count):
    """
    Test generate_n.

    >> generate_n_ints(5)
    [0, 1, 2, 3, 4, 0, 0, 0]
    """
    out = vector[int](count + 3)
    generate_n(out.begin(), count, generator2)
    return out


def remove_spaces(string s):
    """
    Test remove.

    >>> print(remove_spaces(b"Text with some   spaces").decode("ascii"))
    Textwithsomespaces
    """
    s.erase(remove(s.begin(), s.end(), ord(" ")), s.end())
    return s


cdef bool is_whitespace(unsigned char c) except -1:
    return chr(c) in " \f\n\r\t\v"


def remove_whitespace(string s):
    r"""
    Test remove_if.

    >>> print(remove_whitespace(b"Text\n with\tsome \t  whitespaces\n\n").decode("ascii"))
    Textwithsomewhitespaces
    """
    s.erase(remove_if(s.begin(), s.end(), <bool (*)(unsigned char)>is_whitespace), s.end())
    return s


def remove_spaces2(string s):
    """
    Test remove_copy.

    >>> print(remove_spaces2(b"Text with some   spaces").decode("ascii"))
    Textwithsomespaces
    """
    cdef string out
    remove_copy(s.begin(), s.end(), back_inserter(out), ord(" "))
    return out


def remove_whitespace2(string s):
    r"""
    Test remove_copy_if.

    >>> print(remove_whitespace2(b"Text\n with\tsome \t  whitespaces\n\n").decode("ascii"))
    Textwithsomewhitespaces
    """
    cdef string out
    remove_copy_if(s.begin(), s.end(), back_inserter(out), <bool (*)(unsigned char)>is_whitespace)
    return out

