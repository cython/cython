# mode: run
# tag: cpp, cpp11

cdef extern from *:
    """
    enum class Enum1 {
        Item1 = 1,
        Item2 = 2
    };

    enum class Enum2 {
        Item4 = 4,
        Item5 = 5
    };
    """
    cpdef enum class Enum1:
        Item1
        Item2

    cpdef enum class Enum2:
        """Apricots and other fruits.
        """
        Item4
        Item5


def test_enum_to_list():
    """
    >>> test_enum_to_list()
    """
    assert list(Enum1) == [1, 2]
    assert list(Enum2) == [4, 5]


def test_enum_doc():
    """
    >>> Enum2.__doc__ == "Apricots and other fruits.\\n        "
    True
    >>> Enum1.__doc__ != "Apricots and other fruits.\\n        "
    True
    """
    pass


def to_from_py_conversion(Enum1 val):
    """
    >>> to_from_py_conversion(Enum1.Item1) is Enum1.Item1
    True

    Scoped enums should not be used as flags, and therefore attempts to set them
    with arbitrary values should fail
    >>> to_from_py_conversion(500)
    Traceback (most recent call last):
    ...
    ValueError: 500 is not a valid Enum1

    # Note that the ability to bitwise-or together the two numbers is inherited
    from the Python enum (so not in Cython's remit to prevent)
    >>> to_from_py_conversion(Enum1.Item1 | Enum1.Item2)
    Traceback (most recent call last):
    ...
    ValueError: 3 is not a valid Enum1
    """
    return val


def test_pickle():
    """
    >>> from pickle import loads, dumps

    >>> loads(dumps(Enum1.Item2)) == Enum1.Item2
    True
    >>> loads(dumps(Enum2.Item4)) == Enum2.Item4
    True
    """
    pass
