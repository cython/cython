# hack to avoid C compiler warnings about unused functions in the NumPy header files

from numpy cimport import_array  # , import_umath

cdef extern from *:
   bint FALSE "0"

if FALSE:
    import_array()
#    import_umath()
