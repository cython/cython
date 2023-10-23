cdef class ExtType:
    fn c_method(self):
        return self

    def method(self):
        return 1

def call_method(ExtType et):
    """
    >>> call_method( ExtType() ).method()
    1
    """
    return <ExtType>et.c_method()
