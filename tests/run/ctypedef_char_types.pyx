
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
    cdef const_uchar* ust = <unsigned char*>b'XYZ' # needs cast to unsigned

    assert typeof(st) == "const_char *", typeof(st)
    my_st = st
    assert typeof(my_st) == "const_char *", typeof(my_st)
    obj = my_st
    assert obj == b'XYZ', obj

    assert typeof(ust) == "const_uchar *", typeof(ust)
    my_ust = ust
    assert typeof(my_ust) == "const_uchar *", typeof(my_ust)
    obj = my_ust
    assert obj == b'XYZ', obj

ctypedef char mychar
ctypedef unsigned char myuchar

def const_char_arrays():
    """
    >>> const_char_arrays()
    """
    cdef int i
    cdef object obj
    cdef mychar[4]  st
    cdef myuchar[4] ust
    cdef char ch

    i = 0
    for ch in b'XYZ\0':
        st[i] = ch
        ust[i] = <unsigned char>ch
        i += 1

    assert typeof(st) == "mychar [4]", typeof(st)
    obj = st
    assert obj == b'XYZ', obj

    assert typeof(ust) == "myuchar [4]", typeof(ust)
    obj = ust
    assert obj == b'XYZ', obj
