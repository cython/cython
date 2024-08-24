# mode: run

"""
>>> issubclass(Int, int)
True
>>> issubclass(Float, float)
True
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
