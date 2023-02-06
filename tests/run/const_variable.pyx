# mode: run

cdef const int int_constant = 50
cdef const int int_constant2 = int_constant
cdef const int int_constant3
int_constant3 = 5
cdef const int *pint_constant = &int_constant
cdef const int int_sum_constant = 50 + 50
# FIXME:
# cdef const int int_sum_constant = 10 + int_constant

cdef const float float_constant = 50.5
# FIXME:
# cdef const float float_sum_constant = 50.2 + 50.3
# cdef const float float_sum_constant = 50.2 + float_constant


def test_constant_int_value():
    """
    >>> test_constant_int_value()
    50
    50
    100
    """
    print(int_constant)
    print(int_constant2)
    print(int_sum_constant)

def test_array():
    """
    >>> test_array()
    5
    """
    cdef int[int_constant3] int_array
    print(len(int_array))


def test_constant_float_value():
    """
    >>> test_constant_float_value()
    50.5
    """
    print(float_constant)


def test_constant_pointer():
    """
    >>> test_constant_pointer()
    50
    5
    """
    global pint_constant
    print(pint_constant[0])
    pint_constant = &int_constant3
    print(pint_constant[0])
