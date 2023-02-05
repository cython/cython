# mode: run

cdef const int int_constant = 50
cdef const int int_constant2 = int_constant
cdef const int *pint_constant


def test_constant_value():
    """
    >>> test_constant_value()
    50
    50
    """
    print(int_constant)
    print(int_constant2)


def test_constant_pointer():
    """
    >>> test_constant_pointer()
    50
    """
    pint_constant = &int_constant
    print(pint_constant[0])
