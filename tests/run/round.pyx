# mode: run

cdef float test_round_float(float value):
    return round(value)

cdef double test_round_double(double value):
    return round(value)

cdef long double test_round_long_double(long double value):
    return round(value)