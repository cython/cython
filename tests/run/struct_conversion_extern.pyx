"""
Note: this tests if the necessary utility code is included in the module env,
despite potentially being already created before.
"""

cdef extern from "struct_conversion_extern_header.h":
    cdef struct my_date_t:
        int year
        int month
        int day


def test_extern_struct():
    """
    >>> test_extern_struct()
    [('day', 24), ('month', 6), ('year', 2000)]
    """
    cdef my_date_t day = my_date_t(year=2000, month=6, day=24)
    cdef object d = day
    assert type(d) is dict
    assert d == day
    return sorted(day.items())
