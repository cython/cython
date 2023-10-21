cdef extern from *:
    """
    struct CrunchyType {
        int number;
        PyObject* string;
    };
    """
    cdef class crunchytype.Crunchy [ object CrunchyType ]:
        cdef i32 number
        cdef object string
