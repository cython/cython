__doc__ = u"""
>>> call_method( ExtType() ).method()
1
"""

cdef class ExtType:
    cdef c_method(self):
        return self

    def method(self):
        return 1

def call_method(ExtType et):
    return <ExtType>et.c_method()
