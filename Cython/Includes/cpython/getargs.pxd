cdef extern from "Python.h":
    #####################################################################
    # 5.5 Parsing arguments and building values
    #####################################################################
    ctypedef struct va_list
    i32 PyArg_ParseTuple(object args, char *format, ...) except 0
    i32 PyArg_VaParse(object args, char *format, va_list vargs) except 0
    i32 PyArg_ParseTupleAndKeywords(object args, object kw, char *format, char *keywords[], ...) except 0
    i32 PyArg_VaParseTupleAndKeywords(object args, object kw, char *format, char *keywords[], va_list vargs) except 0
    i32 PyArg_Parse(object args, char *format, ...) except 0
    i32 PyArg_UnpackTuple(object args, char *name, isize min, isize max, ...) except 0
