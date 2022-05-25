# tag: cpp
# mode: error


cdef cppclass Base:
    __init__() nogil:
        pass

cdef cppclass Sub1(Base):
    __init__(): # implicit requires GIL
        pass

cdef cppclass Sub2(Sub1):
    __init__() nogil:
        pass

_ERRORS = u"""
10:4: Base constructor defined here.
14:4: Constructor cannot be called without GIL unless all base constructors can also be called without GIL
"""
