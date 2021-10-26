# mode: compile

cdef extern from *:
    """"
    #if PY_VERSION_HEX >= 0x03000000
     #include "Python.h"
    #else
     #include "longintrepr.h"
    #endif
    """
    ctypedef struct PyTypeObject:
        pass

    ctypedef struct PyObject:
        Py_ssize_t ob_refcnt
        PyTypeObject *ob_type

cdef extern from *:
    """"
    #if PY_VERSION_HEX >= 0x03000000
     #include "Python.h"
    #else
     #include "longintrepr.h"
    #endif
    """
    cdef struct _longobject:
        int ob_refcnt
        PyTypeObject *ob_type
#        int ob_size            # not in Py3k
        unsigned int *ob_digit

def test(temp = long(0)):
    cdef _longobject *l
    l = <_longobject *> temp
    #print sizeof(l.ob_size)    # not in Py3k
    print sizeof(l.ob_digit[0])
