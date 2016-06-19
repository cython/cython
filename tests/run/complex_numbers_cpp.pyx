# tag: cpp

from libcpp.complex cimport complex as complex_class

def double_complex(complex_class[double] a):
    """
    >>> double_complex(1 + 2j)
    (1+2j)
    >>> double_complex(1.5 + 2.5j)
    (1.5+2.5j)
    """
    return a

def double_int(complex_class[int] a):
    """
    >>> double_int(1 + 2j)
    (1+2j)
    >>> double_int(1.5 + 2.5j)
    (1+2j)
    """
    return a
