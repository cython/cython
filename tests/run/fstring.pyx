# mode: run
# tag: f_strings, pep498, werror

####
# Cython specific PEP 498 tests in addition to test_fstring.pyx from CPython
####

cimport cython

import sys
IS_PYPY = hasattr(sys, 'pypy_version_info')

from libc.limits cimport INT_MAX, LONG_MAX, LONG_MIN

max_int = INT_MAX
max_long = LONG_MAX
min_long = LONG_MIN


@cython.test_fail_if_path_exists(
    "//FormattedValueNode",
    "//JoinedStrNode",
    "//AddNode",
)
def escaping():
    """
    >>> escaping()
    """
    assert f'{{{{{"abc"}}}}}{{}}{{' == '{{abc}}{}{'
    s = f'{{{{{"abc"}}}}}{{}}{{'
    assert s == '{{abc}}{}{', s

    assert f'\x7b}}' == '{}'
    s = f'\x7b}}'
    assert s == '{}', s

    assert f'{"{{}}"}' == '{{}}'
    s = f'{"{{}}"}'
    assert s == '{{}}', s


@cython.test_fail_if_path_exists(
    "//FormattedValueNode",
    "//JoinedStrNode",
    "//AddNode",
)
def nested_constant():
    """
    >>> print(nested_constant())
    xyabc123321
    """
    return f"""{f'''xy{f"abc{123}{'321'}"!s}'''}"""


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


