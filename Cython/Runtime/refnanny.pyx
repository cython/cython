from python_ref cimport Py_INCREF, Py_DECREF, Py_XDECREF
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

    def regref(self, obj, lineno, is_null):
        log(LOG_ALL, 'regref', "<NULL>" if is_null else obj, lineno)
        if is_null:
            self.errors.append("NULL argument on line %d" % lineno)
            return
        id_ = id(obj)
        count, linenumbers = self.refs.get(id_, (0, []))
        self.refs[id_] = (count + 1, linenumbers)
        linenumbers.append(lineno)

    def delref(self, obj, lineno, is_null):
        log(LOG_ALL, 'delref', "<NULL>" if is_null else obj, lineno)
        if is_null:
            self.errors.append("NULL argument on line %d" % lineno)
            return
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
#            print self.errors
            raise RefnannyException("\n".join(self.errors))

cdef void* Refnanny_NewContext(char* funcname, int lineno) except NULL:
    if exc.PyErr_Occurred() != NULL:
        print "error flag set on newcontext?"
        return NULL
    ctx = RefnannyContext()
    Py_INCREF(ctx)
    return <void*>ctx

cdef void Refnanny_GOTREF(void* ctx, void* p_obj, int lineno):
    cdef exc.PyObject* type = NULL, *value = NULL, *tb = NULL
    if ctx == NULL: return
    exc.PyErr_Fetch(&type, &value, &tb)
    try:
        if p_obj is NULL:
            (<object>ctx).regref(None, lineno, True)
        else:
            (<object>ctx).regref(<object>p_obj, lineno, False)
        exc.PyErr_Restore(<object>type, <object>value, <object>tb)
    except:
        Py_XDECREF(<object>type)
        Py_XDECREF(<object>value)
        Py_XDECREF(<object>tb)
        raise

cdef void Refnanny_GIVEREF(void* ctx, void* p_obj, int lineno):
    cdef exc.PyObject* type = NULL, *value = NULL, *tb = NULL
    if ctx == NULL: return
    exc.PyErr_Fetch(&type, &value, &tb)
    try:
        if p_obj is NULL:
            (<object>ctx).delref(None, lineno, True)
        else:
            (<object>ctx).delref(<object>p_obj, lineno, False)
        exc.PyErr_Restore(<object>type, <object>value, <object>tb)
    except:
        Py_XDECREF(<object>type)
        Py_XDECREF(<object>value)
        Py_XDECREF(<object>tb)
        raise

cdef void Refnanny_INCREF(void* ctx, void* obj, int lineno):
    if obj is not NULL: Py_INCREF(<object>obj)
    Refnanny_GOTREF(ctx, obj, lineno)

cdef void Refnanny_DECREF(void* ctx, void* obj, int lineno):
    # GIVEREF raises exception if we hit 0
    Refnanny_GIVEREF(ctx, obj, lineno)
    if obj is not NULL: Py_DECREF(<object>obj)

cdef int Refnanny_FinishContext(void* ctx) except -1:
    cdef exc.PyObject* type = NULL, *value = NULL, *tb = NULL
    if ctx == NULL:
        assert False
    exc.PyErr_Fetch(&type, &value, &tb)
    obj = <object>ctx
    try:
        obj.end()
        exc.PyErr_Restore(<object>type, <object>value, <object>tb)
    except Exception, e:
        Py_XDECREF(<object>type)
        Py_XDECREF(<object>value)
        Py_XDECREF(<object>tb)
        raise
    finally:
        Py_XDECREF(obj)
    return 0




cdef extern from "Python.h":
    object PyCObject_FromVoidPtr(void *, void (*)(void*))

ctypedef struct RefnannyAPIStruct:
  void (*INCREF)(void*, void*, int)
  void (*DECREF)(void*, void*, int)
  void (*GOTREF)(void*, void*, int)
  void (*GIVEREF)(void*, void*, int)
  void* (*NewContext)(char*, int) except NULL
  int (*FinishContext)(void*) except -1

cdef RefnannyAPIStruct api
api.INCREF = Refnanny_INCREF
api.DECREF =  Refnanny_DECREF
api.GOTREF =  Refnanny_GOTREF
api.GIVEREF = Refnanny_GIVEREF
api.NewContext = Refnanny_NewContext
api.FinishContext = Refnanny_FinishContext

RefnannyAPI = PyCObject_FromVoidPtr(&api, NULL)
