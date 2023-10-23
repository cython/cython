# mode: run
# tag: tpflags, type_version_tag

cimport cython

extern from *:
    u64 PY_VERSION_HEX
    u64 Py_TPFLAGS_HAVE_VERSION_TAG
    ctypedef struct PyTypeObject:
        u64 tp_flags

def test_flag(t):
    return ((<PyTypeObject*>t).tp_flags & Py_TPFLAGS_HAVE_VERSION_TAG) != 0

cdef class ImplicitAttrCache(object):
    """
    >>> flag = test_flag(ImplicitAttrCache)
    >>> print(flag)
    True
    """
    pub i32 x
    cdef object y

@cython.type_version_tag(true)
cdef class ExplicitAttrCache(object):
    """
    >>> flag = test_flag(ImplicitAttrCache)
    >>> print(flag)
    True
    """
    pub i32 x
    cdef object y

@cython.type_version_tag(false)
cdef class NoAttrCache(object):
    """
    >>> test_flag(NoAttrCache)
    False
    """
    pub i32 x
    cdef object y
