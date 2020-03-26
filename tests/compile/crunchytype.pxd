cdef extern from *:
    """
    struct CrunchyType {
        int number;
        PyObject* string;
    };
    """
    cdef class crunchytype.Crunchy [ object CrunchyType ]:
        cdef int number
        cdef object string
