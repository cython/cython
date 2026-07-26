# mode: run

cimport cython

@cython.final
cdef class AClass:
    cdef c_do_something(self, cython.integral x):
        return cython.typeof(x), x

    def do_something(self, x, selector):
        """
        >>> i = AClass()
        >>> i.do_something(1, True)
        ('short', 1)
        >>> i.do_something(2, False)
        ('long', 2)
        """
        if selector:
            return self.c_do_something[short](x)
        else:
            return self.c_do_something[long](x)
