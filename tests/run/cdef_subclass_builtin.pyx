# mode: run

"""
>>> int
<class 'int'>
>>> issubclass(Int, int)
True
>>> float
<class 'float'>
>>> issubclass(Float, float)
True
>>> complex
<class 'complex'>
>>> issubclass(Complex, complex)
True

>>> issubclass(List, list)
True
>>> issubclass(Set, set)
True
>>> issubclass(Dict, dict)
True
"""

cdef class Int(int): pass
cdef class Float(float): pass
cdef class Complex(complex): pass

cdef class List(list): pass
cdef class Set(set): pass
cdef class Dict(dict): pass
