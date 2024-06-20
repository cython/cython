# mode: compile

cdef extern from "Python.h":
    ctypedef struct PyTypeObject:
        pass

    ctypedef struct PyObject:
        Py_ssize_t ob_refcnt
        PyTypeObject *ob_type

cdef extern from "Python.h":
    cdef struct _longobject:
        int ob_refcnt
        PyTypeObject *ob_type
#        int ob_size            # not in Py3k
        unsigned int *ob_digit

def test(temp = int(0)):
    cdef _longobject *l
    l = <_longobject *> temp
    #print sizeof(l.ob_size)    # not in Py3k
    print sizeof(l.ob_digit[0])
