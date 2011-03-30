cdef class SelfInClosure(object):
    """
    >>> o = SelfInClosure()
    >>> o.closure_method()() == o
    True
    """

    def closure_method(self):
        def nested():
            return self
        return nested
