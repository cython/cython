# mode: run
# tag: cpp, cpp11

cdef extern from *:
    """
    enum class Enum1 {
        Item1 = 1,
        Item2 = 2
    };
    """
    cpdef enum class Enum1:
        Item1
        Item2


def test_enum_to_list():
    """
    >>> test_enum_to_list()
    """
    assert list(Enum1) == [1, 2]
