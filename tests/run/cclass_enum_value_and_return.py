# mode: run
# tag: pure3, enum

"""
Test for regression: @cclass Enum with return type annotation and .value attribute access.

GH#XXXX - Compiler crash in PyTypeTestNode when returning enum from cpdef function
GH#XXXX - AttributeError when accessing .value on @cclass Enum member
"""

from enum import Enum

from cython import cclass


@cclass
class KnownPlatform(Enum):
    ANDROID = "android"
    IOS = "ios"
    WIN = "win"
    MACOSX = "macosx"
    LINUX = "linux"
    FREEBSD = "freebsd"


def get_platform_name(name: str) -> KnownPlatform:
    """
    Helper function that returns an enum based on a string.

    >>> get_platform_name("linux")
    <KnownPlatform.LINUX: 'linux'>
    >>> get_platform_name("android")
    <KnownPlatform.ANDROID: 'android'>
    """
    if name == "linux":
        return KnownPlatform.LINUX
    elif name == "android":
        return KnownPlatform.ANDROID
    elif name == "ios":
        return KnownPlatform.IOS
    elif name == "win":
        return KnownPlatform.WIN
    elif name == "macosx":
        return KnownPlatform.MACOSX
    else:
        return KnownPlatform.FREEBSD


def test_enum_return_type_annotation():
    """
    Test that returning an enum value from a function with return type annotation works.

    >>> test_enum_return_type_annotation()
    <KnownPlatform.LINUX: 'linux'>
    """
    result = get_platform_name("linux")
    assert result is KnownPlatform.LINUX, result
    print(repr(result))


def test_enum_value_direct():
    """
    Test accessing .value directly on enum member.

    >>> test_enum_value_direct()
    linux
    """
    # Direct access - this should work
    value = KnownPlatform.LINUX.value
    assert value == "linux", value
    print(value)


def test_enum_value_via_variable():
    """
    Test accessing .value via a variable.

    >>> test_enum_value_via_variable()
    linux
    """
    # Via variable - this was failing
    platform = KnownPlatform.LINUX
    value = platform.value
    assert value == "linux", value
    print(value)


def test_enum_name_attribute():
    """
    Test accessing .name on an enum member.

    >>> test_enum_name_attribute()
    LINUX
    """
    platform = KnownPlatform.LINUX
    name = platform.name
    assert name == "LINUX", name
    print(name)


def test_enum_value_comparison():
    """
    Test comparing enum values via .value attribute.

    >>> test_enum_value_comparison()
    True
    False
    """
    def is_android(p: KnownPlatform) -> bool:
        return p.value == KnownPlatform.ANDROID.value

    result1 = is_android(KnownPlatform.ANDROID)
    result2 = is_android(KnownPlatform.LINUX)
    print(result1)
    print(result2)


def test_enum_in_if_statement():
    """
    Test enum comparison in if statements with return.

    >>> test_enum_in_if_statement()
    True
    False
    """
    def check_platform(p: KnownPlatform) -> bool:
        if p.value == KnownPlatform.LINUX.value:
            return True
        return False

    result1 = check_platform(KnownPlatform.LINUX)
    result2 = check_platform(KnownPlatform.ANDROID)
    print(result1)
    print(result2)
