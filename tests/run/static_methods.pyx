cdef class A:
    @staticmethod
    def static_def(int x):
        """
        >>> A.static_def(2)
        ('def', 2)
        >>> A().static_def(2)
        ('def', 2)
        """
        return 'def', x

    @staticmethod
    cdef static_cdef(int* x):
        return 'cdef', x[0]

#     @staticmethod
#     cpdef static_cpdef(int x):
#         """
#         >>> A.static_def
#         >>> A.static_cpdef
#
#         >>> A().static_def
#         >>> A().static_cpdef
#
#         >>> A.static_cpdef(2)
#         ('cpdef', 2)
#         >>> A().static_cpdef(2)
#         ('cpdef', 2)
#         """
#         return 'cpdef', x

def call_static_def(int x):
    """
    >>> call_static_def(2)
    ('def', 2)
    """
    return A.static_def(x)

def call_static_cdef(int x):
    """
    >>> call_static_cdef(2)
    ('cdef', 2)
    """
    cdef int *x_ptr = &x
    return A.static_cdef(x_ptr)

# def call_static_cpdef(int x):
#     """
#     >>> call_static_cpdef(2)
#     ('cpdef', 2)
#     """
#     return A.static_cpdef(x)

cdef class FromPxd:
    @staticmethod
    cdef static_cdef(int* x):
        return 'pxd_cdef', x[0]

def call_static_pxd_cdef(int x):
    """
    >>> call_static_pxd_cdef(2)
    ('pxd_cdef', 2)
    """
    cdef int *x_ptr = &x
    return FromPxd.static_cdef(x_ptr)
