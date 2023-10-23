# Defines the standard C++ cast operators.
#
# Due to type restrictions, these are only defined for pointer parameters,
# however that is the only case where they are significantly more interesting
# than the standard C cast operator which can be written "<T>(expression)" in
# Cython.

cdef extern from * nogil:
    fn T dynamic_cast[T](void *) except +   # nullptr may also indicate failure
    fn T static_cast[T](void *)
    fn T reinterpret_cast[T](void *)
    fn T const_cast[T](void *)
