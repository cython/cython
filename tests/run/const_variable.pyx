# mode: run

cdef const int int_constant = 2
cdef const int int_constant2 = int_constant
cdef const int int_constant3
int_constant3 = 5
cdef const int *pint_constant = &int_constant
cdef const int int_sum_constant = 50 + 50
cdef const int int_sum_constant2 = int_sum_constant
# FIXME:
# cdef const int int_sum_constant3 = 10 + int_constant

cdef const float float_constant = 50.5
cdef const float float_sum_constant = 50.2 + 50.3
# FIXME:
# cdef const float float_sum_constant2 = 50.2 + float_constant

cdef int[int_constant2] myarray2 = [10, 11]
cdef int[int_constant3] myarray3 = [0, 1, 2, 3, 4]


def test_constant_int_value():
    """
    >>> test_constant_int_value()
    2
    2
    5
    100
    100
    """
    print(int_constant)
    print(int_constant2)
    print(int_constant3)
    print(int_sum_constant)
    print(int_sum_constant2)

def test_constant_float_value():
    """
    >>> test_constant_float_value()
    50.5
    100.5
    """
    print(float_constant)
    print(float_sum_constant)


def test_constant_pointer():
    """
    >>> test_constant_pointer()
    2
    5
    """
    global pint_constant
    print(pint_constant[0])
    pint_constant = &int_constant3
    print(pint_constant[0])

def test_array():
    """
    >>> test_array()
    [10, 11]
    [0, 1, 2, 3, 4]
    """
    print(myarray2)
    print(myarray3)
