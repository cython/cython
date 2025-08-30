# mode: run
# tag: cpp, cpp11

from libcpp.limits cimport numeric_limits

cdef extern from *:
    """
    enum class Enum1 {
        Item1,
        Item2
    };
    """
    cdef enum class Enum1:
        Item1
        Item2


cdef extern from * namespace "Namespace1":
    """
    namespace Namespace1 {
        enum class Enum2 {
            Item1,
            Item2
        };
    }
    """
    cdef enum class Enum2:
        Item1
        Item2


cdef enum class Enum3(int):
    a = 1
    b = 2


cdef extern from *:
    """
    enum class sorted
    {
        a = 1,
        b = 0
    };
    """
    cdef enum class Enum4 "sorted":
        a
        b


cdef extern from *:
    """
    #include <limits>

    enum class LongIntEnum : long int {
        val = std::numeric_limits<long int>::max(),
    };
    """
    enum class LongIntEnum(long int):
        val


def test_compare_enums():
    """
    >>> test_compare_enums()
    (True, True, False, False)
    """
    cdef Enum1 x, y
    x = Enum1.Item1
    y = Enum1.Item2

    return (
        x == Enum1.Item1,
        y == Enum1.Item2,
        x == Enum1.Item2,
        y == Enum1.Item1
    )

        
def test_compare_namespace_enums():
    """
    >>> test_compare_enums()
    (True, True, False, False)
    """
    cdef Enum2 z, w
    
    z = Enum2.Item1
    w = Enum2.Item2

    return (
        z == Enum2.Item1,
        w == Enum2.Item2,
        z == Enum2.Item2,
        w == Enum2.Item1
    )


def test_coerce_to_from_py_value(object i):
    """
    >>> test_coerce_to_from_py_value(1)
    (True, False)

    >>> test_coerce_to_from_py_value(2)
    (False, True)

    >>> test_coerce_to_from_py_value(3)
    (False, False)

    >>> test_coerce_to_from_py_value(11111111111111111111111111111111111111111111)
    Traceback (most recent call last):
    OverflowError: Python int too large to convert to C long
    """
    cdef Enum3 x = i
    y = Enum3.b

    return (
        x == Enum3.a,
        y == int(i)
    )


def test_reserved_cname():
    """
    >>> test_reserved_cname()
    True
    """
    cdef Enum4 x = Enum4.a
    return Enum4.a == int(1)


def test_large_enum():
    """
    >>> test_large_enum()
    True
    """
    long_max = int(numeric_limits[long].max())
    return LongIntEnum.val == long_max
