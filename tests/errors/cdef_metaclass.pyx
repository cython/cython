# mode: error

cdef class MetaclassOne(type):
    pass

cdef class MetaclassTwo(type):
    pass

cdef class MetaclassThree(object):
    pass

cdef class ClassOne:
    cdef MetaclassOne __metaclass__

cdef class ClassTwo(ClassOne):
    cdef MetaclassTwo __metaclass__

cdef class ClassThree:
    cdef MetaclassThree __metaclass__

_ERRORS = """
 16:22: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
 19:24: __metaclass__ must inherit from 'type'
"""
