# tag: cpp
# mode: run, no-cpp-locals

cdef extern from *:
    """
    enum Enum1 {
        Item1,
        Item2
    };

    """
    cdef enum Enum1:
        Item1
        Item2

a = Item1
b = Item2

cdef Enum1 x, y
x = Item1
y = Item2


def compare_enums():
    """
    >>> compare_enums()
    (True, True, True, True)
    """
    return x == a, a == Item1, b == y, y == Item2


cdef extern from * namespace "Namespace1":
    """
    namespace Namespace1 {
        enum Enum2 {
            Item3,
            Item4
        };
    }
    """
    cdef enum Enum2:
        Item3
        Item4

c = Item3
d = Item4

cdef Enum2 z, w
z = Item3
w = Item4


def compare_namespace_enums():
    """
    >>> compare_namespace_enums()
    (True, True, True, True)
    """
    return z == c, c == Item3, d == w, d == Item4
