# mode: run
# tag: pep484, warnings, pure3.6
# ticket: 5643
# cython: language_level=3

try:
    from typing import Optional
except ImportError:
    pass


# no crash
def gh5643_optional(a: Optional[int] = None):
    """
    >>> gh5643_optional()
    True
    >>> gh5643_optional(1)
    False
    """
    return a is None


# no crash
def gh5643_int_untyped(a: int = 1, b = None):
    """
    >>> gh5643_int_untyped(2)
    (False, True)
    >>> gh5643_int_untyped(2, None)
    (False, True)
    >>> gh5643_int_untyped(1, 3)
    (True, False)
    """
    return a == 1, b is None


# used to crash
def gh5643_int_int_none(a: int = 1, b: int = None):  # should warn about missing "Optional[]"
    """
    >>> gh5643_int_int_none()
    (True, True)
    >>> gh5643_int_int_none(2, 3)
    (False, False)
    """
    return a == 1, b is None


def gh5643_int_int_integer(a: int = 1, b: int = 3):
    """
    >>> gh5643_int_int_integer()
    (True, True)
    >>> gh5643_int_int_integer(2, 3)
    (False, True)
    """
    return a == 1, b == 3


# used to crash
def gh5643_int_optional_none(a: int = 1, b: Optional[int] = None):
    """
    >>> gh5643_int_optional_none()
    (True, True)
    >>> gh5643_int_optional_none(2)
    (False, True)
    >>> gh5643_int_optional_none(2, 3)
    (False, False)
    """
    return a == 1, b is None


def gh5643_int_optional_integer(a: int = 1, b: Optional[int] = 2):
    """
    >>> gh5643_int_optional_integer()
    (True, True)
    >>> gh5643_int_optional_integer(2)
    (False, True)
    >>> gh5643_int_optional_integer(2, 3)
    (False, False)
    >>> gh5643_int_optional_integer(2, 2)
    (False, True)
    """
    return a == 1, b == 2


_WARNINGS = """
37:36: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
"""
