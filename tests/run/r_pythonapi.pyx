__doc__ = """
    >>> x = spam()
    >>> print repr(x)
    'Ftang\\x00Ftang!'
"""

cdef extern from "string.h":
    void memcpy(char *d, char *s, int n)

cdef extern from "Python.h":
    object PyString_FromStringAndSize(char *s, int len)
    
def spam():
    cdef char buf[12]
    memcpy(buf, "Ftang\0Ftang!", sizeof(buf))
    return PyString_FromStringAndSize(buf, sizeof(buf))
