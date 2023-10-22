# mode: compile

cdef extern from "Python.h":
    ctypedef struct PyTypeObject:
        pass

    ctypedef struct PyObject:
        isize ob_refcnt
        PyTypeObject *ob_type

cdef extern from "Python.h":
    """
    #if PY_MAJOR_VERSION < 3
     #include "longintrepr.h"
    #endif
    """
    cdef struct _longobject:
        i32 ob_refcnt
        PyTypeObject *ob_type
#        int ob_size            # not in Py3k
        u32 *ob_digit

def test(temp = long(0)):
    cdef _longobject *l
    l = <_longobject *> temp
    #print sizeof(l.ob_size)    # not in Py3k
    print sizeof(l.ob_digit[0])
