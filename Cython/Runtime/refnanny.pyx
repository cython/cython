from python_ref cimport Py_INCREF, Py_DECREF
cimport python_exc as exc


loglevel = 0
reflog = []

cdef log(level, action, obj, lineno):
    if loglevel >= level:
        reflog.append((lineno, action, id(obj)))

LOG_NONE, LOG_ALL = range(2)

class RefnannyException(Exception):
    pass

class RefnannyContext(object):
    def __init__(self):
        self.refs = {} # id -> (count, [lineno])
        self.errors = []

    def regref(self, obj, lineno):
        log(LOG_ALL, 'regref', obj, lineno)
        id_ = id(obj)
        count, linenumbers = self.refs.get(id_, (0, []))
        self.refs[id_] = (count + 1, linenumbers)
        linenumbers.append(lineno)

    def delref(self, obj, lineno):
        log(LOG_ALL, 'delref', obj, lineno)
        id_ = id(obj)
        count, linenumbers = self.refs.get(id_, (0, []))
        if count == 0:
            self.errors.append("Too many decrefs on line %d, reference acquired on lines %r" %
                (lineno, linenumbers))
        elif count == 1:
            del self.refs[id_]
        else:
            self.refs[id_] = (count - 1, linenumbers)

    def end(self):
        if len(self.refs) > 0:
            msg = ""
            for count, linenos in self.refs.itervalues():
                msg += "\n  Acquired on lines: " + ", ".join(["%d" % x for x in linenos])
            self.errors.append("References leaked: %s" % msg)
        if self.errors:
            raise RefnannyException("\n".join(self.errors))

cdef public void* __Pyx_Refnanny_NewContext(char* funcname, int lineno) except NULL:
    ctx = RefnannyContext()
    Py_INCREF(ctx)
    return <void*>ctx

cdef public void __Pyx_Refnanny_GOTREF(void* ctx, object obj, int lineno):
    if ctx == NULL: return
    (<object>ctx).regref(obj, lineno)

cdef public void __Pyx_Refnanny_GIVEREF(void* ctx, object obj, int lineno):
    if ctx == NULL: return
    (<object>ctx).delref(obj, lineno)

cdef public void __Pyx_Refnanny_INCREF(void* ctx, object obj, int lineno):
    Py_INCREF(obj)
    __Pyx_Refnanny_GOTREF(ctx, obj, lineno)
    
cdef public void __Pyx_Refnanny_DECREF(void* ctx, object obj, int lineno):
    # GIVEREF raises exception if we hit 0
    # 
    __Pyx_Refnanny_GIVEREF(ctx, obj, lineno)
    Py_DECREF(obj)
    
cdef public int __Pyx_Refnanny_FinishContext(void* ctx) except -1:
    cdef exc.PyObject* type, *value, *tb
    if exc.PyErr_Occurred():
        exc.PyErr_Fetch(&type, &value, &tb)
        Py_DECREF(<object>type); Py_DECREF(<object>value); Py_DECREF(<object>tb)
        print "cleared!"
        print (exc.PyErr_Occurred() == NULL)
    obj = <object>ctx
    try:
        obj.end()
    finally:
        Py_DECREF(obj)
    return 0

    
