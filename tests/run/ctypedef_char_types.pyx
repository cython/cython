
cimport cython
from cython cimport typeof

from libc.string cimport const_char, const_uchar

@cython.test_assert_path_exists(
    "//NameNode[@name = 'st' and @type.is_string = True]",
    "//NameNode[@name = 'ust' and @type.is_string = True]",
    "//NameNode[@name = 'my_st' and @type.is_string = True]",
    "//NameNode[@name = 'my_ust' and @type.is_string = True]",
    )
def const_charptrs():
    """
    >>> const_charptrs()
    """
    cdef object obj
    cdef const_char*  st  = b'XYZ'
    cdef const_uchar* ust = b'XYZ'

    assert typeof(st) == "const_char *", typeof(st)
    my_st = st
    assert typeof(my_st) == "const_char *", typeof(my_st)
    obj = my_st

    assert typeof(ust) == "const_uchar *", typeof(ust)
    my_ust = ust
    assert typeof(my_ust) == "const_uchar *", typeof(my_ust)
    obj = my_ust
