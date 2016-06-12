#distutils: define_macros = DEFINE_NO_VALUE  DEFINE_WITH_VALUE=0

cdef extern from "define_macro_helper.h" nogil:
    int VAL;

def test():
    """
    >>> test()
    1
    """
    return VAL
