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

    @staticmethod
    cdef static_cdef2(int* x, int* y):
        return 'cdef2', x[0] + y[0]

    @staticmethod
    cdef static_cdef_untyped(a, b):
        return 'cdef_utyped', a, b

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

def call_static_cdef2(int x, int y):
    """
    >>> call_static_cdef2(2, 3)
    ('cdef2', 5)
    """
    return A.static_cdef2(&x, &y)

def call_static_list_comprehension_GH1540(int x):
    """
    >>> call_static_list_comprehension_GH1540(5)
    [('cdef', 5), ('cdef', 5), ('cdef', 5)]
    """
    return [A.static_cdef(&x) for _ in range(3)]

# BROKEN
#def call_static_cdef_untyped(a, b):
#    """
#    >>> call_static_cdef_untyped(100, None)
#    ('cdef_untyped', 100, None)
#    """
#    return A.static_cdef_untyped(a, b)

# UNIMPLEMENTED
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
