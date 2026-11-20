cdef class Base:
    cdef int a(self):
        return 1

cdef class Sub(Base):
    cdef int a(self):
        # this method is optimized converted to:
        #  -->  Cy: return Base.a(self) + 1
        #  -->  C/C++: __pyx_t_1 = __pyx_f_15class_super_opt_4Base_a(((struct __pyx_obj_15class_super_opt_Base *)__pyx_v_self));
        return super().a() + 1

cpdef test_fn():
    """
    >>> test_fn()
    """
    s = Sub()
    assert s.a() == 2
