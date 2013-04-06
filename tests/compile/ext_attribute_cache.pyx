# mode: compile

cimport cython

cdef class AttrCache(object):
    cdef public int x
    cdef object y

@cython.type_version_tag(False)
cdef class NoAttrCache(object):
    cdef public int x
    cdef object y