ctypedef enum TestValues:
    enum_ABC = 1
    enum_XYZ = 2


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
def format_c_enum():
    """
    >>> s = format_c_enum()
    >>> s == '1-2' or s
    True
    """
    return f"{enum_ABC}-{enum_XYZ}"


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
    0C014 3.14

    >>> s1, s2, s3, s4 = format_c_numbers(-123, -135, -12, -12312312, -2.3456, -3.1415926)
    >>> print(s1)
    -123-135-12312312-12-2.35
    >>> print(s2)
    -3.14-2.3
    >>> print(s3)
     -12f
    >>> print(s4)
    -C-14-3.14

    >>> s1, s2, s3, s4 = format_c_numbers(0, 0, 0, 0, -2.3456, -0.1415926)
    >>> print(s1)
    0   000-2.35
    >>> print(s2)
    -0.142-2.3
    >>> print(s3)
       0f
    >>> print(s4)
    00000-0.142

    """
    s1 = f"{c}{s:4}{l}{n}{f:.3}"
    assert isinstance(s1, unicode), type(s1)
    s2 = f"{d:.3}{f:4.2}"
    assert isinstance(s2, unicode), type(s2)
    s3 = f"{n:-4}f"
    assert isinstance(s3, unicode), type(s3)
    s4 = f"{n:02X}{n:03o}{d:5.3}"
    assert isinstance(s4, unicode), type(s4)
    return s1, s2, s3, s4


def format_c_numbers_unsigned(unsigned char c, unsigned short s, unsigned int n, unsigned long l):
    """
    >>> s1, s2, s3 = format_c_numbers_unsigned(123, 135, 12, 12312312)
    >>> print(s1)
    123 135 5675737012
    >>> print(s2)
      12f
    >>> print(s3)
    0C014    bbdef8

    """
    s1 = f"{c}{s:4} {l:o}{n}"
    assert isinstance(s1, unicode), type(s1)
    s2 = f"{n:-4}f"
    assert isinstance(s2, unicode), type(s2)
    s3 = f"{n:02X}{n:03o}{l:10x}"
    assert isinstance(s3, unicode), type(s3)
    return s1, s2, s3


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
def format_c_numbers_max(int n, long l):
    """
    >>> n, l = max_int, max_long
    >>> s1, s2 = format_c_numbers_max(n, l)
    >>> s1 == '{n}:{l}'.format(n=n, l=l) or s1
    True
    >>> s2 == '{n:012X}:{l:020X}'.format(n=n, l=l) or s2
    True

    >>> n, l = -max_int-1, -max_long-1
    >>> s1, s2 = format_c_numbers_max(n, l)
    >>> s1 == '{n}:{l}'.format(n=n, l=l) or s1
    True
    >>> s2 == '{n:012X}:{l:020X}'.format(n=n, l=l) or s2
    True
    """
    s1 = f"{n}:{l}"
    assert isinstance(s1, unicode), type(s1)
    s2 = f"{n:012X}:{l:020X}"
    assert isinstance(s2, unicode), type(s2)
    return s1, s2


def format_c_number_const():
    """
    >>> s = format_c_number_const()
    >>> s == '{0}'.format(max_long) or s
    True
    """
    return f"{LONG_MAX}"


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
def format_c_number_range(int n):
    """
    >>> for i in range(-1000, 1001):
    ...     assert format_c_number_range(i) == str(i)
    """
    return f'{n}'


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
def format_c_number_range_width(int n):
    """
    >>> for i in range(-1000, 1001):
    ...     formatted = format_c_number_range_width(i)
    ...     expected = '{n:04d}'.format(n=i)
    ...     assert formatted == expected, "%r != %r" % (formatted, expected)
    """
    return f'{n:04}'


def format_c_number_range_width0(int n):
    """
    >>> for i in range(-100, 101):
    ...     formatted = format_c_number_range_width0(i)
    ...     expected = '{n:00d}'.format(n=i)
    ...     assert formatted == expected, "%r != %r" % (formatted, expected)
    """
    return f'{n:00}'


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
def format_c_number_range_width1(int n):
    """
    >>> for i in range(-100, 101):
    ...     formatted = format_c_number_range_width1(i)
    ...     expected = '{n:01d}'.format(n=i)
    ...     assert formatted == expected, "%r != %r" % (formatted, expected)
    """
    return f'{n:01}'


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
def format_c_number_range_width_m4(int n):
    """
    >>> for i in range(-100, 101):
    ...     formatted = format_c_number_range_width_m4(i)
    ...     expected = '{n:-4d}'.format(n=i)
    ...     assert formatted == expected, "%r != %r" % (formatted, expected)
    """
    return f'{n:-4}'


def format_c_number_range_dyn_width(int n, int width):
    """
    >>> for i in range(-1000, 1001):
    ...     assert format_c_number_range_dyn_width(i, 0) == str(i), format_c_number_range_dyn_width(i, 0)
    ...     assert format_c_number_range_dyn_width(i, 1) == '%01d' % i, format_c_number_range_dyn_width(i, 1)
    ...     assert format_c_number_range_dyn_width(i, 4) == '%04d' % i, format_c_number_range_dyn_width(i, 4)
    ...     assert format_c_number_range_dyn_width(i, 5) == '%05d' % i, format_c_number_range_dyn_width(i, 5)
    ...     assert format_c_number_range_dyn_width(i, 6) == '%06d' % i, format_c_number_range_dyn_width(i, 6)
    """
    return f'{n:0{width}}'


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
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
    s3 = f"{l.reverse()}"  # C int return value => 'None'
    assert isinstance(s3, unicode), type(s3)
    assert l == [3, 2, 1]
    return s, s1, s2, s3


xyz_ustring = u'xÄyÖz'

def format_strings(str s, unicode u):
    u"""
    >>> a, b, c, d, e, f, g = format_strings('abc', b'xyz'.decode('ascii'))
    >>> print(a)
    abcxyz
    >>> print(b)
    xyzabc
    >>> print(c)
    uxyzsabc
    >>> print(d)
    sabcuxyz
    >>> print(e)
    sabcuÄÄuxyz
    >>> print(f)
    sabcu\N{SNOWMAN}uxyz
    >>> print(g)
    sabcu\N{OLD PERSIAN SIGN A}uxyz\N{SNOWMAN}

    >>> a, b, c, d, e, f, g = format_strings('abc', xyz_ustring)
    >>> print(a)
    abcxÄyÖz
    >>> print(b)
    xÄyÖzabc
    >>> print(c)
    uxÄyÖzsabc
    >>> print(d)
    sabcuxÄyÖz
    >>> print(e)
    sabcuÄÄuxÄyÖz
    >>> print(f)
    sabcu\N{SNOWMAN}uxÄyÖz
    >>> print(g)
    sabcu\N{OLD PERSIAN SIGN A}uxÄyÖz\N{SNOWMAN}
    """
    a = f"{s}{u}"
    assert isinstance(a, unicode), type(a)
    b = f"{u}{s}"
    assert isinstance(b, unicode), type(b)
    c = f"u{u}s{s}"
    assert isinstance(c, unicode), type(c)
    d = f"s{s}u{u}"
    assert isinstance(d, unicode), type(d)
    e = f"s{s}uÄÄu{u}"
    assert isinstance(e, unicode), type(e)
    f = f"s{s}u\N{SNOWMAN}u{u}"
    assert isinstance(f, unicode), type(f)
    g = f"s{s}u\N{OLD PERSIAN SIGN A}u{u}\N{SNOWMAN}"
    assert isinstance(g, unicode), type(g)
    return a, b, c, d, e, f, g


def format_pystr(str s1, str s2):
    """
    >>> a, b, c, d = format_pystr('abc', 'xyz')
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


