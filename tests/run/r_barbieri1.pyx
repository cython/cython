# mode: run

"""
>>> try:
...     B()
... except Exception as e:
...     print("%s: %s" % (e.__class__.__name__, e))
Exception: crash-me
"""


cdef class A:
    def __cinit__(self):
        raise Exception(u"crash-me")


cdef class B(A):
    def __cinit__(self):
        print "hello world"
