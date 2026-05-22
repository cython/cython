# mode: run
# tag: pure3, enum

"""
Test for regression: @cclass Enum types with non-int values
causing TypeError when passed to typed function parameters.

GH#XXXX - TypeError: an integer is required when passing non-int
@cclass Enum member to a typed function parameter.
"""

from enum import Enum, IntEnum

from cython import cclass


@cclass
class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


@cclass
class Size(IntEnum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


def process_color(c: Color) -> Color:
    """Pass through an enum value with string values."""
    return c


def process_size(s: Size) -> Size:
    """Pass through an IntEnum value."""
    return s


def compare_colors(a: Color, b: Color) -> bool:
    """Compare two regular Enum values."""
    return a is b


def test_enum_from_py():
    """
    Test passing a regular (non-int) @cclass Enum member
    to a function with a typed parameter.

    >>> test_enum_from_py()
    <Color.RED: 'red'>
    """
    result = process_color(Color.RED)
    assert result is Color.RED, result
    print(repr(result))


def test_enum_from_py_green():
    """
    >>> test_enum_from_py_green()
    <Color.GREEN: 'green'>
    """
    result = process_color(Color.GREEN)
    assert result is Color.GREEN, result
    print(repr(result))


def test_intenum_from_py():
    """
    Test that IntEnum still works correctly (regression check).

    >>> test_intenum_from_py()
    <Size.LARGE: 3>
    """
    result = process_size(Size.LARGE)
    assert result is Size.LARGE, result
    print(repr(result))


def test_intenum_int_value():
    """
    Test passing an int value to an IntEnum typed parameter.
    The int gets converted to the C enum value and may come back
    as a plain int (not the enum wrapper).

    >>> test_intenum_int_value()
    True
    """
    s = process_size(1)
    print(s == 1)


def test_enum_compare():
    """
    Test comparing two enum values passed as arguments.

    >>> test_enum_compare()
    True
    False
    """
    print(compare_colors(Color.RED, Color.RED))
    print(compare_colors(Color.RED, Color.BLUE))


def test_enum_in_function_call():
    """
    Test passing enum result directly into another function call.

    >>> test_enum_in_function_call()
    <Color.BLUE: 'blue'>
    """
    result = process_color(process_color(Color.BLUE))
    assert result is Color.BLUE, result
    print(repr(result))


def test_enum_from_py_compare_identity():
    """
    Test that enum from_py preserves identity.

    >>> test_enum_from_py_compare_identity()
    True
    True
    """
    result = process_color(Color.GREEN)
    print(result is Color.GREEN)
    print(result == Color.GREEN)
