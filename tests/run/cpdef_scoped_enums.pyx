# tag: cpp
# mode: run

cdef extern from *:
    """
    enum class Enum1 {
        Item1 = 1,
        Item2 = 2
    };
    """
    cpdef enumclass Enum1:
        Item1
        Item2


def test_enum_to_list():
    """
    test_enum_to_list()
    """
    assert list(Enum1) == [1, 2], list(Enum1)


