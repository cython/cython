from enum import Enum, IntEnum

from cython import cclass

@cclass
class PyxEnum(Enum):
    TWO = 2
    THREE = 3
    FIVE = 5


def test_as_variable_from_cython():
    """
    >>> test_as_variable_from_cython()
    >>> PyxEnum.THREE
    <PyxEnum.THREE: 3>
    """
    assert list(PyxEnum) == [PyxEnum.TWO, PyxEnum.THREE, PyxEnum.FIVE], list(PyxEnum)


@cclass
class PyxEnumInt(IntEnum):
    TWO = 2
    THREE = 3
    FIVE = 5


def test_as_variable_from_cython_int():
    """
    >>> test_as_variable_from_cython_int()
    >>> PyxEnumInt.THREE
    <PyxEnumInt.THREE: 3>
    """
    assert list(PyxEnumInt) == [PyxEnumInt.TWO, PyxEnumInt.THREE, PyxEnumInt.FIVE], list(PyxEnumInt)


@cclass
class PyxEnumStr(Enum):
    TWO = "two"
    THREE = "three"
    FIVE = "five"


def test_as_variable_from_cython_str():
    """
    >>> test_as_variable_from_cython_str()
    >>> PyxEnumStr.THREE
    <PyxEnumStr.THREE: 'three'>
    """
    assert list(PyxEnumStr) == [PyxEnumStr.TWO, PyxEnumStr.THREE, PyxEnumStr.FIVE], list(PyxEnumStr)


def test_enum_member_attributes():
    """
    >>> test_enum_member_attributes()
    ('TWO', 2, 'TWO', 2)
    >>> PyxEnum.TWO.name = 'bad'  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: <enum 'Enum'> cannot set attribute 'name'
    >>> PyxEnumInt.TWO.value = 99  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: <enum 'Enum'> cannot set attribute 'value'
    """
    return PyxEnum.TWO.name, PyxEnum.TWO.value, PyxEnumInt.TWO.name, PyxEnumInt.TWO.value