def raw_fstring(value):
    """
    >>> print(raw_fstring('abc'))
    abc\\x61
    """
    return fr'{value}\x61'


def format_repr(value):
    """
    >>> a, b = format_repr('abc')
    >>> print('x{value!r}x'.format(value='abc'))
    x'abc'x
    >>> print('x{value!r:6}x'.format(value='abc'))
    x'abc' x
    >>> print(a)
    x'abc'x
    >>> print(b)
    x'abc' x
    """
    a = f'x{value!r}x'
    assert isinstance(a, unicode), type(a)
    b = f'x{value!r:6}x'
    assert isinstance(b, unicode), type(b)
    return a, b


def format_str(value):
    """
    >>> a, b = format_str('abc')
    >>> print('x{value!s}x'.format(value='abc'))
    xabcx
    >>> print('x{value!s:6}x'.format(value='abc'))
    xabc   x
    >>> print(a)
    xabcx
    >>> print(b)
    xabc   x
    """
    a = f'x{value!s}x'
    assert isinstance(a, unicode), type(a)
    b = f'x{value!s:6}x'
    assert isinstance(b, unicode), type(b)
    return a, b


@cython.test_fail_if_path_exists(
    "//FormattedValueNode",  # bytes.decode() returns unicode => formatting is useless
    "//JoinedStrNode",       # replaced by call to PyUnicode_Concat()
    "//PythonCapiCallNode//PythonCapiCallNode",
)
def format_decoded_bytes(bytes value):
    """
    >>> print(format_decoded_bytes(b'xyz'))
    U-xyz
    """
    return f"U-{value.decode('utf-8')}"


@cython.test_fail_if_path_exists(
    "//AddNode",
    "//ModNode",
)
@cython.test_assert_path_exists(
    "//FormattedValueNode",
    "//JoinedStrNode",
)
def generated_fstring(int i, unicode u not None, o):
    """
    >>> i, u, o = 11, u'xyz', [1]
    >>> print(((
    ...     u"(i) %s-%.3s-%r-%.3r-%d-%3d-%o-%04o-%x-%4x-%X-%03X-%.1f-%04.2f %% "
    ...     u"(u) %s-%.2s-%r-%.7r %% "
    ...     u"(o) %s-%.2s-%r-%.2r"
    ... ) % (
    ...     i, i, i, i, i, i, i, i, i, i, i, i, i, i,
    ...     u, u, u, u,
    ...     o, o, o, o,
    ... )).replace("-u'xyz'", "-'xyz'"))
    (i) 11-11-11-11-11- 11-13-0013-b-   b-B-00B-11.0-11.00 % (u) xyz-xy-'xyz'-'xyz' % (o) [1]-[1-[1]-[1

    >>> print(generated_fstring(i, u, o).replace("-u'xyz'", "-'xyz'"))
    (i) 11-11-11-11-11- 11-13-0013-b-   b-B-00B-11.0-11.00 % (u) xyz-xy-'xyz'-'xyz' % (o) [1]-[1-[1]-[1
    """
    return (
        u"(i) %s-%.3s-%r-%.3r-%d-%3d-%o-%04o-%x-%4x-%X-%03X-%.1f-%04.2f %% "
        u"(u) %s-%.2s-%r-%.7r %% "
        u"(o) %s-%.2s-%r-%.2r"
    ) % (
        i, i, i, i, i, i, i, i, i, i, i, i, i, i,
        u, u, u, u,
        o, o, o, o,
    )


@cython.test_assert_path_exists(
    "//FormattedValueNode",
    "//JoinedStrNode",
)
def percent_s_unicode(u, int i):
    u"""
    >>> u = u'x\u0194z'
    >>> print(percent_s_unicode(u, 12))
    x\u0194z-12
    """
    return u"%s-%d" % (u, i)


########################################
# await inside f-string

def test_await_inside_f_string():
    """
    >>> test_await_inside_f_string()
    PARSED_SUCCESSFULLY
    """

    async def f():
        return "some value"

    async def main():
        print(f"{await f()}")

    print("PARSED_SUCCESSFULLY")
