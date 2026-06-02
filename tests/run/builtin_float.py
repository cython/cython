# mode: run
# tag: pure3.0

import cython


def empty_float():
    """
    >>> float()
    0.0
    >>> empty_float()
    0.0
    """
    x = float()
    return x


def float_conjugate():
    """
    >>> float_call_conjugate()
    1.5
    """
    x = 1.5 .conjugate()
    return x


def float_call_conjugate():
    """
    >>> float_call_conjugate()
    1.5
    """
    x = float(1.5).conjugate()
    return x


def from_int(i):
    """
    >>> from_int(0)
    0.0
    >>> from_int(1)
    1.0
    >>> from_int(-1)
    -1.0
    >>> from_int(99)
    99.0
    >>> from_int(-99)
    -99.0

    >>> for exp in (14, 15, 16, 30, 31, 32, 52, 53, 54, 60, 61, 62, 63, 64):
    ...     for sign in (1, 0, -1):
    ...         value = (sign or 1) * 2**exp + sign
    ...         float_value = from_int(value)
    ...         assert float_value == float(value), "expected %s2**%s+%s == %r, got %r, difference %r" % (
    ...             '-' if sign < 0 else '', exp, sign, float(value), float_value, float_value - float(value))
    """
    return float(i)


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_bytes(s: bytes):
    """
    >>> from_bytes(b"123")
    123.0
    >>> from_bytes(b"123.25")
    123.25
    >>> from_bytes(b"98_5_6.2_1")
    9856.21
    >>> from_bytes(b"12_4_131_123123_1893798127398123_19238712_128937198237.8222113_519879812387")
    1.2413112312318938e+47
    >>> from_bytes(b"123E100")
    1.23e+102
    >>> from_bytes(b"12__._3")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...12__._3...
    >>> from_bytes(b"_12.3")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ..._12.3...
    >>> from_bytes(b"12.3_")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...12.3_...
    >>> from_bytes(b"na_n")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...na_n...
    >>> from_bytes(b"_" * 10000)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...____...
    >>> from_bytes(None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError...
    """
    return float(s)


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_bytes_literals():
    """
    >>> from_bytes_literals()
    (123.0, 123.23, 123.76, 1e+100)
    """
    return float(b"123"), float(b"123.23"), float(b"12_3.7_6"), float(b"1e100")


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_bytearray(s: bytearray):
    """
    >>> from_bytearray(bytearray(b"123"))
    123.0
    >>> from_bytearray(bytearray(b"123.25"))
    123.25
    >>> from_bytearray(bytearray(b"98_5_6.2_1"))
    9856.21
    >>> from_bytearray(bytearray(b"12_4_131_123123_1893798127398123_19238712_128937198237.8222113_519879812387"))
    1.2413112312318938e+47
    >>> from_bytearray(bytearray(b"123E100"))
    1.23e+102
    >>> from_bytearray(bytearray(b"12__._3"))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...12__._3...
    >>> from_bytearray(bytearray(b"_12.3"))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ..._12.3...
    >>> from_bytearray(bytearray(b"12.3_"))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...12.3_...
    >>> from_bytearray(bytearray(b"in_f"))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...in_f...
    >>> from_bytearray(None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError...
    """
    return float(s)


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_str(s: 'str'):
    """
    >>> from_str("123")
    123.0
    >>> from_str("123.25")
    123.25
    >>> from_str("3_21.2_5")
    321.25
    >>> from_str("12_4_131_123123_1893798127398123_19238712_128937198237.8222113_519879812387")
    1.2413112312318938e+47
    >>> from_str("123E100")
    1.23e+102
    >>> from_str("12__._3")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...12__._3...
    >>> from_str("_12.3")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ..._12.3...
    >>> from_str("12.3_")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...12.3_...
    >>> from_str("n_an")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...n_an...
    >>> from_str(None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError...
    """
    return float(s)


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_str_literals():
    """
    >>> from_str_literals()
    (123.0, 123.23, 124.23, 1e+100)
    """
    return float("123"), float("123.23"), float("1_2_4.2_3"), float("1e100")


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_unicode(s: 'unicode'):
    """
    >>> from_unicode(u"123")
    123.0
    >>> from_unicode(u"123.25")
    123.25
    >>> from_unicode(u"12_4.8_5")
    124.85
    >>> from_unicode(u"12_4_131_123123_1893798127398123_19238712_128937198237.8222113_519879812387")
    1.2413112312318938e+47
    >>> from_unicode(u"123E100")
    1.23e+102
    >>> from_unicode("೬")
    6.0
    >>> from_unicode(u"123.23\\N{PUNCTUATION SPACE}")
    123.23
    >>> from_unicode(u"\\N{PUNCTUATION SPACE} 123.23 \\N{PUNCTUATION SPACE}")
    123.23
    >>> from_unicode(u"\\N{PUNCTUATION SPACE} 12_3.2_3 \\N{PUNCTUATION SPACE}")
    123.23
    >>> from_unicode(u"\\N{PUNCTUATION SPACE} " * 25 + u"123.54 " + u"\\N{PUNCTUATION SPACE} " * 22)  # >= 40 chars
    123.54
    >>> from_unicode(u"\\N{PUNCTUATION SPACE} " * 25 + u"1_23.5_4 " + u"\\N{PUNCTUATION SPACE} " * 22)
    123.54
    >>> from_unicode(u"\\N{PUNCTUATION SPACE} " + u"123.54 " * 2 + u"\\N{PUNCTUATION SPACE}")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...123.54 123.54...
    >>> from_unicode(u"\\N{PUNCTUATION SPACE} " * 25 + u"123.54 " * 2 + u"\\N{PUNCTUATION SPACE} " * 22)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...123.54 123.54...
    >>> from_unicode(u"_12__._3")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ..._12__._3...
    >>> from_unicode(u"_12.3")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ..._12.3...
    >>> from_unicode(u"12.3_")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...12.3_...
    >>> from_unicode(u"i_nf")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: ...i_nf...
    >>> from_unicode(None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError...
    """
    return float(s)


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_unicode_literals():
    """
    >>> from_unicode_literals()
    (123.0, 123.23, 123.45, 1e+100, 123.23)
    """
    return float(u"123"), float(u"123.23"), float(u"12_3.4_5"), float(u"1e100"), float(u"123.23\N{PUNCTUATION SPACE}")


def catch_valueerror(val):
    """
    >>> catch_valueerror("foo")
    False
    >>> catch_valueerror(u"foo")
    False
    >>> catch_valueerror(b"foo")
    False
    >>> catch_valueerror(bytearray(b"foo"))
    False
    >>> catch_valueerror("-1")
    -1.0
    """
    try:
        return float(val)
    except ValueError:
        return False
