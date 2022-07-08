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
    >>> to_from_py_conversion(500)
    Traceback (most recent call last):
    ...
    ValueError: 500 is not a valid Enum1
    """
    return val
