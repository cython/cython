cdef class MyType:
    def dup(self):
        """
        >>> x1 = MyType()
        >>> isinstance(x1, MyType)
        True
        >>> x2 = x1.dup()
        >>> isinstance(x2, MyType)
        True
        >>> x1 != x2
        True
        """
        cdef MyType clone = <MyType>type(self)()
        return clone
