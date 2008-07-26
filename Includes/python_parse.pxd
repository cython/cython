cdef extern from "Python.h":
    ctypedef void PyObject
    #####################################################################
    # 5.5 Parsing arguments and building values
    #####################################################################
    ctypedef struct va_list
    int PyArg_ParseTuple(PyObject *args, char *format, ...)
    int PyArg_VaParse(PyObject *args, char *format, va_list vargs)
    int PyArg_ParseTupleAndKeywords(PyObject *args, PyObject *kw, char *format, char *keywords[], ...)
    int PyArg_VaParseTupleAndKeywords(PyObject *args, PyObject *kw, char *format, char *keywords[], va_list vargs)
    int PyArg_Parse(PyObject *args, char *format, ...)
    int PyArg_UnpackTuple(PyObject *args, char *name, Py_ssize_t min, Py_ssize_t max, ...)

