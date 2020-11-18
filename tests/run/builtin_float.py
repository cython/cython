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
    >>> from_bytes(b"123E100")
    1.23e+102
    """
    return float(s)


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_bytes_literals():
    """
    >>> from_bytes_literals()
    (123.0, 123.23, 1e+100)
    """
    return float(b"123"), float(b"123.23"), float(b"1e100")


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
    >>> from_str("123E100")
    1.23e+102
    """
    return float(s)


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_str_literals():
    """
    >>> from_str_literals()
    (123.0, 123.23, 1e+100)
    """
    return float("123"), float("123.23"), float("1e100")


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
    >>> from_unicode(u"123E100")
    1.23e+102
    >>> from_unicode(u"123.23\\N{PUNCTUATION SPACE}")
    123.23
    """
    return float(s)


@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//PythonCapiCallNode",
)
def from_unicode_literals():
    """
    >>> from_unicode_literals()
    (123.0, 123.23, 1e+100, 123.23)
    """
    return float(u"123"), float(u"123.23"), float(u"1e100"), float(u"123.23\N{PUNCTUATION SPACE}")
