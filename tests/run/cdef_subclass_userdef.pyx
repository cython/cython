# mode: run

__doc__ = f"""
>>> int
<class '{__name__}.int'>
>>> issubclass(Int, int)
True

>>> float
<class '{__name__}.float'>
>>> issubclass(Float, float)
True

>>> complex
<class '{__name__}.complex'>
>>> issubclass(Complex, complex)
True
"""

cdef class int: pass
cdef class float: pass
cdef class complex: pass

cdef class Int(int): pass
cdef class Float(float): pass
cdef class Complex(complex): pass
