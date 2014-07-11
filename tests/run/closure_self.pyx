# mode: run
# tag: closures
cdef class Test:
    cdef int x

cdef class SelfInClosure(object):
    cdef Test _t
    cdef int x

    def plain(self):
        """
        >>> o = SelfInClosure()
        >>> o.plain()
        1
        """
        self.x = 1
        return self.x

    def closure_method(self):
        """
        >>> o = SelfInClosure()
        >>> o.closure_method()() == o
        True
        """
        def nested():
            return self
        return nested

    def closure_method_cdef_attr(self, Test t):
        """
        >>> o = SelfInClosure()
        >>> o.closure_method_cdef_attr(Test())()
        (1, 2)
        """
        t.x = 2
        self._t = t
        self.x = 1
        def nested():
            return self.x, t.x
        return nested

    def call_closure_method_cdef_attr_c(self, Test t):
        """
        >>> o = SelfInClosure()
        >>> o.call_closure_method_cdef_attr_c(Test())()
        (1, 2)
        """
        return self.closure_method_cdef_attr_c(t)

    cdef closure_method_cdef_attr_c(self, Test t):
        t.x = 2
        self._t = t
        self.x = 1
        def nested():
            return self.x, t.x
        return nested
