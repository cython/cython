# mode: run
# tag: f_strings, pep498

####
# Cython specific PEP 498 tests in addition to test_fstring.pyx from CPython
####

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
    assert isinstance(c, unicode), type(c)
    return a, b, c


def format_c_numbers(int n, float f, double d):
    """
    >>> s1, s2, s3, s4 = format_c_numbers(12, 2.3456, 3.1415926)
    >>> print(s1)
    122.35
    >>> print(s2)
    3.14 2.3
    >>> print(s3)
      12f
    >>> print(s4)
    C 3.14

    """
    s1 = f"{n}{f:.3}"
    assert isinstance(s1, unicode), type(s1)
    s2 = f"{d:.3}{f:4.2}"
    assert isinstance(s2, unicode), type(s2)
    s3 = f"{n:-4}f"
    assert isinstance(s3, unicode), type(s3)
    s4 = f"{n:X}{d:5.3}"
    assert isinstance(s4, unicode), type(s4)
    return s1, s2, s3, s4


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
    assert isinstance(a, unicode), type(a)
    b = f"{s2}{s1}"
    assert isinstance(b, unicode), type(b)
    c = f"u{s2}s{s1}"
    assert isinstance(c, unicode), type(c)
    d = f"s{s1}u{s2}"
    assert isinstance(d, unicode), type(d)
    return a, b, c, d
