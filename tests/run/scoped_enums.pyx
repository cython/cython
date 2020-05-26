# tag: cpp
# mode: run

cdef extern from *:
    """
    enum class Enum1 {
        Item1,
        Item2
    };
    """
    cdef enumclass Enum1:
        Item1
        Item2


cdef Enum1 x, y
x = Enum1.Item1
y = Enum1.Item2


def compare_enums():
    """
    >>> compare_enums()
    (True, True, False, False)
    """
    return (
        x == Enum1.Item1,
        y == Enum1.Item2,
        x == Enum1.Item2,
        y == Enum1.Item1
    )


cdef extern from * namespace "Namespace1":
    """
    namespace Namespace1 {
        enum class Enum2 {
            Item1,
            Item2
        };
    }
    """
    cdef enumclass Enum2:
        Item1
        Item2


cdef Enum2 z, w
z = Enum2.Item1
w = Enum2.Item2


def compare_namespace_enums():
    """
    >>> compare_enums()
    (True, True, False, False)
    """
    return (
        z == Enum2.Item1,
        w == Enum2.Item2,
        z == Enum2.Item2,
        w == Enum2.Item1
    )
