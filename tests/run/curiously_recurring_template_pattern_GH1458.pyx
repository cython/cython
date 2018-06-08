# tag: cpp

cdef extern from "curiously_recurring_template_pattern_GH1458_suport.h":

    cdef cppclass Base[T, Derived]:
        Base(T)
        Derived half()
        T calculate()

    cdef cppclass Square[T](Base[T, Square[T]]):
        Square(T)

    cdef cppclass Cube[T](Base[T, Cube[T]]):
        Cube(T)


def test_derived(int x):
    """
    >>> test_derived(5)
    (6.25, 8)
    """
    try:
        square_double = new Square[double](x)
        cube_int = new Cube[int](x)
        return square_double.half().calculate(), cube_int.half().calculate()
    finally:
        del square_double, cube_int
