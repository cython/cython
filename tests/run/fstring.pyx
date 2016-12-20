# mode: run
# tag: f_strings, pep498

####
# Cython specific PEP 498 tests in addition to test_fstring.pyx from CPython
####

import sys
IS_PYPY = hasattr(sys, 'pypy_version_info')


def format2(ab, cd):
    """
    >>> a, b, c = format2(1, 2)
    >>> print(a)
    ab2
    >>> print(b)
    1cd
    >>> print(c)
    12

    >>> a, b, c = format2('ab', 'cd')
    >>> print(a)
    abcd
    >>> print(b)
    abcd
    >>> print(c)
    abcd
    """
    a = f"ab{cd}"
    assert isinstance(a, unicode), type(a)
    b = f"{ab}cd"
    assert isinstance(b, unicode), type(b)
    c = f"{ab}{cd}"
    assert isinstance(c, unicode) or (IS_PYPY and isinstance(c, str)), type(c)
    return a, b, c


def format_c_numbers(signed char c, short s, int n, long l, float f, double d):
    """
    >>> s1, s2, s3, s4 = format_c_numbers(123, 135, 12, 12312312, 2.3456, 3.1415926)
    >>> print(s1)
    123 13512312312122.35
    >>> print(s2)
    3.14 2.3
    >>> print(s3)
      12f
    >>> print(s4)
    0C00C 3.14

    >>> s1, s2, s3, s4 = format_c_numbers(-123, -135, -12, -12312312, -2.3456, -3.1415926)
    >>> print(s1)
    -123-135-12312312-12-2.35
    >>> print(s2)
    -3.14-2.3
    >>> print(s3)
     -12f
    >>> print(s4)
    -C-0C-3.14

    """
    s1 = f"{c}{s:4}{l}{n}{f:.3}"
    assert isinstance(s1, unicode), type(s1)
    s2 = f"{d:.3}{f:4.2}"
    assert isinstance(s2, unicode), type(s2)
    s3 = f"{n:-4}f"
    assert isinstance(s3, unicode), type(s3)
    s4 = f"{n:02X}{n:03X}{d:5.3}"
    assert isinstance(s4, unicode), type(s4)
    return s1, s2, s3, s4


def format_bool(bint x):
    """
    >>> a, b, c, d = format_bool(1)
    >>> print(a)  # 1
    True
    >>> print(b)  # 1
    True
    >>> print(c)  # 1
    False
    >>> print(d)  # 1
    False

    >>> a, b, c, d = format_bool(2)
    >>> print(a)  # 2
    True
    >>> print(b)  # 2
    True
    >>> print(c)  # 2
    False
    >>> print(d)  # 2
    False

    >>> a, b, c, d = format_bool(0)
    >>> print(a)  # 3
    False
    >>> print(b)  # 3
    True
    >>> print(c)  # 3
    False
    >>> print(d)  # 3
    False
    """
    return f'{x}', f'{True}', f'{x == 2}', f'{2 > 3}'


def format_c_values(Py_UCS4 uchar, Py_UNICODE pyunicode):
    """
    >>> s, s1, s2, s3 = format_c_values(b'A'.decode('ascii'), b'X'.decode('ascii'))
    >>> print(s)
    AXAX
    >>> print(s1)
    A
    >>> print(s2)
    X
    >>> print(s3)
    None

    """
    s = f"{uchar}{pyunicode}{uchar!s}{pyunicode!s}"
    assert isinstance(s, unicode), type(s)
    s1 = f"{uchar}"
    assert isinstance(s1, unicode), type(s1)
    s2 = f"{pyunicode}"
    assert isinstance(s2, unicode), type(s2)
    l = [1, 2, 3]
    s3 = f"{l.reverse()}"  # C int return value => None
    assert isinstance(s3, unicode), type(s3)
    assert l == [3, 2, 1]
    return s, s1, s2, s3


def format_strings(str s, unicode u):
    """
    >>> a, b, c, d = format_strings('abc', b'xyz'.decode('ascii'))
    >>> print(a)
    abcxyz
    >>> print(b)
    xyzabc
    >>> print(c)
    uxyzsabc
    >>> print(d)
    sabcuxyz
    """
    a = f"{s}{u}"
    assert isinstance(a, unicode), type(a)
    b = f"{u}{s}"
    assert isinstance(b, unicode), type(b)
    c = f"u{u}s{s}"
    assert isinstance(c, unicode), type(c)
    d = f"s{s}u{u}"
    assert isinstance(d, unicode), type(d)
    return a, b, c, d


def format_str(str s1, str s2):
    """
    >>> a, b, c, d = format_str('abc', 'xyz')
    >>> print(a)
    abcxyz
    >>> print(b)
    xyzabc
    >>> print(c)
    uxyzsabc
    >>> print(d)
    sabcuxyz
    """
    a = f"{s1}{s2}"
    assert isinstance(a, unicode) or (IS_PYPY and isinstance(a, str)), type(a)
    b = f"{s2}{s1}"
    assert isinstance(b, unicode) or (IS_PYPY and isinstance(a, str)), type(b)
    c = f"u{s2}s{s1}"
    assert isinstance(c, unicode), type(c)
    d = f"s{s1}u{s2}"
    assert isinstance(d, unicode), type(d)
    return a, b, c, d
