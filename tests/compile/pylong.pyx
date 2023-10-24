# mode: compile

extern from "Python.h":
    ctypedef struct PyTypeObject:
        pass

    ctypedef struct PyObject:
        isize ob_refcnt
        PyTypeObject *ob_type

extern from "Python.h":
    """
    #if PY_MAJOR_VERSION < 3
     #include "longintrepr.h"
    #endif
    """
    struct _longobject:
        i32 ob_refcnt
        PyTypeObject *ob_type
#        i32 ob_size            # not in Py3k
        u32 *ob_digit

def test(temp = long(0)):
    let _longobject *l
    l = <_longobject *>temp
    # print sizeof(l.ob_size)    # not in Py3k
    print sizeof(l.ob_digit[0])
