# mode: run
# tag: pure3.0

import cython
import sys

def fix_underscores(s):
    if sys.version_info < (3, 6):
        # Py2 float() does not support PEP-515 underscore literals
        if isinstance(s, bytes):
            if not cython.compiled and b'_' in s:
                return s.replace(b'_', b'')
        elif '_' in s:
            return s.replace('_', '')
    return s


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
    >>> from_bytes(fix_underscores(b"98_5_6.2_1"))
    9856.21
    >>> from_bytes(fix_underscores(b"12_4_131_123123_1893798127398123_19238712_128937198237.8222113_519879812387"))
    1.2413112312318938e+47
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
    (123.0, 123.23, 123.76, 1e+100)
    """
    return float(b"123"), float(b"123.23"), float(fix_underscores(b"12_3.7_6")), float(b"1e100")


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
    >>> from_bytearray(bytearray(fix_underscores(b"98_5_6.2_1")))
    9856.21
    >>> from_bytearray(bytearray(fix_underscores(b"12_4_131_123123_1893798127398123_19238712_128937198237.8222113_519879812387")))
    1.2413112312318938e+47
    >>> from_bytearray(bytearray(b"123E100"))
    1.23e+102
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
    >>> from_str(fix_underscores("3_21.2_5"))
    321.25
    >>> from_str(fix_underscores("12_4_131_123123_1893798127398123_19238712_128937198237.8222113_519879812387"))
    1.2413112312318938e+47
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
    (123.0, 123.23, 124.23, 1e+100)
    """
    return float("123"), float("123.23"), float(fix_underscores("1_2_4.2_3")), float("1e100")


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
    >>> from_unicode(fix_underscores(u"12_4.8_5"))
    124.85
    >>> from_unicode(fix_underscores(u"12_4_131_123123_1893798127398123_19238712_128937198237.8222113_519879812387"))
    1.2413112312318938e+47
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
    (123.0, 123.23, 123.45, 1e+100, 123.23)
    """
    return float(u"123"), float(u"123.23"), float(fix_underscores(u"12_3.4_5")), float(u"1e100"), float(u"123.23\N{PUNCTUATION SPACE}")
